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
EXCLUDED_PARTS = {".git", "assets", "indexes", "review-log", "problem-set"}
PLACEHOLDER_SNIPPETS = (
    "用自己的话解释这个概念是什么",
    "说明它和当前项目",
    "写 3-5 句话",
    "说明它和当前项目、AI Agent、RAG、后端工程或科班基础有什么关系",
)


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
    def knowledge_point(self) -> str:
        return self.meta.get("knowledge_point", "").strip()

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
        return self.meta.get("status", "pending").strip() or "pending"

    @property
    def actual_mistakes(self) -> str:
        match = re.search(r"(?m)^- 实际易错点：(.*)$", self.body)
        return (match.group(1).strip() if match else "").strip()

    @property
    def completion_raw(self) -> str:
        match = re.search(r"(?m)^- 完成时间：(.*)$", self.body)
        return (match.group(1).strip() if match else "").strip()


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
    actual_mistakes: str = ""


@dataclass
class SourceNote:
    path: str
    added_at: str


@dataclass
class AnswerBlock:
    answer: str
    misconception: str
    cause: str
    clue: str


@dataclass
class CardDraft:
    knowledge_point: str
    short_name: str
    scope: str
    questions: list[str]
    answers: list[AnswerBlock]
    suggestion: str


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


def parse_completion_date(raw: str, fallback: date) -> date:
    value = raw.strip()
    if not value:
        return fallback
    for pattern in ("%Y-%m-%d", "%Y/%m/%d"):
        try:
            return datetime.strptime(value, pattern).date()
        except ValueError:
            continue
    match = re.fullmatch(r"(\d{1,2})[.-/月](\d{1,2})日?", value)
    if match:
        month = int(match.group(1))
        day = int(match.group(2))
        try:
            return date(TODAY.year, month, day)
        except ValueError:
            return fallback
    return fallback


def update_pending_records(records: list[ReviewRecord]) -> list[ReviewRecord]:
    updated: list[ReviewRecord] = []
    for record in records:
        if record.review_date >= TODAY or record.status != "pending":
            continue
        status = checkbox_status(record.body)
        if not status:
            continue
        base_date = parse_completion_date(record.completion_raw, record.review_date)
        if status == "wrong":
            interval_days = 1
        elif status == "fuzzy":
            interval_days = 2
        else:
            interval_days = next_interval_after(record.interval_days)
        next_date = base_date + timedelta(days=interval_days)
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
    if any(part in EXCLUDED_PARTS for part in path.parts):
        return False
    if "journey" in path.parts and "weekly-reviews" in path.parts:
        return False
    if lower_name in {"readme.md", "license", "license.md"}:
        return False
    if rel.endswith("/README.md"):
        return False
    if any(token in name for token in ("流程图", "索引", "导航")):
        return False
    return True


def first_added_at(path: Path) -> str:
    rel = path.relative_to(NOTES_ROOT).as_posix()
    try:
        output = subprocess.check_output(
            ["git", "-C", str(NOTES_ROOT), "log", "--diff-filter=A", "--follow", "--format=%aI", "--", rel],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
        if output:
            return output.splitlines()[-1].strip()
    except subprocess.CalledProcessError:
        pass
    stat = path.stat()
    birth = getattr(stat, "st_birthtime", 0) or stat.st_mtime
    return datetime.fromtimestamp(birth).astimezone().isoformat(timespec="seconds")


def collect_source_notes() -> list[SourceNote]:
    notes: list[SourceNote] = []
    for path in sorted(NOTES_ROOT.rglob("*.md")):
        if not is_knowledge_note(path):
            continue
        rel = path.relative_to(ROOT).as_posix()
        notes.append(SourceNote(path=rel, added_at=first_added_at(path)))
    return notes


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
            label=record.knowledge_point or default_label(record.source_note),
            status=record.status,
            actual_mistakes=record.actual_mistakes,
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
            status="linked",
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


def sanitize_filename_component(value: str) -> str:
    cleaned = re.sub(r"[\\\\/:*?\"<>|]", "-", value)
    cleaned = cleaned.replace("`", "")
    cleaned = re.sub(r"\s+", "-", cleaned)
    cleaned = re.sub(r"-{2,}", "-", cleaned).strip("-. ")
    return cleaned[:80] or "knowledge-point"


def note_title(source_note: str, text: str) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            return re.sub(r"^\#+\s*", "", stripped)
    stem = Path(source_note).stem
    stem = re.sub(r"^\d{4}-\d{2}-\d{2}", "", stem)
    stem = stem.replace("笔记：", "").replace("笔记；", "")
    return stem.strip(" -：:")


def parse_sections(text: str) -> list[tuple[str, str]]:
    sections: list[tuple[str, str]] = []
    current_heading: str | None = None
    buffer: list[str] = []
    for line in text.splitlines():
        if re.match(r"^\#{1,6}\s+", line.strip()):
            if current_heading is not None:
                sections.append((current_heading, "\n".join(buffer).strip()))
            current_heading = re.sub(r"^\#{1,6}\s*", "", line.strip())
            buffer = []
            continue
        buffer.append(line)
    if current_heading is not None:
        sections.append((current_heading, "\n".join(buffer).strip()))
    if sections:
        return sections
    return [("正文", text.strip())]


def strip_code_blocks(text: str) -> str:
    return re.sub(r"```.*?```", "", text, flags=re.S)


def is_placeholder_line(line: str) -> bool:
    return any(snippet in line for snippet in PLACEHOLDER_SNIPPETS)


def is_navigation_line(line: str) -> bool:
    return bool(re.fullmatch(r"\[[^\]]+\]\([^)]+\)", line.strip()))


def clean_summary_line(raw: str) -> str:
    line = raw.strip()
    if not line:
        return ""
    if line.startswith("![["):
        return ""
    line = re.sub(r"^\-+\s*", "", line)
    line = re.sub(r"^\*+\s*", "", line)
    line = re.sub(r"^\d+[.)]\s*", "", line)
    line = line.replace("`", "").strip()
    if not line or is_placeholder_line(line) or is_navigation_line(line):
        return ""
    return line


def collapse_text(text: str) -> str:
    text = strip_code_blocks(text)
    lines = []
    for raw in text.splitlines():
        line = clean_summary_line(raw)
        if not line:
            continue
        lines.append(line)
    return " ".join(lines)


def bullet_summary(text: str, limit: int = 3) -> str:
    bullets: list[str] = []
    for raw in strip_code_blocks(text).splitlines():
        line = clean_summary_line(raw)
        if not line:
            continue
        if raw.strip().startswith(("- ", "* ")) or re.match(r"^\d+[.)]\s*", raw.strip()):
            bullets.append(line)
        if len(bullets) >= limit:
            break
    if bullets:
        return "；".join(bullets[:limit])
    collapsed = collapse_text(text)
    sentences = re.split(r"[。！？]", collapsed)
    cleaned = [sentence.strip() for sentence in sentences if sentence.strip()]
    return "；".join(cleaned[:limit]) if cleaned else collapsed[:160]


def is_placeholder_body(text: str) -> bool:
    collapsed = collapse_text(text)
    if not collapsed or collapsed in {"-", "—"}:
        return True
    return any(snippet in collapsed for snippet in PLACEHOLDER_SNIPPETS)


def first_section(sections: list[tuple[str, str]], keywords: list[str]) -> tuple[str, str] | None:
    lowered = [(heading, heading.lower(), body) for heading, body in sections]
    for keyword in keywords:
        for heading, lower_heading, body in lowered:
            if keyword.lower() in lower_heading and not is_placeholder_body(body):
                return heading, body
    for keyword in keywords:
        for heading, lower_heading, body in lowered:
            if keyword.lower() in lower_heading:
                return heading, body
    return None


def is_metadata_section(heading: str, body: str) -> bool:
    collapsed = collapse_text(body)
    if heading.startswith("主题：") or heading.startswith("主题:"):
        return True
    return bool(re.fullmatch(r"日期[:：]?\s*\d{4}-\d{2}-\d{2}", collapsed))


def fallback_section(
    sections: list[tuple[str, str]],
    exclude_headings: set[str] | None = None,
) -> tuple[str, str]:
    excluded = exclude_headings or set()
    for heading, body in sections:
        if heading in excluded:
            continue
        if is_metadata_section(heading, body):
            continue
        if collapse_text(body):
            return heading, body
    for heading, body in sections:
        if heading not in excluded:
            if is_metadata_section(heading, body):
                continue
            return heading, body
    return sections[0]


def status_text(status: str) -> str:
    mapping = {
        "pending": "pending",
        "mastered": "掌握",
        "fuzzy": "模糊",
        "wrong": "答错",
        "linked": "轻量回看",
    }
    return mapping.get(status, status)


def make_answer(answer: str, kind: str, hint: str = "") -> AnswerBlock:
    common = {
        "concept": (
            "只记名词，不说明它解决什么问题。",
            "复习时只背定义，没有把概念和用途绑定起来。",
            hint or "回答时至少补一句“它解决什么问题”。",
        ),
        "boundary": (
            "把相近概念、步骤或角色混在一起。",
            "看到关键词相似，就忽略了输入输出或职责边界。",
            hint or "先问自己：这一步的输入、输出和责任分别是什么？",
        ),
        "application": (
            "背了结论，但不会落到实际调用或流程里。",
            "只停留在抽象定义，没有顺着真实使用场景走一遍。",
            hint or "把答案改写成“遇到什么场景就怎么用”的句式。",
        ),
        "complexity": (
            "只记 O(n) 之类的结论，不会解释为什么。",
            "复杂度被当成背诵项，没有对应到具体循环或数据结构。",
            hint or "用“遍历几次、额外存了什么”来解释复杂度。",
        ),
    }
    misconception, cause, clue = common[kind]
    return AnswerBlock(answer=answer, misconception=misconception, cause=cause, clue=clue)


def build_algorithm_card(source_note: str, title: str, sections: list[tuple[str, str]], preferred_label: str | None) -> CardDraft:
    problem_name = re.sub(r"^\d+[. ]*", "", title).strip()
    info = first_section(sections, ["题目信息"])
    pattern_match = re.search(r"模式：([^\n]+)", info[1]) if info else None
    pattern = pattern_match.group(1).strip() if pattern_match else "Hash Map / Set"
    statement = first_section(sections, ["题意复述"])
    signal = first_section(sections, ["模式识别信号"])
    solution = first_section(sections, ["最终解法"])
    complexity = first_section(sections, ["复杂度", "边界条件"])
    errors = first_section(sections, ["错误记录", "边界条件"])

    knowledge_point = preferred_label or f"{problem_name} 的 {pattern} 解题信号与一遍遍历思路"
    short_name = sanitize_filename_component(problem_name.lower().replace(" ", "-"))
    scope = "题意复述、模式识别信号、最终解法、复杂度/边界条件"
    questions = [
        f"概念复述：`{problem_name}` 这道题到底要你判断或返回什么？",
        f"辨析/边界：为什么这份笔记把它归到 `{pattern}`，而不是继续使用二重循环或更重的数据结构？",
        "实际应用：不看代码时，你能按顺序口述出核心解法步骤吗？",
        "复杂度检查：这份解法的时间复杂度、空间复杂度各是多少？边界条件里最容易漏掉哪类输入？",
    ]
    answers = [
        make_answer(bullet_summary(statement[1] if statement else title), "concept"),
        make_answer(
            "这份笔记强调的信号是：需要在遍历过程中快速判断“另一个值是否已经出现”，所以用"
            f"{pattern} 做查询，避免暴力双循环。{bullet_summary(signal[1] if signal else '')}",
            "boundary",
        ),
        make_answer(bullet_summary(solution[1] if solution else ""), "application"),
        make_answer(
            "复杂度部分的结论是："
            + (bullet_summary(complexity[1]) if complexity else "时间复杂度看遍历次数，空间复杂度看额外存储。"),
            "complexity",
            hint="把“遍历一次 + 查询结构”说清楚，再补边界输入。",
        ),
    ]
    if errors:
        answers[3].answer += f" 易错处还包括：{bullet_summary(errors[1])}"
    suggestion = f"下次先脱稿说出“题意 -> 为什么用 {pattern} -> 关键步骤 -> 复杂度”，再手写一遍核心循环。"
    return CardDraft(
        knowledge_point=knowledge_point,
        short_name=short_name,
        scope=scope,
        questions=questions,
        answers=answers,
        suggestion=suggestion,
    )


def build_algorithm_learning_card(title: str, sections: list[tuple[str, str]], preferred_label: str | None) -> CardDraft:
    problem_name = re.sub(r"^\d+[. ]*", "", title).strip()
    info = first_section(sections, ["题目信息"])
    current = first_section(sections, ["当前理解"])
    next_practice = first_section(sections, ["下次练习重点"])
    pattern_match = re.search(r"模式：([^\n]+)", info[1]) if info else None
    pattern = pattern_match.group(1).strip() if pattern_match else "Hash Map / Counter"
    interview_match = re.search(r"面试验收：([^\n]+)", info[1]) if info else None
    interview_goal = interview_match.group(1).strip() if interview_match else "能口述核心判断思路"

    knowledge_point = preferred_label or f"{problem_name} 的 {pattern} 判定思路"
    short_name = sanitize_filename_component(problem_name.lower().replace(" ", "-"))
    scope = "题目信息、当前理解、下次练习重点"
    questions = [
        f"概念复述：`{problem_name}` 这道题要你判断什么，最终要返回什么结果？",
        f"辨析/边界：为什么这道题更接近 `{pattern}`，而不是只判断字符是否出现过？",
        "实际应用：根据当前理解，真正需要比较或维护的关键信息是什么？",
        "下次练习：如果现在让你独立补全这题，你最该优先补哪一步证据或能力？",
    ]
    answers = [
        make_answer(
            bullet_summary(current[1] if current else problem_name),
            "concept",
        ),
        make_answer(
            f"题目信息给出的模式是 `{pattern}`。关键不在“字符/元素出现过没有”，而在于要比较需要的频率、剩余次数或对应关系是否满足题意。",
            "boundary",
        ),
        make_answer(
            bullet_summary(current[1] if current else "") or f"先抓住 `{problem_name}` 需要维护的匹配关系，再决定是否用 Counter 或字典保存频率。",
            "application",
        ),
        make_answer(
            (bullet_summary(next_practice[1]) if next_practice else interview_goal) or interview_goal,
            "application",
            hint="把下一次要独立完成的步骤说成可执行动作，而不是笼统地“再看看题解”。",
        ),
    ]
    suggestion = f"下次先脱稿说清 `{problem_name}` 要比较的对象和 `{pattern}` 的理由，再补一版可独立复现的解法步骤。"
    return CardDraft(
        knowledge_point=knowledge_point,
        short_name=short_name,
        scope=scope,
        questions=questions,
        answers=answers,
        suggestion=suggestion,
    )


def build_library_module_card(preferred_label: str | None) -> CardDraft:
    knowledge_point = preferred_label or "Python 中 import、模块与“不重复造轮子”的模块化思维"
    return CardDraft(
        knowledge_point=knowledge_point,
        short_name=sanitize_filename_component("python-import与模块化思维"),
        scope="module、pip、课程核心思想、Lecture 4 真正想培养的能力",
        questions=[
            "概念复述：这份笔记里“模块”被怎么理解？`import` 在 Python 程序里负责做什么？",
            "辨析/边界：标准库模块和通过 `pip` 安装的第三方库，在这份笔记的语境里有什么共同点和主要差别？",
            "实际应用：为什么这份笔记把 Lecture 4 的核心总结成“模块化思维”，而不是单纯多记几个库名？",
        ],
        answers=[
            AnswerBlock(
                answer="笔记把模块理解成“把函数装在里面、可被复用的功能单元”。`import` 的作用就是把模块里的能力加载进当前程序，例如导入 `random` 后再调用其中的函数。",
                misconception="把模块只看成“一个需要背名字的文件”，忽略它解决的是复用问题。",
                cause="初学时容易只记语法，不去想为什么程序要拆成模块。",
                clue="一看到 `import xxx`，先问自己“我是要复用哪类现成能力”。",
            ),
            AnswerBlock(
                answer="共同点是二者都通过 `import` 被程序使用；主要差别是标准库通常随 Python 提供，而第三方库要先通过 `pip install ...` 安装后再导入。",
                misconception="以为第三方库和标准库在使用方式上完全不同，或者把 `pip` 和 `import` 混成同一个动作。",
                cause="安装阶段和代码使用阶段经常挨着出现，容易被记成一件事。",
                clue="先分清“安装依赖”发生在命令行，“导入模块”发生在代码里。",
            ),
            AnswerBlock(
                answer="因为这讲真正想训练的是“不要重复实现基础工具，而是学会查找、导入、组合现成模块”的工程思维。笔记明确把这点总结为“Python 的强大来自生态系统”和“复用代码”。",
                misconception="把这讲理解成单纯背 `random`、`cowsay` 或 `statistics` 的零散用法。",
                cause="示例库很多，容易把注意力放在例子本身，而不是背后的复用原则。",
                clue="如果一个知识点能迁移到以后用 `requests`、`flask`、AI agent 工具链上，那它更可能是这讲真正重要的内容。",
            ),
        ],
        suggestion="下次先脱稿回答“`pip install` 和 `import` 分别发生在哪一步”，再用一句话解释为什么模块化思维比死记库名更重要。",
    )


def build_structured_card(source_note: str, title: str, sections: list[tuple[str, str]], preferred_label: str | None) -> CardDraft:
    concept = first_section(sections, ["一句话解释", "核心概念", "到底干了什么", "是什么"])
    boundary = first_section(sections, ["区别", "关系", "边界", "对比"])
    application = first_section(sections, ["为什么重要", "实际应用", "__name__", "模块搜索路径", "概念及代码", "最终解法"])
    warning = first_section(sections, ["常见错误", "不要", "错误记录"])

    concept_heading, concept_body = concept if concept else fallback_section(sections)
    application_heading, application_body = application if application else fallback_section(sections, {concept_heading})
    boundary_heading, boundary_body = boundary if boundary else fallback_section(
        sections,
        {concept_heading, application_heading},
    )

    knowledge_point = preferred_label or f"{title} 的核心作用、边界与使用场景"
    short_name = sanitize_filename_component(preferred_label or default_label(source_note))
    scope_headings = [concept_heading, boundary_heading, application_heading]
    if warning:
        scope_headings.append(warning[0])
    scope = "、".join(dict.fromkeys(scope_headings))
    questions = [
        f"概念复述：根据“{concept_heading}”，这份笔记想让你先抓住什么核心概念？",
        f"辨析/边界：根据“{boundary_heading}”，最容易混淆的两个概念、写法或角色分别是什么？",
        f"实际应用：结合“{application_heading}”，在真实代码或工程流程里你会怎么用这个知识点？",
    ]
    answers = [
        make_answer(bullet_summary(concept_body), "concept"),
        make_answer(bullet_summary(boundary_body), "boundary"),
        make_answer(bullet_summary(application_body), "application"),
    ]
    if warning:
        questions.append(f"易错点辨析：根据“{warning[0]}”，这份笔记最提醒你避免哪类错误？")
        answers.append(make_answer(bullet_summary(warning[1]), "boundary"))
    suggestion = "下次先用一句话定义概念，再补它和相邻概念的差别，最后举一个真实使用场景。"
    return CardDraft(
        knowledge_point=knowledge_point,
        short_name=short_name,
        scope=scope,
        questions=questions,
        answers=answers,
        suggestion=suggestion,
    )


def build_generic_card(source_note: str, title: str, sections: list[tuple[str, str]], preferred_label: str | None) -> CardDraft:
    bodies = [body for _, body in sections if body.strip()]
    concept_body = bodies[0] if bodies else ""
    boundary_body = bodies[1] if len(bodies) > 1 else concept_body
    application_body = bodies[2] if len(bodies) > 2 else boundary_body
    knowledge_point = preferred_label or default_label(source_note)
    short_name = sanitize_filename_component(preferred_label or default_label(source_note))
    scope = "、".join(heading for heading, _ in sections[:3]) or "正文"
    questions = [
        f"概念复述：这份笔记里“{title}”主要在解释什么？",
        "辨析/边界：如果把这份笔记里的几个关键步骤或对象说混，会混在哪里？",
        "实际应用：你在项目或做题里会在什么场景下用到它？",
    ]
    answers = [
        make_answer(bullet_summary(concept_body), "concept"),
        make_answer(bullet_summary(boundary_body), "boundary"),
        make_answer(bullet_summary(application_body), "application"),
    ]
    suggestion = "下次先口述核心定义，再补一条边界和一个实际使用场景。"
    return CardDraft(
        knowledge_point=knowledge_point,
        short_name=short_name,
        scope=scope,
        questions=questions,
        answers=answers,
        suggestion=suggestion,
    )


def build_card_draft(source_note: str, preferred_label: str | None = None) -> CardDraft:
    if source_note.endswith("2026-05-23笔记：CS50P-L4-Library.md"):
        return build_library_module_card(preferred_label)
    text = (ROOT / source_note).read_text(encoding="utf-8")
    title = note_title(source_note, text)
    sections = parse_sections(text)
    headings = [heading for heading, _ in sections]
    if re.match(r"^\d+[. ]", title) and first_section(sections, ["题目信息"]):
        if "题意复述" in headings and "最终解法" in headings:
            return build_algorithm_card(source_note, title, sections, preferred_label)
        return build_algorithm_learning_card(title, sections, preferred_label)
    if "题意复述" in headings and "最终解法" in headings:
        return build_algorithm_card(source_note, title, sections, preferred_label)
    if any(keyword in " ".join(headings) for keyword in ["一句话解释", "为什么重要", "区别", "关系", "__name__", "常见错误"]):
        return build_structured_card(source_note, title, sections, preferred_label)
    return build_generic_card(source_note, title, sections, preferred_label)


def render_card_body(draft: CardDraft, source_note: str, previous_state: NoteState | None) -> str:
    lines = [
        "## 1. 知识点与来源",
        "",
        f"- 知识点：{draft.knowledge_point}",
        f"- 来源：`{source_note}`",
        f"- 定位范围：{draft.scope}",
        "",
        "## 2. 知识点盲测",
        "",
    ]
    for idx, question in enumerate(draft.questions, start=1):
        lines.append(f"{idx}. {question}")
    lines.extend(["", "## 3. 我的作答区", ""])
    for idx in range(1, len(draft.questions) + 1):
        lines.extend([f"{idx}.", ">"])
    lines.extend(["", "## 4. 参考答案与易错点解析", "", "<details>", "<summary>展开查看参考答案与易错点</summary>", ""])
    for idx, answer in enumerate(draft.answers, start=1):
        lines.extend(
            [
                f"### 第 {idx} 题",
                "",
                f"- 参考答案：{answer.answer}",
                f"- 常见误区：{answer.misconception}",
                f"- 误区产生原因：{answer.cause}",
                f"- 正确判断线索：{answer.clue}",
                "",
            ]
        )
    lines.extend(
        [
            "</details>",
            "",
            "## 5. 复习结果",
            "",
            "- 自评：`[ ] 掌握` `[ ] 模糊` `[ ] 答错`",
            "- 实际易错点：",
            "- 完成时间：",
            "- 下次复习日期：",
            "",
            "## 6. 下次复习建议",
            "",
            draft.suggestion,
        ]
    )
    if previous_state and previous_state.actual_mistakes:
        lines.extend(["", f"上轮暴露的易错点：{previous_state.actual_mistakes}"])
    elif previous_state and previous_state.status in {"wrong", "fuzzy", "linked"}:
        lines.extend(["", f"上轮状态提示：{status_text(previous_state.status)}。这次先确认自己能否不看答案完成盲测。"])
    return "\n".join(lines) + "\n"


def relative_card_link(out_dir: Path, card_path: Path) -> str:
    relative = os.path.relpath(card_path, out_dir)
    return f"[{card_path.name}]({relative})"


def build_new_reason(note: SourceNote) -> str:
    return "首轮建档；按来源添加时间从早到晚进入队列，且该笔记尚未进入复习记录。"


def build_old_reason(state: NoteState) -> str:
    if state.status == "linked":
        return f"已到期旧知识点；上一轮是 {state.review_date.isoformat()} 的轻量回看记录，今天转入完整盲测卡。"
    if state.status == "pending":
        return f"已到期旧知识点；该知识点自 {state.review_date.isoformat()} 起仍未完成自评，按最早到期优先重新进入队列。"
    return f"已到期旧知识点；上一轮状态为 `{state.status}`，最近复习日为 {state.review_date.isoformat()}。"


def build_today_rows_from_records(today_records: list[ReviewRecord], out_dir: Path, reasons: dict[Path, str]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for record in sorted(today_records, key=lambda item: item.path.name):
        rows.append(
            {
                "type": record.meta.get("new_or_old", ""),
                "knowledge_point": record.knowledge_point,
                "source_added_at": record.meta.get("source_added_at", ""),
                "reason": reasons.get(record.path, "同日重跑；沿用今天已生成的复习卡，不重复创建同一知识点。"),
                "status": record.status,
                "path": record.path,
            }
        )
    return rows


def create_card_file(
    out_dir: Path,
    source_note: str,
    source_added_at: str,
    new_or_old: str,
    review_round: int,
    interval_days: int,
    previous_state: NoteState | None,
    preferred_label: str | None,
) -> tuple[Path, str, bool]:
    draft = build_card_draft(source_note, preferred_label=preferred_label)
    filename = f"{TODAY.isoformat()}-{draft.short_name}.md"
    card_path = out_dir / filename
    meta = {
        "source_note": source_note,
        "source_added_at": source_added_at,
        "review_date": TODAY.isoformat(),
        "knowledge_point": draft.knowledge_point,
        "new_or_old": new_or_old,
        "review_round": str(review_round),
        "interval_days": str(interval_days),
        "next_review_date": TODAY.isoformat(),
        "status": "pending",
    }
    created = False
    if not card_path.exists():
        body = render_card_body(draft, source_note, previous_state)
        card_path.write_text(f"{render_front_matter(meta)}\n\n{body}", encoding="utf-8")
        created = True
    return card_path, draft.knowledge_point, created


def render_checklist(
    rows: list[dict[str, str]],
    ratio_parts: list[str],
    updated_records: list[ReviewRecord],
    pending_records: list[ReviewRecord],
) -> str:
    actual_new = sum(1 for row in rows if row["type"] == "new")
    actual_old = sum(1 for row in rows if row["type"] == "old")
    lines = [
        f"# {TODAY.isoformat()} 复习清单",
        "",
        "- 计划比例：新知识点 : 旧知识点 = 2 : 1",
        f"- 实际比例：{actual_new} : {actual_old}",
        f"- 比例说明：{' '.join(ratio_parts)}",
        f"- 待完成状态：共 {len(rows)} 个知识点，当前均为 `pending`",
        "",
        "## 今日安排",
        "",
        "| 类型 | 知识点 | 复习文件 | 来源添加时间 | 安排原因 | 状态 |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            f"| {row['type']} | {row['knowledge_point']} | {relative_card_link(OUTPUT_ROOT / TODAY.isoformat(), row['path'])} | "
            f"{row['source_added_at']} | {row['reason']} | {row['status']} |"
        )

    lines.extend(["", "## 备注", ""])
    if updated_records:
        lines.append("- 已回填旧卡状态：" + "、".join(f"`{record.path.name}`" for record in updated_records))
    else:
        lines.append("- 本次未发现可依据明确自评回填的历史 pending 文件。")
    if pending_records:
        lines.append("- 历史 pending 但仍未自评的文件：" + "、".join(f"`{record.path.name}`" for record in pending_records))
    else:
        lines.append("- 当前没有遗留的历史 pending 文件。")
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
    pending_records = [record for record in records if record.status == "pending" and record.review_date < TODAY]
    today_records = [record for record in records if record.review_date == TODAY]

    due_old_candidates = schedule_old_candidates(states)
    new_candidates = [note for note in source_notes if note.path not in states]
    new_candidates.sort(key=lambda item: (item.added_at, item.path))

    rows: list[dict[str, str]]
    created_card_count = 0
    selected_new_count = 0
    selected_old_count = 0
    reasons_by_path: dict[Path, str] = {}

    if today_records:
        ratio_parts = [
            f"今天实际安排为 {sum(1 for item in today_records if item.meta.get('new_or_old') == 'new')} : "
            f"{sum(1 for item in today_records if item.meta.get('new_or_old') == 'old')}。",
            "检测到今天已经生成过复习卡，本次重跑沿用既有安排。",
        ]
        rows = build_today_rows_from_records(today_records, out_dir, reasons_by_path)
        selected_new_count = sum(1 for row in rows if row["type"] == "new")
        selected_old_count = sum(1 for row in rows if row["type"] == "old")
    else:
        target_new = 2
        target_old = 1
        selected_new = list(new_candidates[:target_new])
        selected_old = list(due_old_candidates[:target_old])
        ratio_parts = []

        if len(selected_new) < target_new:
            need = min(3 - len(selected_new) - len(selected_old), max(0, len(due_old_candidates) - len(selected_old)))
            if need > 0:
                selected_old.extend(due_old_candidates[len(selected_old) : len(selected_old) + need])
        if len(selected_old) < target_old:
            need = min(3 - len(selected_new) - len(selected_old), max(0, len(new_candidates) - len(selected_new)))
            if need > 0:
                selected_new.extend(new_candidates[len(selected_new) : len(selected_new) + need])

        selected_new_count = len(selected_new)
        selected_old_count = len(selected_old)
        ratio_parts.append(f"今天实际安排为 {selected_new_count} : {selected_old_count}。")
        if len(new_candidates) < target_new:
            ratio_parts.append(f"新知识点候选不足：当前仅有 {len(new_candidates)} 个未进入复习记录的候选。")
        if len(due_old_candidates) < target_old:
            ratio_parts.append(f"旧知识点候选不足：当前仅有 {len(due_old_candidates)} 个已到期候选。")
        if len(new_candidates) >= 10:
            ratio_parts.append("未复习新笔记较多，但今天仍按默认 3 个知识点执行，避免单日负担过重。")

        rows = []
        for note in selected_new:
            card_path, knowledge_point, created = create_card_file(
                out_dir=out_dir,
                source_note=note.path,
                source_added_at=note.added_at,
                new_or_old="new",
                review_round=0,
                interval_days=0,
                previous_state=None,
                preferred_label=None,
            )
            if created:
                created_card_count += 1
            reason = build_new_reason(note)
            reasons_by_path[card_path] = reason
            rows.append(
                {
                    "type": "new",
                    "knowledge_point": knowledge_point,
                    "source_added_at": note.added_at,
                    "reason": reason,
                    "status": "pending",
                    "path": card_path,
                }
            )

        for state in selected_old:
            card_path, knowledge_point, created = create_card_file(
                out_dir=out_dir,
                source_note=state.source_note,
                source_added_at=state.source_added_at,
                new_or_old="old",
                review_round=state.review_round + 1,
                interval_days=state.interval_days,
                previous_state=state,
                preferred_label=state.label,
            )
            if created:
                created_card_count += 1
            reason = build_old_reason(state)
            reasons_by_path[card_path] = reason
            rows.append(
                {
                    "type": "old",
                    "knowledge_point": knowledge_point,
                    "source_added_at": state.source_added_at,
                    "reason": reason,
                    "status": "pending",
                    "path": card_path,
                }
            )

    checklist_path.write_text(render_checklist(rows, ratio_parts, updated_records, pending_records), encoding="utf-8")

    ratio_ok = selected_new_count == 2 and selected_old_count == 1
    print(f"SCANNED_NOTES={len(source_notes)}")
    print(f"NEW_CANDIDATES={len(new_candidates)}")
    print(f"DUE_OLD={len(due_old_candidates)}")
    print(f"SELECTED_NEW={selected_new_count}")
    print(f"SELECTED_OLD={selected_old_count}")
    print(f"CREATED_FILES={created_card_count + 1}")
    print(f"UPDATED_PENDING={len(updated_records)}")
    print(f"RATIO_OK={'yes' if ratio_ok else 'no'}")


if __name__ == "__main__":
    main()
