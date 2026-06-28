from __future__ import annotations

import os
import re
import subprocess
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTES_ROOT = ROOT / "notes" / "library"
OUTPUT_ROOT = ROOT / "knowledge-review" / "content"
TODAY = date.fromisoformat(os.environ.get("REVIEW_TODAY", date.today().isoformat()))
INTERVALS = [0, 1, 2, 4, 7, 15, 30, 60]
CHECKLIST_NAME = f"{TODAY.isoformat()}-复习清单.md"


@dataclass
class ReviewRecord:
    path: Path
    meta: dict[str, str]
    body: str

    @property
    def source_note(self) -> str:
        return self.meta["source_note"]

    @property
    def review_date(self) -> date:
        return date.fromisoformat(self.meta["review_date"])

    @property
    def next_review_date(self) -> date:
        raw = self.meta.get("next_review_date", "").strip()
        return date.fromisoformat(raw) if raw else self.review_date

    @property
    def review_round(self) -> int:
        return int(self.meta.get("review_round", "0") or 0)

    @property
    def interval_days(self) -> int:
        return int(self.meta.get("interval_days", "0") or 0)

    @property
    def status(self) -> str:
        return self.meta.get("status", "").strip()


@dataclass
class LiteHistoryItem:
    source_note: str
    source_added_at: str
    review_date: date
    new_or_old: str
    review_round: int
    interval_days: int
    next_review_date: date
    label: str
    reason: str
    status: str = "linked"


@dataclass
class NoteState:
    source_note: str
    source_added_at: str
    review_date: date
    next_review_date: date
    review_round: int
    interval_days: int
    label: str
    status: str


def parse_front_matter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        return {}, text
    parts = text.split("\n---\n", 1)
    if len(parts) != 2:
        return {}, text
    front, body = parts
    meta: dict[str, str] = {}
    for line in front.splitlines()[1:]:
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        meta[key.strip()] = value.strip()
    return meta, body


def render_front_matter(meta: dict[str, str]) -> str:
    order = [
        "source_note",
        "source_added_at",
        "review_date",
        "knowledge_point",
        "new_or_old",
        "review_round",
        "interval_days",
        "next_review_date",
        "status",
    ]
    lines = ["---"]
    for key in order:
        lines.append(f"{key}: {meta.get(key, '')}")
    lines.append("---")
    return "\n".join(lines)


def load_review_records() -> list[ReviewRecord]:
    records: list[ReviewRecord] = []
    for path in sorted(OUTPUT_ROOT.glob("*/*.md")):
        if path.name.endswith("复习清单.md"):
            continue
        meta, body = parse_front_matter(path.read_text(encoding="utf-8"))
        if not meta or "source_note" not in meta or "review_date" not in meta:
            continue
        records.append(ReviewRecord(path=path, meta=meta, body=body))
    return records


def checkbox_status(body: str) -> str | None:
    if "[x] 掌握" in body:
        return "mastered"
    if "[x] 模糊" in body:
        return "fuzzy"
    if "[x] 答错" in body:
        return "wrong"
    return None


def next_interval_after(current: int) -> int:
    for idx, value in enumerate(INTERVALS):
        if value == current:
            return INTERVALS[min(idx + 1, len(INTERVALS) - 1)]
    return 1


def update_pending_records(records: list[ReviewRecord]) -> list[ReviewRecord]:
    updated: list[ReviewRecord] = []
    for record in records:
        if record.review_date >= TODAY or record.status != "pending":
            continue
        status = checkbox_status(record.body)
        if not status:
            continue
        interval_days = 1 if status == "wrong" else 2 if status == "fuzzy" else next_interval_after(record.interval_days)
        next_date = record.review_date + timedelta(days=interval_days)
        record.meta["status"] = status
        record.meta["interval_days"] = str(interval_days)
        record.meta["next_review_date"] = next_date.isoformat()
        body = re.sub(r"(?m)^- 下次复习日期：.*$", f"- 下次复习日期：{next_date.isoformat()}", record.body)
        record.path.write_text(f"{render_front_matter(record.meta)}\n\n{body.lstrip()}", encoding="utf-8")
        updated.append(record)
    return updated


def is_knowledge_note(path: Path) -> bool:
    rel = path.relative_to(ROOT).as_posix()
    name = path.name
    lower_name = name.lower()
    if not lower_name.endswith(".md"):
        return False
    if any(part in {".git", "assets", "indexes", "review-log", "problem-set"} for part in path.parts):
        return False
    if "journey" in path.parts and "weekly-reviews" in path.parts:
        return False
    if lower_name in {"readme.md", "license", "license.md"}:
        return False
    if "流程图" in name or rel.endswith("/README.md"):
        return False
    return True


def first_added_at(path: Path) -> str:
    rel = path.relative_to(NOTES_ROOT).as_posix()
    try:
        output = subprocess.check_output(
            ["git", "-C", str(NOTES_ROOT), "log", "--diff-filter=A", "--follow", "--format=%aI", "--", rel],
            text=True,
        ).strip()
        if output:
            return output.splitlines()[-1].strip()
    except subprocess.CalledProcessError:
        pass
    stat = path.stat()
    birth = getattr(stat, "st_birthtime", 0) or stat.st_mtime
    return datetime.fromtimestamp(birth).astimezone().isoformat(timespec="seconds")


def collect_source_notes() -> list[dict[str, str]]:
    notes: list[dict[str, str]] = []
    for path in sorted(NOTES_ROOT.rglob("*.md")):
        if not is_knowledge_note(path):
            continue
        rel = path.relative_to(ROOT).as_posix()
        notes.append({"path": rel, "added_at": first_added_at(path)})
    return notes


def parse_lite_history_line(line: str) -> LiteHistoryItem | None:
    marker = "<!-- REVIEW_ITEM|"
    if not line.startswith(marker) or not line.endswith("-->"):
        return None
    payload = line[len(marker) : -3]
    parts = payload.split("|")
    if len(parts) != 9:
        return None
    new_or_old, source_note, source_added_at, review_date_raw, review_round_raw, interval_days_raw, next_review_raw, label, reason = parts
    return LiteHistoryItem(
        source_note=source_note,
        source_added_at=source_added_at,
        review_date=date.fromisoformat(review_date_raw),
        new_or_old=new_or_old,
        review_round=int(review_round_raw),
        interval_days=int(interval_days_raw),
        next_review_date=date.fromisoformat(next_review_raw),
        label=label,
        reason=reason,
    )


def load_lite_history() -> list[LiteHistoryItem]:
    items: list[LiteHistoryItem] = []
    for path in sorted(OUTPUT_ROOT.glob("*/*复习清单.md")):
        text = path.read_text(encoding="utf-8")
        for line in text.splitlines():
            item = parse_lite_history_line(line.strip())
            if item is not None:
                items.append(item)
    return items


def default_label(source_note: str) -> str:
    stem = Path(source_note).stem
    stem = re.sub(r"^\d{4}-\d{2}-\d{2}", "", stem)
    stem = stem.removeprefix("笔记：")
    stem = stem.lstrip("：:- ")
    return stem or Path(source_note).stem


def build_note_states(records: list[ReviewRecord], lite_items: list[LiteHistoryItem]) -> dict[str, NoteState]:
    states: dict[str, NoteState] = {}
    for record in records:
        state = NoteState(
            source_note=record.source_note,
            source_added_at=record.meta.get("source_added_at", ""),
            review_date=record.review_date,
            next_review_date=record.next_review_date,
            review_round=record.review_round,
            interval_days=record.interval_days,
            label=record.meta.get("knowledge_point", "").strip() or default_label(record.source_note),
            status=record.status or "pending",
        )
        previous = states.get(state.source_note)
        if previous is None or state.review_date > previous.review_date:
            states[state.source_note] = state
    for item in lite_items:
        state = NoteState(
            source_note=item.source_note,
            source_added_at=item.source_added_at,
            review_date=item.review_date,
            next_review_date=item.next_review_date,
            review_round=item.review_round,
            interval_days=item.interval_days,
            label=item.label,
            status=item.status,
        )
        previous = states.get(state.source_note)
        if previous is None or state.review_date > previous.review_date:
            states[state.source_note] = state
    return states


def schedule_old_candidates(states: dict[str, NoteState]) -> list[NoteState]:
    status_rank = {"wrong": 0, "fuzzy": 1, "pending": 2, "linked": 3, "mastered": 4}
    candidates = [
        state
        for state in states.values()
        if state.review_date < TODAY and state.next_review_date <= TODAY
    ]
    candidates.sort(
        key=lambda item: (
            item.next_review_date,
            status_rank.get(item.status, 9),
            item.review_date,
            item.source_note,
        )
    )
    return candidates


def relative_note_link(from_dir: Path, source_note: str, label: str) -> str:
    target = ROOT / source_note
    relative = os.path.relpath(target, from_dir)
    return f"[{label}]({relative})"


def build_today_rows_from_history(today_items: list[LiteHistoryItem], out_dir: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for item in today_items:
        rows.append(
            {
                "type": item.new_or_old,
                "label": item.label,
                "source_note": item.source_note,
                "source_added_at": item.source_added_at,
                "reason": "同日重跑；沿用今天已生成的轻量回看链接。",
                "link": relative_note_link(out_dir, item.source_note, item.label),
            }
        )
    return rows


def build_today_selection(
    source_notes: list[dict[str, str]],
    states: dict[str, NoteState],
) -> tuple[list[LiteHistoryItem], int, int, list[str]]:
    reviewed_notes = set(states)
    new_candidates = [note for note in source_notes if note["path"] not in reviewed_notes]
    new_candidates.sort(key=lambda item: (item["added_at"], item["path"]))
    old_candidates = schedule_old_candidates(states)

    target_new = 2
    target_old = 1
    selected_new = new_candidates[:target_new]
    selected_old = old_candidates[:target_old]

    ratio_notes: list[str] = []
    if len(selected_new) < target_new:
        need = min(3 - len(selected_new) - len(selected_old), len(old_candidates) - len(selected_old))
        if need > 0:
            selected_old.extend(old_candidates[len(selected_old) : len(selected_old) + need])
    if len(selected_old) < target_old:
        need = min(3 - len(selected_new) - len(selected_old), len(new_candidates) - len(selected_new))
        if need > 0:
            selected_new.extend(new_candidates[len(selected_new) : len(selected_new) + need])

    ratio_notes.append(f"今天实际安排为 {len(selected_new)} : {len(selected_old)}。")
    if len(new_candidates) < target_new:
        ratio_notes.append(f"新笔记候选不足：当前仅有 {len(new_candidates)} 篇从未进入回看历史的笔记。")
    if len(old_candidates) < target_old:
        ratio_notes.append(f"旧笔记候选不足：当前仅有 {len(old_candidates)} 篇已到期的历史回看笔记。")

    items: list[LiteHistoryItem] = []
    for note in selected_new:
        interval_days = next_interval_after(0)
        items.append(
            LiteHistoryItem(
                source_note=note["path"],
                source_added_at=note["added_at"],
                review_date=TODAY,
                new_or_old="new",
                review_round=0,
                interval_days=interval_days,
                next_review_date=TODAY + timedelta(days=interval_days),
                label=default_label(note["path"]),
                reason="新笔记；按添加时间从早到晚进入轻量回看队列。",
            )
        )

    for state in selected_old:
        interval_days = next_interval_after(state.interval_days)
        items.append(
            LiteHistoryItem(
                source_note=state.source_note,
                source_added_at=state.source_added_at,
                review_date=TODAY,
                new_or_old="old",
                review_round=state.review_round + 1,
                interval_days=interval_days,
                next_review_date=TODAY + timedelta(days=interval_days),
                label=state.label,
                reason=f"旧笔记；已到回看时间，上次状态为 `{state.status}`，最近回看日为 {state.review_date.isoformat()}。",
            )
        )

    return items, len(new_candidates), len(old_candidates), ratio_notes


def render_checklist(
    out_dir: Path,
    rows: list[dict[str, str]],
    hidden_items: list[LiteHistoryItem],
    ratio_parts: list[str],
    updated_records: list[ReviewRecord],
    pending_records: list[ReviewRecord],
) -> str:
    actual_new = sum(1 for row in rows if row["type"] == "new")
    actual_old = sum(1 for row in rows if row["type"] == "old")
    lines = [
        f"# {TODAY.isoformat()} 轻量复习清单",
        "",
        "- 模式：轻量回看，只回原笔记，不生成单独盲测卡。",
        "- 计划比例：新笔记 : 旧笔记 = 2 : 1",
        f"- 实际比例：{actual_new} : {actual_old}",
        f"- 比例说明：{' '.join(ratio_parts)}",
        "- 使用方式：直接点开下面 3 个笔记链接，快速回看 5-10 分钟即可。",
        "",
        "## 今日安排",
        "",
        "| 类型 | 笔记 | 打开链接 | 来源添加时间 | 安排原因 |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            f"| {row['type']} | {row['label']} | {row['link']} | {row['source_added_at']} | {row['reason']} |"
        )

    lines.extend(["", "## 备注", ""])
    if updated_records:
        lines.append("- 已回填旧卡状态：" + "、".join(f"`{record.path.name}`" for record in updated_records))
    else:
        lines.append("- 本次未发现可依据明确自评回填的历史盲测卡。")
    if pending_records:
        lines.append("- 历史盲测卡里仍未自评的文件：" + "、".join(f"`{record.path.name}`" for record in pending_records))
    else:
        lines.append("- 当前没有遗留的历史盲测卡 pending 文件。")

    lines.extend(["", "<!-- 机器可读历史，不要手动编辑 -->"])
    for item in hidden_items:
        safe_label = item.label.replace("|", "/")
        safe_reason = item.reason.replace("|", "/")
        lines.append(
            "<!-- REVIEW_ITEM|"
            f"{item.new_or_old}|{item.source_note}|{item.source_added_at}|{item.review_date.isoformat()}|"
            f"{item.review_round}|{item.interval_days}|{item.next_review_date.isoformat()}|{safe_label}|{safe_reason}"
            "-->"
        )
    return "\n".join(lines) + "\n"


def main() -> None:
    source_notes = collect_source_notes()
    records = load_review_records()
    updated_records = update_pending_records(records)
    records = load_review_records()
    lite_history = load_lite_history()
    states = build_note_states(records, lite_history)

    out_dir = OUTPUT_ROOT / TODAY.isoformat()
    out_dir.mkdir(parents=True, exist_ok=True)
    checklist_path = out_dir / CHECKLIST_NAME

    today_items = [item for item in lite_history if item.review_date == TODAY]
    pending_records = [
        record for record in records if record.status == "pending" and record.review_date < TODAY
    ]

    if today_items:
        rows = build_today_rows_from_history(today_items, out_dir)
        hidden_items = today_items
        ratio_parts = [
            f"今天实际安排为 {sum(1 for item in today_items if item.new_or_old == 'new')} : "
            f"{sum(1 for item in today_items if item.new_or_old == 'old')}。",
            "检测到今天已经生成过轻量清单，本次重跑沿用既有链接。",
        ]
        new_candidate_count = 0
        old_candidate_count = 0
    else:
        hidden_items, new_candidate_count, old_candidate_count, ratio_parts = build_today_selection(source_notes, states)
        rows = [
            {
                "type": item.new_or_old,
                "label": item.label,
                "source_note": item.source_note,
                "source_added_at": item.source_added_at,
                "reason": item.reason,
                "link": relative_note_link(out_dir, item.source_note, item.label),
            }
            for item in hidden_items
        ]

    checklist_path.write_text(
        render_checklist(out_dir, rows, hidden_items, ratio_parts, updated_records, pending_records),
        encoding="utf-8",
    )

    print(f"SCANNED_NOTES={len(source_notes)}")
    print(f"NEW_CANDIDATES={new_candidate_count}")
    print(f"DUE_OLD={old_candidate_count}")
    print("CREATED_FILES=1")
    print(f"RATIO_OK={'yes' if len([row for row in rows if row['type'] == 'new']) == 2 and len([row for row in rows if row['type'] == 'old']) == 1 else 'no'}")


if __name__ == "__main__":
    main()
