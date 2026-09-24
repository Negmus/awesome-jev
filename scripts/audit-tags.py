#!/usr/bin/env python3
"""Cross-check entry tags against what the entry text actually says.

Two directions, treated differently because the rules differ:

  error   a tagged entry whose name and description never mention the agent it
          claims. Tags are optional, but a tag that is present has to be
          supported by the source — that is the rule in CONTRIBUTING.md.

  notice  an untagged entry that does name an agent. Not a failure: tags are
          optional, and naming an agent is not the same as targeting it. It is
          printed so a reviewer can look, and so the gap is visible.

What this cannot do is decide whether a project *targets* the agent it
mentions. "OpenCode Zen's free tier" is a gateway an entry routes through, not
the OpenCode agent — see issue #154. This is the cheap check that runs first;
anything it cannot settle stays a human decision.

Usage: python3 scripts/audit-tags.py [categories_dir]
"""
from __future__ import annotations

import pathlib
import re
import sys

# What an entry must mention for the agent tag to be supported.
# `multi` is a judgement about breadth, so no single name can confirm it.
SUPPORT = {
    "claude-code": r"claude[ -]?code",
    "pi":          r"\bpi\b",
    "codex":       r"\bcodex\b",
    "cursor":      r"\bcursor\b",
    "cline":       r"\bcline\b",
    "dsh":         r"deepseek[ -]?harness|\bdsh\b",
    "multi":       None,
}

ENTRY_RE = re.compile(r"^- \[([^\]]+)\]\(([^)]+)\)(?:\s*`\{([^}]*)\}`)?\s*-\s*(.+)$")


def parse_tags(raw: str) -> dict[str, str]:
    tags = {}
    for pair in (raw or "").split(","):
        key, _, value = pair.partition(":")
        if key.strip():
            tags[key.strip()] = value.strip()
    return tags


def audit(root: pathlib.Path) -> tuple[list, list]:
    unsupported, unnoticed = [], []

    for path in sorted(root.glob("*.md")):
        for line in path.read_text(encoding="utf-8").splitlines():
            match = ENTRY_RE.match(line)
            if not match:
                continue
            name, _url, raw, description = match.groups()
            agent = parse_tags(raw).get("agent")
            # The agent may be named in the entry title as well as the sentence.
            haystack = f"{name} {description}"

            if agent and SUPPORT.get(agent):
                if not re.search(SUPPORT[agent], haystack, re.I):
                    unsupported.append((name, agent, path.name))
            elif not agent:
                named = [
                    candidate
                    for candidate, pattern in SUPPORT.items()
                    if pattern and re.search(pattern, haystack, re.I)
                ]
                if named:
                    unnoticed.append((name, named, path.name))

    return unsupported, unnoticed



def check_no_rendered_badges(paths) -> int:
    """分类文件必须用源码标签 `{agent: x}`，不能写渲染后的 badge。

    渲染形式会让 ENTRY_RE 匹配失败：该条拿不到星数 badge，也不会进入
    「Find by coding agent」索引 —— 从 README 上看不出来，因为 markdown 照样
    渲染那张图片（2026-09-24 在 infra-sdks-integrations.md 找到 6 行这样的残骸）。
    """
    bad = 0
    for p in paths:
        for i, line in enumerate(open(p, encoding="utf-8"), 1):
            if line.startswith("- [") and "img.shields.io" in line:
                print(f"error: {p}:{i} 条目里写了渲染后的 badge，应改为 `{{agent: ...}}` / `{{type: ...}}`")
                bad += 1
    return bad

def main(argv: list[str]) -> int:
    root = pathlib.Path(argv[1] if len(argv) > 1 else "categories")
    if not root.is_dir():
        raise SystemExit(f"{root}: not a directory")

    rendered = check_no_rendered_badges(sorted(root.glob("*.md")))

    unsupported, unnoticed = audit(root)

    for name, named, filename in unnoticed:
        print(f"notice: {name} ({filename}) mentions {', '.join(named)} but carries no tag")

    for name, agent, filename in unsupported:
        print(f"error: {name} ({filename}) is tagged {agent}, which its text does not mention")

    if unsupported or rendered:
        if unsupported:
            print(f"\n{len(unsupported)} tag(s) unsupported by the entry text.")
        if rendered:
            print(f"{rendered} entry/badge line(s) rendered instead of tagged.")
        return 1

    print(f"tags check out ({len(unnoticed)} notice(s)).")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
