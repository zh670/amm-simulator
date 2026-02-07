import argparse
import csv
import datetime as dt
import json
import os
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable, List, Dict, Optional

DATA_ENV = "TIME_MANAGER_DATA"
DEFAULT_DATA_PATH = Path.home() / ".amm_time_manager" / "data.json"
DATE_FORMAT = "%Y-%m-%d"


@dataclass
class TimeEntry:
    timestamp: str
    activity: str
    duration_minutes: int
    note: str = ""


@dataclass
class BrainstormPrompt:
    timestamp: str
    topic: str
    thoughts: str


def ensure_storage(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        payload = {"entries": [], "brainstorms": []}
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2))


def load_storage(path: Path) -> Dict[str, List[Dict[str, str]]]:
    ensure_storage(path)
    return json.loads(path.read_text(encoding="utf-8"))


def save_storage(path: Path, payload: Dict[str, List[Dict[str, str]]]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2))


def parse_duration(value: str) -> int:
    """Parse duration like '90', '90m', '1.5h', '2h30m'."""
    value = value.strip().lower()
    if re.fullmatch(r"\d+", value):
        return int(value)
    hours = 0
    minutes = 0
    hour_match = re.search(r"(\d+(?:\.\d+)?)h", value)
    minute_match = re.search(r"(\d+)m", value)
    if hour_match:
        hours = float(hour_match.group(1))
    if minute_match:
        minutes = int(minute_match.group(1))
    if hours == 0 and minutes == 0:
        raise ValueError(f"Unable to parse duration: {value}")
    return int(hours * 60 + minutes)


def parse_voice_or_text_input(text: str) -> TimeEntry:
    """Parse text like 'Writing report for 45m note: status update'."""
    note = ""
    if "note:" in text:
        text, note = text.split("note:", 1)
        note = note.strip()
    duration_match = re.search(r"for\s+([^\s]+)", text)
    if not duration_match:
        raise ValueError("Input must include duration with 'for <duration>'.")
    duration = parse_duration(duration_match.group(1))
    activity = text[: duration_match.start()].strip()
    if not activity:
        raise ValueError("Activity cannot be empty.")
    timestamp = dt.datetime.now().isoformat(timespec="seconds")
    return TimeEntry(timestamp=timestamp, activity=activity, duration_minutes=duration, note=note)


def add_entry(path: Path, entry: TimeEntry) -> None:
    payload = load_storage(path)
    payload["entries"].append(asdict(entry))
    save_storage(path, payload)


def add_brainstorm(path: Path, prompt: BrainstormPrompt) -> None:
    payload = load_storage(path)
    payload["brainstorms"].append(asdict(prompt))
    save_storage(path, payload)


def iter_entries(payload: Dict[str, List[Dict[str, str]]]) -> Iterable[TimeEntry]:
    for item in payload.get("entries", []):
        yield TimeEntry(
            timestamp=item["timestamp"],
            activity=item["activity"],
            duration_minutes=int(item["duration_minutes"]),
            note=item.get("note", ""),
        )


def group_by_day(entries: Iterable[TimeEntry]) -> Dict[str, List[TimeEntry]]:
    grouped: Dict[str, List[TimeEntry]] = {}
    for entry in entries:
        day = entry.timestamp[:10]
        grouped.setdefault(day, []).append(entry)
    return grouped


def summarize_entries(entries: Iterable[TimeEntry]) -> Dict[str, int]:
    totals: Dict[str, int] = {}
    for entry in entries:
        totals[entry.activity] = totals.get(entry.activity, 0) + entry.duration_minutes
    return dict(sorted(totals.items(), key=lambda item: item[1], reverse=True))


def analyze_totals(totals: Dict[str, int]) -> List[str]:
    suggestions = []
    total_minutes = sum(totals.values())
    if total_minutes == 0:
        return ["No data to analyze yet. Start logging your time for insights."]
    top_activity = max(totals.items(), key=lambda item: item[1])
    if top_activity[1] > total_minutes * 0.6:
        suggestions.append(
            f"'{top_activity[0]}'占用了超过60%的时间，建议安排多样化任务或加入休息。"
        )
    if total_minutes > 600:
        suggestions.append("今日累计时间超过10小时，注意休息与恢复。")
    if len(totals) <= 2:
        suggestions.append("活动类型较少，可以记录更多类别以便分析平衡性。")
    if not suggestions:
        suggestions.append("时间分配较为均衡，继续保持并关注重点项目进展。")
    return suggestions


def build_report(title: str, entries: Iterable[TimeEntry]) -> str:
    totals = summarize_entries(entries)
    total_minutes = sum(totals.values())
    lines = [f"# {title}", "", f"总时长：{total_minutes} 分钟", "", "## 分类统计"]
    for activity, minutes in totals.items():
        lines.append(f"- {activity}: {minutes} 分钟")
    lines.append("\n## 分析与建议")
    lines.extend([f"- {tip}" for tip in analyze_totals(totals)])
    return "\n".join(lines)


def export_entries(path: Path, fmt: str, output: Path) -> None:
    payload = load_storage(path)
    entries = list(iter_entries(payload))
    if fmt == "json":
        output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        return
    if fmt == "csv":
        with output.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=["timestamp", "activity", "duration_minutes", "note"])
            writer.writeheader()
            for entry in entries:
                writer.writerow(asdict(entry))
        return
    if fmt == "markdown":
        report = build_report("全部记录汇总", entries)
        output.write_text(report, encoding="utf-8")
        return
    raise ValueError(f"Unsupported export format: {fmt}")


def filter_entries(entries: Iterable[TimeEntry], start: dt.date, end: dt.date) -> List[TimeEntry]:
    results = []
    for entry in entries:
        entry_date = dt.date.fromisoformat(entry.timestamp[:10])
        if start <= entry_date <= end:
            results.append(entry)
    return results


def parse_period(period: str, reference: Optional[dt.date] = None) -> tuple[dt.date, dt.date, str]:
    if reference is None:
        reference = dt.date.today()
    if period == "daily":
        start = reference
        end = reference
        title = f"{reference.isoformat()} 日报"
    elif period == "weekly":
        start = reference - dt.timedelta(days=reference.weekday())
        end = start + dt.timedelta(days=6)
        title = f"{start.isoformat()} 至 {end.isoformat()} 周报"
    elif period == "monthly":
        start = reference.replace(day=1)
        next_month = (start + dt.timedelta(days=32)).replace(day=1)
        end = next_month - dt.timedelta(days=1)
        title = f"{start.strftime('%Y-%m')} 月报"
    elif period == "yearly":
        start = reference.replace(month=1, day=1)
        end = reference.replace(month=12, day=31)
        title = f"{reference.year} 年报"
    else:
        raise ValueError("Period must be daily, weekly, monthly, or yearly")
    return start, end, title


def brainstorm(topic: str, thoughts: str) -> str:
    prompts = [
        f"目标拆解：把『{topic}』拆成3个更小的目标。",
        f"风险预演：有哪些可能阻碍『{topic}』的因素？",
        f"资源盘点：你已有的资源/支持有哪些？",
        f"下一步行动：24小时内可以完成的最小行动是什么？",
        f"灵感延展：从『{thoughts}』中延伸出新的视角或问题。",
    ]
    return "\n".join([f"- {prompt}" for prompt in prompts])


def maybe_use_speech_recognition() -> Optional[str]:
    try:
        import speech_recognition as sr
    except ImportError:
        return None
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("请说出你的记录内容...", file=sys.stderr)
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio, language="zh-CN")
    except sr.UnknownValueError:
        return None
    except sr.RequestError:
        return None


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="时间管理工具")
    parser.add_argument(
        "--data",
        type=Path,
        default=Path(os.environ.get(DATA_ENV, DEFAULT_DATA_PATH)),
        help="数据文件路径",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    log_parser = subparsers.add_parser("log", help="记录时间")
    log_parser.add_argument("text", nargs="?", help="活动描述，例如 '写周报 for 45m note: 完成总结' ")
    log_parser.add_argument("--voice", action="store_true", help="使用语音输入")

    report_parser = subparsers.add_parser("report", help="生成日报/周报/月报/年报")
    report_parser.add_argument("period", choices=["daily", "weekly", "monthly", "yearly"])
    report_parser.add_argument("--date", help="参考日期 YYYY-MM-DD")

    export_parser = subparsers.add_parser("export", help="导出记录")
    export_parser.add_argument("format", choices=["json", "csv", "markdown"])
    export_parser.add_argument("output", type=Path, help="导出文件路径")

    brain_parser = subparsers.add_parser("brainstorm", help="记录想法并获取发散建议")
    brain_parser.add_argument("topic", help="主题")
    brain_parser.add_argument("thoughts", help="当前想法")

    summary_parser = subparsers.add_parser("summary", help="今日统计")

    return parser


def handle_log(args: argparse.Namespace) -> None:
    text = args.text
    if args.voice:
        voice_text = maybe_use_speech_recognition()
        if not voice_text:
            raise RuntimeError("语音识别失败或不可用，请改用文本输入。")
        text = voice_text
    if not text:
        raise RuntimeError("必须提供记录内容或使用 --voice。")
    entry = parse_voice_or_text_input(text)
    add_entry(args.data, entry)
    print(f"已记录：{entry.activity} {entry.duration_minutes} 分钟")


def handle_summary(args: argparse.Namespace) -> None:
    payload = load_storage(args.data)
    entries = list(iter_entries(payload))
    today = dt.date.today().isoformat()
    todays = [entry for entry in entries if entry.timestamp.startswith(today)]
    if not todays:
        print("今天还没有记录。")
        return
    report = build_report(f"{today} 今日统计", todays)
    print(report)


def handle_report(args: argparse.Namespace) -> None:
    reference = dt.date.fromisoformat(args.date) if args.date else dt.date.today()
    start, end, title = parse_period(args.period, reference)
    payload = load_storage(args.data)
    entries = list(iter_entries(payload))
    selected = filter_entries(entries, start, end)
    report = build_report(title, selected)
    print(report)


def handle_export(args: argparse.Namespace) -> None:
    export_entries(args.data, args.format, args.output)
    print(f"已导出到 {args.output}")


def handle_brainstorm(args: argparse.Namespace) -> None:
    prompt = BrainstormPrompt(
        timestamp=dt.datetime.now().isoformat(timespec="seconds"),
        topic=args.topic,
        thoughts=args.thoughts,
    )
    add_brainstorm(args.data, prompt)
    suggestions = brainstorm(args.topic, args.thoughts)
    print("已记录想法。\n\n## 发散建议\n" + suggestions)


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    try:
        if args.command == "log":
            handle_log(args)
        elif args.command == "summary":
            handle_summary(args)
        elif args.command == "report":
            handle_report(args)
        elif args.command == "export":
            handle_export(args)
        elif args.command == "brainstorm":
            handle_brainstorm(args)
    except Exception as exc:  # noqa: BLE001
        print(f"错误：{exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
