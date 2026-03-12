#!/usr/bin/env python3
"""Generate W05 task-closure markdown logs.

Main interfaces:
- `build_parser()`: declare the CLI contract.
- `generate_markdown()`: render the task log body.
- `write_task_log()`: persist the markdown into `agent-task-log/ongoing/`.

Quick start:
`python global/agent-workflow/w05-task-closure/scripts/generate_task_log.py --help`
"""

from __future__ import annotations

import argparse
import logging
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Iterable, Sequence


LOGGER = logging.getLogger("generate_task_log")
DIMENSION_ORDER = [
    "代码质量",
    "架构设计",
    "性能",
    "测试",
    "可维护性",
    "技术债务",
]


@dataclass(frozen=True)
class DimensionEntry:
    """Represents one optimization-review dimension."""

    name: str
    highlight: str
    suggestion: str
    priority: str


def configure_logging() -> None:
    """Configure a minimal logger for CLI output."""

    logging.basicConfig(level=logging.INFO, format="%(message)s")


def build_parser() -> argparse.ArgumentParser:
    """Create the CLI parser for task-log generation."""

    parser = argparse.ArgumentParser(
        description="生成符合 W05 规范的任务日志与六维度优化分析。"
    )
    parser.add_argument("--task-type", required=True, help="任务类型，例如 skill-doc。")
    parser.add_argument("--task-name", required=True, help="任务名称，不含文档类型后缀。")
    parser.add_argument(
        "--trigger", required=True, help="触发方式说明，例如：用户主动触发。"
    )
    parser.add_argument(
        "--issue",
        default="N/A（本次未绑定 GitHub Issue）",
        help="相关 Issue 信息，默认写为未绑定。",
    )
    parser.add_argument(
        "--date",
        dest="run_date",
        default=date.today().isoformat(),
        help="执行日期，格式 YYYY-MM-DD，默认今天。",
    )
    parser.add_argument(
        "--doc-type", default="任务日志", help="文档类型，默认“任务日志”。"
    )
    parser.add_argument(
        "--output-dir",
        default="agent-task-log/ongoing",
        help="输出目录，默认 agent-task-log/ongoing。",
    )
    parser.add_argument(
        "--file",
        action="append",
        default=[],
        help="相关文件，可重复传入。",
    )
    parser.add_argument(
        "--w00",
        action="append",
        default=[],
        help="W00 同步与收口说明，可重复传入。",
    )
    parser.add_argument(
        "--structure",
        action="append",
        default=[],
        help="结构检查说明，可重复传入。",
    )
    parser.add_argument(
        "--step",
        action="append",
        default=[],
        help="关键步骤，可重复传入。",
    )
    parser.add_argument(
        "--implementation",
        action="append",
        default=[],
        help="实施说明，可重复传入。",
    )
    parser.add_argument(
        "--test",
        action="append",
        default=[],
        help="测试与校验结果，可重复传入。",
    )
    parser.add_argument(
        "--conclusion",
        action="append",
        default=[],
        help="交付结论，可重复传入。",
    )
    parser.add_argument(
        "--residual",
        action="append",
        default=[],
        help="遗留与后续计划，可重复传入。",
    )
    parser.add_argument(
        "--priority",
        action="append",
        default=[],
        help="优先级汇总项，可重复传入。",
    )
    parser.add_argument(
        "--dimension",
        action="append",
        default=[],
        metavar="NAME|HIGHLIGHT|SUGGESTION|PRIORITY",
        help="六维度分析项，使用 | 分隔，可重复传入。",
    )
    return parser


def sanitize_filename(value: str) -> str:
    """Return a filesystem-safe filename fragment."""

    cleaned = re.sub(r'[\\/:*?"<>|]+', "-", value).strip()
    return cleaned.rstrip(".") or "task-log"


def next_index(output_dir: Path, run_date: str) -> int:
    """Compute the next daily index under the output directory."""

    pattern = f"{run_date}-*_*.md"
    indexes: list[int] = []
    for path in output_dir.glob(pattern):
        match = re.match(rf"{re.escape(run_date)}-(\d+)_", path.name)
        if match:
            indexes.append(int(match.group(1)))
    return max(indexes, default=0) + 1


def parse_dimensions(raw_dimensions: Sequence[str]) -> list[DimensionEntry]:
    """Parse `--dimension` values into typed entries."""

    parsed: list[DimensionEntry] = []
    for raw in raw_dimensions:
        parts = [part.strip() for part in raw.split("|")]
        if len(parts) != 4 or any(not part for part in parts):
            raise ValueError(
                "--dimension 必须使用 NAME|HIGHLIGHT|SUGGESTION|PRIORITY 格式。"
            )
        parsed.append(DimensionEntry(*parts))
    return sorted(
        parsed,
        key=lambda item: DIMENSION_ORDER.index(item.name)
        if item.name in DIMENSION_ORDER
        else len(DIMENSION_ORDER),
    )


def ensure_required_sections(args: argparse.Namespace) -> None:
    """Validate required sections before rendering the markdown."""

    required_lists = {
        "--structure": args.structure,
        "--step": args.step,
        "--implementation": args.implementation,
        "--test": args.test,
        "--conclusion": args.conclusion,
        "--priority": args.priority,
        "--dimension": args.dimension,
    }
    missing = [flag for flag, values in required_lists.items() if not values]
    if missing:
        joined = ", ".join(missing)
        raise ValueError(f"缺少必填段落参数：{joined}")


def bullet_lines(items: Iterable[str]) -> list[str]:
    """Render bullet items with a shared markdown format."""

    return [f"- {item}" for item in items]


def numbered_lines(items: Sequence[str]) -> list[str]:
    """Render numbered items using markdown ordered-list syntax."""

    return [f"{index}. {item}" for index, item in enumerate(items, start=1)]


def generate_markdown(
    args: argparse.Namespace, output_path: Path, dimensions: Sequence[DimensionEntry]
) -> str:
    """Render the task-log markdown content."""

    related_files = list(args.file)
    related_files.append(str(output_path))
    lines: list[str] = [
        f"# {args.run_date} 【{args.task_type}】{args.task_name}-{args.doc_type}",
        "",
        "## 元信息",
        "",
        f"- 任务类型：{args.task_type}",
        f"- 触发方式：{args.trigger}",
        f"- 执行日期：{args.run_date}",
        f"- 相关 Issue：{args.issue}",
        "- 相关文件：",
    ]
    lines.extend([f"  - `{path}`" for path in related_files])
    lines.extend(["", "## W00 同步与收口", ""])
    lines.extend(bullet_lines(args.w00 or ["未绑定 Issue：本次通过任务日志与 Git 变更作为替代追踪方式。"]))
    lines.extend(["", "## 结构检查（先检查再收尾）", ""])
    lines.extend(bullet_lines(args.structure))
    lines.extend(["", "## 关键步骤", ""])
    lines.extend(numbered_lines(args.step))
    lines.extend(["", "## 实施说明", ""])
    lines.extend(bullet_lines(args.implementation))
    lines.extend(["", "## 测试与校验结果", ""])
    lines.extend(bullet_lines(args.test))
    lines.extend(["", "## 交付结论", ""])
    lines.extend(bullet_lines(args.conclusion))
    lines.extend(["", "## 六维度优化分析", ""])
    for index, entry in enumerate(dimensions, start=1):
        suggestion = entry.suggestion.rstrip("；;。 ")
        lines.extend(
            [
                f"### {index}) {entry.name}",
                "",
                f"- ✅ 亮点：{entry.highlight}",
                f"- ⚠️ 建议：{suggestion}；优先级：{entry.priority}。",
                "",
            ]
        )
    lines.extend(["## 优先级汇总", ""])
    lines.extend(bullet_lines(args.priority))
    if args.residual:
        lines.extend(["", "## 遗留与后续计划", ""])
        lines.extend(bullet_lines(args.residual))
    return "\n".join(lines).rstrip() + "\n"


def write_task_log(output_path: Path, content: str) -> None:
    """Write the rendered markdown to disk."""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")


def main() -> int:
    """Parse arguments, render markdown, and persist the task log."""

    configure_logging()
    parser = build_parser()
    args = parser.parse_args()
    ensure_required_sections(args)
    dimensions = parse_dimensions(args.dimension)
    output_dir = Path(args.output_dir)
    file_index = next_index(output_dir, args.run_date)
    safe_name = sanitize_filename(args.task_name)
    safe_doc_type = sanitize_filename(args.doc_type)
    filename = f"{args.run_date}-{file_index}_【{args.task_type}】{safe_name}-{safe_doc_type}.md"
    output_path = output_dir / filename
    content = generate_markdown(args, output_path, dimensions)
    write_task_log(output_path, content)
    LOGGER.info("任务日志已生成：%s", output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
