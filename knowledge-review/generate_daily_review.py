from __future__ import annotations

import os
import re
import subprocess
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
NOTES_ROOT = ROOT / "notes" / "library"
OUTPUT_ROOT = ROOT / "knowledge-review" / "content"
TODAY = date.fromisoformat(os.environ.get("REVIEW_TODAY", date.today().isoformat()))
INTERVALS = [0, 1, 2, 4, 7, 15, 30, 60]
STATUS_TO_DAYS = {"wrong": 1, "fuzzy": 2}


NOTE_TEMPLATES = {
    "notes/library/python/basics/2026-05-24笔记：RAG为什么需要chunks.md": {
        "knowledge_point": "RAG 中为什么不能直接检索整本书，以及 chunking 的核心取舍",
        "slug": "rag为什么需要chunks",
        "scope": "整本书 vs chunk、经典数据流、chunk 太大 / 太小、固定切块与更高级 chunking 相关段落。",
        "summary": "为什么要把文档切成 chunks、chunk 太大/太小时各会出现什么问题。",
        "questions": [
            "概念复述：这份笔记为什么认为 RAG 不能“直接检索整本书”，而要先做 chunking？",
            "辨析边界：chunk 太大和 chunk 太小分别会导致什么问题？它们对应牺牲了什么？",
            "实际应用：这份笔记把 chunk size 的选择总结成什么 tradeoff？你在做文本切块脚本时该优先追求什么样的切分单位？",
        ],
        "answers": [
            {
                "answer": "因为整本书一次性送给 embedding model 会遇到上下文窗口限制，而且如果整本书只生成一个 embedding，检索粒度会太粗，只能知道“这本书相关”，无法精确定位到具体片段。",
                "mistake": "把 chunking 理解成单纯为了适配 token 限制。",
                "reason": "只看到模型窗口，不去看检索定位精度。",
                "signal": "一想到 RAG，就先问自己“我要找整本书，还是找语义相关的片段”。",
            },
            {
                "answer": "chunk 太大会让 embedding 被平均化，多个主题混在一起，检索不精准；chunk 太小会让上下文断裂，语义不完整，embedding 效果变差。",
                "mistake": "只记住“大不好、小也不好”，但说不出各自坏在哪里。",
                "reason": "没有把“语义聚焦”和“上下文完整”这两个损失分开。",
                "signal": "大块先想平均化和无关内容，小块先想指代丢失和语义残缺。",
            },
            {
                "answer": "这份笔记把 chunk size 总结成“信息密度 vs 检索精度”的 tradeoff，本质上是在寻找“语义完整”的最小单元。做切块脚本时，不该只按长度机械切，而要尽量避免把一个完整语义单元从中间截断。",
                "mistake": "把 chunking 只当成 `text[i:i+chunk_size]` 的机械实现题。",
                "reason": "实现方式最显眼，容易盖过背后的检索目标。",
                "signal": "只要切块结果会把一句话或一个概念拆烂，就要反问是否破坏了语义完整性。",
            },
        ],
        "suggestion": "下次先脱稿说出“为什么不能整本书一个 embedding”，再对比一次“大 chunk 平均化”和“小 chunk 断语义”的区别。",
    },
    "notes/library/python/basics/2026-05-24笔记：字符串的方法.md": {
        "knowledge_point": "Python 字符串处理中 strip、split、join、replace 的职责边界",
        "slug": "python字符串-strip-split-join-replace",
        "scope": "`.strip()`、`.rstrip()`、`.lstrip()`、`.split()`、`.join()`、`.replace()` 相关段落。",
        "summary": "常见字符串清洗、切分、拼接、替换方法分别解决什么问题。",
        "questions": [
            "概念复述：这份笔记里 `.strip()`、`.split()`、`.join()`、`.replace()` 各自负责处理字符串的哪一类操作？",
            "辨析边界：`.strip()` 和 `.split()` 为什么不能互相替代？`.join()` 又为什么不是“再造一个 split”？",
            "实际应用：如果你拿到一段文本，想先清掉首尾空白、再切成单词列表、最后把列表拼回一句话，调用链路应该怎么组织？",
        ],
        "answers": [
            {
                "answer": "`.strip()` 负责去掉首尾空白，`.split()` 负责把字符串按分隔规则切开，`.join()` 负责把多个字符串重新拼接成一个字符串，`.replace()` 负责把旧子串替换成新子串。",
                "mistake": "把这些方法都记成“字符串处理工具”，但说不清输入输出变化。",
                "reason": "只记名字，不跟具体数据形态绑定。",
                "signal": "先问自己操作前后数据是“一个字符串”还是“字符串列表”。",
            },
            {
                "answer": "`.strip()` 处理的是首尾空白，不会把字符串切成列表；`.split()` 会按空格或指定分隔符切分，返回列表。`.join()` 的方向和 `.split()` 相反，它接收一组字符串并按连接符拼回单个字符串。",
                "mistake": "把“清洗字符串”和“切分字符串”混成一步，或者记反 `split` / `join` 的方向。",
                "reason": "三者经常连续出现，容易在流程里串台。",
                "signal": "看到列表就想到 `join`，看到单个长字符串想拆开才想到 `split`。",
            },
            {
                "answer": "可以按 `s.strip()` -> `words = s.split()` -> `' '.join(words)` 这样的顺序组织；如果还要替换其中某个词，再在合适位置插入 `.replace()`。",
                "mistake": "先 `join` 再 `split`，或者忘了先清理首尾空白。",
                "reason": "没有按数据流顺序思考字符串处理步骤。",
                "signal": "按“清洗 -> 切分 -> 处理 -> 拼接”的顺序回忆最稳。",
            },
        ],
        "suggestion": "下次直接口述一遍“`strip` 处理边缘，`split` 拆开，`join` 拼回，`replace` 替换”的最小流程。",
    },
    "notes/library/python/basics/2026-05-25笔记：argparse.md": {
        "knowledge_point": "argparse 相比 sys.argv 的优势，以及 add_argument 的基本角色",
        "slug": "argparse与sys-argv对比",
        "scope": "`argparse` 作用、和 `sys.argv` 的对比、`add_argument()`、`--help` 相关段落。",
        "summary": "为什么 CLI 参数解析更推荐 argparse，以及位置参数和可选参数的基本写法。",
        "questions": [
            "概念复述：这份笔记里 `argparse` 被定义成什么工具？它主要替你处理哪类任务？",
            "辨析边界：和直接读取 `sys.argv` 相比，`argparse` 至少在哪三件事上更强？",
            "实际应用：`parser.add_argument(\"fname\")` 和 `parser.add_argument(\"--size\")` 分别表示什么样的参数？",
        ],
        "answers": [
            {
                "answer": "`argparse` 是 Python 标准库中专门解析命令行参数的模块，用来自动读取参数、做类型转换、生成 `--help`，并检查参数是否合法。",
                "mistake": "把 `argparse` 只理解成 `sys.argv` 的语法糖。",
                "reason": "两者都处理命令行参数，表面上看像替代品。",
                "signal": "只要需求里出现帮助文档、类型检查或参数校验，就想到 `argparse`。",
            },
            {
                "answer": "笔记里强调的优势至少有三点：参数缺失时给出更清晰的错误信息、支持自动类型检查、能自动生成 `--help` 帮助文档。",
                "mistake": "只记住 `argparse` 更高级，却说不出具体高级在哪。",
                "reason": "没有把“程序员手写校验”和“库自动完成”对应起来。",
                "signal": "回忆 `IndexError`、`invalid int value`、`usage: ...` 这三个典型场景。",
            },
            {
                "answer": "`add_argument(\"fname\")` 表示必填的位置参数；`add_argument(\"--size\")` 表示带名字的可选参数，调用时通常写成 `--size 100`。",
                "mistake": "把带 `--` 的参数也当成普通位置参数，或忘记调用时要显式写名称。",
                "reason": "命令行参数的“位置”和“命名”两套风格容易混淆。",
                "signal": "没有 `--` 的通常按位置传，有 `--` 的需要带着名字传。",
            },
        ],
        "suggestion": "下次先不看答案，直接说出 `argparse` 相比 `sys.argv` 多做了哪三件事，再写一遍位置参数和可选参数的最小示例。",
    },
    "notes/library/python/basics/2026-05-25笔记：collections.Counter.md": {
        "knowledge_point": "collections.Counter 的本质、most_common 与默认计数行为",
        "slug": "collections-counter基础",
        "scope": "`Counter` 的本质、`most_common()`、不存在 key 默认返回 0、`update()` 相关段落。",
        "summary": "为什么 Counter 适合频次统计，以及它和普通 dict 的关键区别。",
        "questions": [
            "概念复述：这份笔记如何定义 `Counter`？它和普通字典的关系是什么？",
            "辨析边界：`Counter` 相比手写 `dict` 计数逻辑，省掉了哪些重复工作？不存在的 key 又会发生什么？",
            "实际应用：如果你要做 Top K 高频元素或词频统计，笔记里最关键的方法是什么？它返回的结果长什么样？",
        ],
        "answers": [
            {
                "answer": "`Counter` 是 `collections` 模块里的一个类，本质上是“专门用于计数的字典”。它仍然像字典一样存键和值，但默认把“统计出现次数”这件事封装好了。",
                "mistake": "把 `Counter` 当成完全不同的数据结构。",
                "reason": "类名特殊，容易忽略它底层仍按字典方式取值。",
                "signal": "记住它本质还是 dict，但对计数场景做了增强。",
            },
            {
                "answer": "它省掉了手写 `if key in dict` 再累加的样板代码，直接 `Counter(words)` 就能统计；而且不存在的 key 默认返回 0，不会像普通字典那样直接报错。",
                "mistake": "只看到语法更短，忽略默认值语义也更适合计数。",
                "reason": "平时更容易注意代码长度，不容易注意边界行为。",
                "signal": "一想到“频率统计”，先比较是不是还在手写 `+= 1` 分支。",
            },
            {
                "answer": "最关键的方法之一是 `most_common(n)`，它返回按频次排序后的前 n 个元素，形如 `[('a', 3), ('b', 2)]`。",
                "mistake": "记住了 `Counter` 能计数，但忘了怎么取 Top K 结果。",
                "reason": "把统计和排序当成两件脱节的事。",
                "signal": "题目里一出现“高频”“Top K”，优先想到 `most_common()`。",
            },
        ],
        "suggestion": "下次先手写一遍普通 dict 计数，再对照 `Counter(words)`，把两者差异说清楚。",
    },
}


@dataclass
class ReviewRecord:
    path: Path
    meta: dict[str, str]
    body: str
    sections: dict[str, str]

    @property
    def source_note(self) -> str:
        return self.meta["source_note"]

    @property
    def knowledge_point(self) -> str:
        return self.meta["knowledge_point"]

    @property
    def review_date(self) -> date:
        return date.fromisoformat(self.meta["review_date"])

    @property
    def next_review_date(self) -> date:
        raw = self.meta.get("next_review_date", "").strip()
        if raw:
            return date.fromisoformat(raw)
        return self.review_date


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


def split_sections(body: str) -> dict[str, str]:
    sections: dict[str, str] = {}
    matches = list(re.finditer(r"^##\s+(\d+)\.\s+(.+)$", body, flags=re.M))
    for idx, match in enumerate(matches):
        start = match.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(body)
        key = f"{match.group(1)}. {match.group(2).strip()}"
        sections[key] = body[start:end].strip()
    return sections


def load_review_records() -> list[ReviewRecord]:
    records: list[ReviewRecord] = []
    for path in sorted(OUTPUT_ROOT.glob("*/*.md")):
        if path.name.endswith("复习清单.md"):
            continue
        meta, body = parse_front_matter(path.read_text(encoding="utf-8"))
        if not meta:
            continue
        records.append(ReviewRecord(path=path, meta=meta, body=body, sections=split_sections(body)))
    return records


def checkbox_status(body: str) -> str | None:
    if "[x] 掌握" in body:
        return "mastered"
    if "[x] 模糊" in body:
        return "fuzzy"
    if "[x] 答错" in body:
        return "wrong"
    return None


def update_pending_records(records: list[ReviewRecord]) -> list[ReviewRecord]:
    updated: list[ReviewRecord] = []
    for record in records:
        if record.review_date >= TODAY or record.meta.get("status") != "pending":
            continue
        status = checkbox_status(record.body)
        if not status:
            continue
        record.meta["status"] = status
        interval_days = STATUS_TO_DAYS.get(status, next_interval_after(record.meta.get("interval_days", "0")))
        next_date = record.review_date + timedelta(days=interval_days)
        record.meta["next_review_date"] = next_date.isoformat()
        body = re.sub(
            r"(?m)^- 下次复习日期：.*$",
            f"- 下次复习日期：{next_date.isoformat()}",
            record.body,
        )
        record.body = body
        record.sections = split_sections(body)
        text = f"{render_front_matter(record.meta)}\n\n{record.body.lstrip()}"
        record.path.write_text(text, encoding="utf-8")
        updated.append(record)
    return updated


def next_interval_after(raw_days: str) -> int:
    try:
        current = int(raw_days)
    except ValueError:
        current = 0
    for idx, value in enumerate(INTERVALS):
        if value == current:
            next_idx = min(idx + 1, len(INTERVALS) - 1)
            return INTERVALS[next_idx]
    return 1


def is_knowledge_note(path: Path) -> bool:
    rel = path.relative_to(ROOT).as_posix()
    name = path.name
    lower_name = name.lower()
    if not lower_name.endswith(".md"):
        return False
    if any(part in {".git", "assets", "indexes"} for part in path.parts):
        return False
    if "journey" in path.parts and "weekly-reviews" in path.parts:
        return False
    if "templates" in path.parts:
        return False
    if lower_name in {"readme.md", "license", "license.md", "review-log.md", "problem-set.md"}:
        return False
    if "流程图" in name:
        return False
    if rel.endswith("/README.md"):
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
        notes.append(
            {
                "path": rel,
                "added_at": first_added_at(path),
            }
        )
    return notes


def latest_records(records: Iterable[ReviewRecord]) -> dict[tuple[str, str], ReviewRecord]:
    latest: dict[tuple[str, str], ReviewRecord] = {}
    for record in records:
        key = (record.source_note, record.knowledge_point)
        prev = latest.get(key)
        if prev is None or record.review_date > prev.review_date:
            latest[key] = record
    return latest


def pending_summary(records: Iterable[ReviewRecord]) -> list[str]:
    items: list[str] = []
    for record in sorted(records, key=lambda item: (item.review_date, item.path.name)):
        if record.meta.get("status") == "pending" and record.review_date < TODAY:
            items.append(record.path.name)
    return items


def build_new_card(note: dict[str, str], review_round: int = 0) -> tuple[str, str]:
    template = NOTE_TEMPLATES[note["path"]]
    card = f"""## 1. 知识点与来源

- 知识点：{template["summary"]}
- 来源：`{note["path"]}`
- 定位范围：{template["scope"]}

## 2. 知识点盲测

1. {template["questions"][0]}
2. {template["questions"][1]}
3. {template["questions"][2]}

## 3. 我的作答区

1.
>

2.
>

3.
>

## 4. 参考答案与易错点解析

<details>
<summary>展开查看参考答案与易错点</summary>

### 第 1 题

- 参考答案：{template["answers"][0]["answer"]}
- 常见误区：{template["answers"][0]["mistake"]}
- 误区产生原因：{template["answers"][0]["reason"]}
- 正确判断线索：{template["answers"][0]["signal"]}

### 第 2 题

- 参考答案：{template["answers"][1]["answer"]}
- 常见误区：{template["answers"][1]["mistake"]}
- 误区产生原因：{template["answers"][1]["reason"]}
- 正确判断线索：{template["answers"][1]["signal"]}

### 第 3 题

- 参考答案：{template["answers"][2]["answer"]}
- 常见误区：{template["answers"][2]["mistake"]}
- 误区产生原因：{template["answers"][2]["reason"]}
- 正确判断线索：{template["answers"][2]["signal"]}

</details>

## 5. 复习结果

- 自评：`[ ] 掌握` `[ ] 模糊` `[ ] 答错`
- 实际易错点：
- 完成时间：
- 下次复习日期：

## 6. 下次复习建议

{template["suggestion"]}
"""
    return template["knowledge_point"], card


def build_old_card(latest: ReviewRecord) -> str:
    sec1 = latest.sections["1. 知识点与来源"]
    sec2 = latest.sections["2. 知识点盲测"]
    sec4 = latest.sections["4. 参考答案与易错点解析"]
    sec6 = latest.sections["6. 下次复习建议"]
    prior_error = extract_actual_error(latest.body)
    if prior_error:
        suggestion = f"{sec6.strip()}\n\n上轮暴露的易错点：{prior_error}"
    else:
        suggestion = sec6.strip()
    question_count = len(re.findall(r"(?m)^\d+\.\s", sec2))
    answer_slots = []
    for idx in range(1, question_count + 1):
        answer_slots.append(f"{idx}.\n>")
    return f"""## 1. 知识点与来源

{sec1.strip()}

## 2. 知识点盲测

{sec2.strip()}

## 3. 我的作答区

{os.linesep.join(answer_slots)}

## 4. 参考答案与易错点解析

{sec4.strip()}

## 5. 复习结果

- 自评：`[ ] 掌握` `[ ] 模糊` `[ ] 答错`
- 实际易错点：
- 完成时间：
- 下次复习日期：

## 6. 下次复习建议

{suggestion}
"""


def extract_actual_error(body: str) -> str:
    match = re.search(r"(?m)^- 实际易错点：(.*)$", body)
    if not match:
        return ""
    return match.group(1).strip()


def schedule_old_candidates(records: list[ReviewRecord]) -> list[ReviewRecord]:
    status_rank = {"wrong": 0, "fuzzy": 1, "mastered": 2}
    latest = latest_records(records)
    candidates: list[ReviewRecord] = []
    for record in latest.values():
        if record.meta.get("status") == "pending":
            continue
        if record.next_review_date > TODAY:
            continue
        candidates.append(record)
    candidates.sort(
        key=lambda item: (
            item.next_review_date,
            status_rank.get(item.meta.get("status", ""), 9),
            item.review_date,
            item.source_note,
            item.knowledge_point,
        )
    )
    return candidates


def due_interval_for_old(record: ReviewRecord) -> int:
    status = record.meta.get("status")
    if status in STATUS_TO_DAYS:
        return STATUS_TO_DAYS[status]
    return next_interval_after(record.meta.get("interval_days", "0"))


def safe_slug(text: str) -> str:
    cleaned = re.sub(r"[\\/:*?\"<>|]+", "-", text).strip()
    cleaned = re.sub(r"\s+", "-", cleaned)
    cleaned = re.sub(r"-+", "-", cleaned)
    return cleaned.strip("-")


def write_card(path: Path, meta: dict[str, str], body: str) -> bool:
    if path.exists():
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"{render_front_matter(meta)}\n\n{body}", encoding="utf-8")
    return True


def main() -> None:
    source_notes = collect_source_notes()
    records = load_review_records()
    updated_records = update_pending_records(records)
    records = load_review_records()
    latest = latest_records(records)

    reviewed_notes = {record.source_note for record in records}
    new_candidates = [
        note
        for note in source_notes
        if note["path"] not in reviewed_notes and note["path"] in NOTE_TEMPLATES
    ]
    new_candidates.sort(key=lambda note: (note["added_at"], note["path"]))

    old_candidates = schedule_old_candidates(records)

    target_new = 2
    target_old = 1
    selected_new = new_candidates[:target_new]
    selected_old = old_candidates[:target_old]

    ratio_note = "比例满足 2 : 1。"
    if len(selected_new) < target_new or len(selected_old) < target_old:
        ratio_note = "比例未完全满足。"
        if len(selected_old) < target_old:
            need = min(3 - len(selected_new) - len(selected_old), max(0, len(new_candidates) - len(selected_new)))
            if need > 0:
                selected_new.extend(new_candidates[len(selected_new) : len(selected_new) + need])
        elif len(selected_new) < target_new:
            need = min(3 - len(selected_new) - len(selected_old), max(0, len(old_candidates) - len(selected_old)))
            if need > 0:
                selected_old.extend(old_candidates[len(selected_old) : len(selected_old) + need])

    out_dir = OUTPUT_ROOT / TODAY.isoformat()
    created_files = 0
    list_rows: list[tuple[str, str, str, str, str, str]] = []

    for note in selected_new:
        template = NOTE_TEMPLATES[note["path"]]
        knowledge_point, body = build_new_card(note)
        filename = f"{TODAY.isoformat()}-{safe_slug(template['slug'])}.md"
        meta = {
            "source_note": note["path"],
            "source_added_at": note["added_at"],
            "review_date": TODAY.isoformat(),
            "knowledge_point": knowledge_point,
            "new_or_old": "new",
            "review_round": "0",
            "interval_days": "0",
            "next_review_date": TODAY.isoformat(),
            "status": "pending",
        }
        created = write_card(out_dir / filename, meta, body)
        created_files += int(created)
        list_rows.append(
            (
                "new",
                knowledge_point,
                filename,
                note["added_at"],
                f"首轮建档；按添加时间排序后进入队列，且该笔记尚未进入复习记录。",
                "pending",
            )
        )

    for record in selected_old:
        filename = f"{TODAY.isoformat()}-{safe_slug(record.path.stem.split('-', 3)[-1])}.md"
        body = build_old_card(record)
        meta = {
            "source_note": record.source_note,
            "source_added_at": record.meta["source_added_at"],
            "review_date": TODAY.isoformat(),
            "knowledge_point": record.knowledge_point,
            "new_or_old": "old",
            "review_round": str(int(record.meta.get("review_round", "0")) + 1),
            "interval_days": str(due_interval_for_old(record)),
            "next_review_date": TODAY.isoformat(),
            "status": "pending",
        }
        created = write_card(out_dir / filename, meta, body)
        created_files += int(created)
        list_rows.append(
            (
                "old",
                record.knowledge_point,
                filename,
                record.meta["source_added_at"],
                f"已到期旧知识点；上一轮状态为 `{record.meta.get('status')}`，最近复习日为 {record.meta['review_date']}。",
                "pending",
            )
        )

    unresolved_pending = pending_summary(records)
    actual_new = sum(1 for row in list_rows if row[0] == "new")
    actual_old = sum(1 for row in list_rows if row[0] == "old")
    ratio_reason_parts = []
    if actual_new == 2 and actual_old == 1:
        ratio_reason_parts.append("今天按默认 3 个知识点执行，实际比例满足 2 : 1。")
    else:
        ratio_reason_parts.append(f"今天实际安排为 {actual_new} : {actual_old}。")
    if not old_candidates:
        ratio_reason_parts.append("没有可重排的已完成旧知识点；仅保留历史 pending，避免重复生成同一知识点。")
    if unresolved_pending:
        ratio_reason_parts.append(f"以下旧卡仍为未完成 pending，本次未代替你判断表现：{', '.join(unresolved_pending)}。")
    if updated_records:
        ratio_reason_parts.append(
            "本次先回填了已明确勾选自评的旧卡：" + ", ".join(record.path.name for record in updated_records) + "。"
        )

    list_lines = [
        f"# {TODAY.isoformat()} 复习清单",
        "",
        "- 计划比例：新知识点 : 旧知识点 = 2 : 1",
        f"- 实际比例：{actual_new} : {actual_old}",
        f"- 比例说明：{' '.join(ratio_reason_parts)}",
        f"- 待完成状态：共 {len(list_rows)} 个知识点，当前均为 `pending`",
        "",
        "## 今日安排",
        "",
        "| 类型 | 知识点 | 复习文件 | 来源添加时间 | 安排原因 | 状态 |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for row in list_rows:
        list_lines.append(
            f"| {row[0]} | {row[1]} | [{row[2]}](./{row[2]}) | {row[3]} | {row[4]} | {row[5]} |"
        )
    list_lines.extend(["", "## 备注", ""])
    if updated_records:
        list_lines.append(
            "- 已回填旧卡状态：" + "、".join(f"`{record.path.name}`" for record in updated_records)
        )
    else:
        list_lines.append("- 本次未发现可依据明确自评回填的历史 pending 文件。")
    if unresolved_pending:
        list_lines.append(
            "- 仍未完成的历史 pending：" + "、".join(f"`{name}`" for name in unresolved_pending)
        )
    else:
        list_lines.append("- 当前没有遗留的历史 pending 文件。")
    review_list_path = out_dir / f"{TODAY.isoformat()}-复习清单.md"
    review_list_path.write_text("\n".join(list_lines) + "\n", encoding="utf-8")
    created_files += 1

    due_old_count = len(old_candidates)
    print(f"SCANNED_NOTES={len(source_notes)}")
    print(f"NEW_CANDIDATES={len(new_candidates)}")
    print(f"DUE_OLD={due_old_count}")
    print(f"CREATED_FILES={created_files}")
    print(f"RATIO_OK={'yes' if actual_new == 2 and actual_old == 1 else 'no'}")
    print(f"RATIO_NOTE={ratio_note}")


if __name__ == "__main__":
    main()
