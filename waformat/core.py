"""Markdown <-> WhatsApp formatting conversion.

WhatsApp supports *bold*, _italic_, ~strikethrough~, and ```monospace```.
It does not support headings, links with labels, tables, or single backtick
code. Pasting raw Markdown (for example AI chat output) into WhatsApp shows
the ** and ## literally. This module converts both ways.
"""
import re

PLACEHOLDER = "\x00{}\x00"


def _inline_md_to_wa(line):
    stash = []

    def keep(final):
        stash.append(final)
        return PLACEHOLDER.format(len(stash) - 1)

    line = re.sub(r"```([^`]+)```", lambda m: keep(m.group(0)), line)
    line = re.sub(r"`([^`\n]+)`", lambda m: keep(f"```{m.group(1)}```"), line)
    line = re.sub(r"\*\*\*(.+?)\*\*\*", lambda m: keep(f"*_{m.group(1)}_*"), line, flags=re.S)
    line = re.sub(r"___(.+?)___", lambda m: keep(f"*_{m.group(1)}_*"), line, flags=re.S)
    line = re.sub(r"\*\*(.+?)\*\*", lambda m: keep(f"*{m.group(1)}*"), line, flags=re.S)
    line = re.sub(r"__(.+?)__", lambda m: keep(f"*{m.group(1)}*"), line, flags=re.S)
    line = re.sub(r"(?<![\w*])\*([^*\n]+?)\*(?![\w*])", r"_\1_", line)
    line = re.sub(r"~~(.+?)~~", r"~\1~", line, flags=re.S)
    line = re.sub(r"\[([^\]]+)\]\(([^)]+)\)",
                  lambda m: m.group(1) if m.group(1) == m.group(2)
                  else f"{m.group(1)} ({m.group(2)})", line)
    for idx, final in enumerate(stash):
        line = line.replace(PLACEHOLDER.format(idx), final)
    return line


def _convert_table(lines):
    out = []
    for line in lines:
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if cells and all(set(c) <= set("-: ") for c in cells):
            continue
        out.append(_inline_md_to_wa(" • ".join(cells)))
    return out


def md_to_wa(text):
    lines = text.replace("\r\n", "\n").split("\n")
    out = []
    in_fence = False
    table_buffer = []

    def flush_table():
        if table_buffer:
            out.extend(_convert_table(table_buffer))
            table_buffer.clear()

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("```"):
            flush_table()
            in_fence = not in_fence
            out.append(line)
            continue
        if in_fence:
            out.append(line)
            continue
        if stripped.startswith("|") and stripped.endswith("|"):
            table_buffer.append(line)
            continue
        flush_table()
        heading = re.match(r"^#{1,6}\s+(.*)$", stripped)
        if heading:
            out.append("*" + _inline_md_to_wa(heading.group(1).strip()).strip("*") + "*")
            continue
        if re.match(r"^\s*[-*_]{3,}\s*$", stripped):
            out.append("----------")
            continue
        line = re.sub(r"^\s*[-*+]\s+", "• ", line)
        line = re.sub(r"^>\s?", "» ", line)
        out.append(_inline_md_to_wa(line))
    flush_table()
    return "\n".join(out)


def wa_to_md(text):
    result = text.replace("\r\n", "\n")
    result = re.sub(r"\*_([^_]+?)_\*", r"***\1***", result)
    result = re.sub(r"(?<![\w*])\*([^*\n]+?)\*(?![\w*])", r"**\1**", result)
    result = re.sub(r"(?<![\w_])_([^_\n]+?)_(?![\w_])", r"*\1*", result)
    result = re.sub(r"(?<![\w~])~([^~\n]+?)~(?![\w~])", r"~~\1~~", result)
    result = re.sub(r"^•\s+", "- ", result, flags=re.M)
    return result
