from __future__ import annotations

import html
import re


def parse_markdown(content: str) -> tuple[str, list[dict[str, object]]]:
    sections: list[dict[str, object]] = []
    current_title = "Introduction"
    current_lines: list[str] = []
    for line in content.splitlines():
        if line.startswith("#"):
            if current_lines:
                sections.append({"title": current_title, "content": "\n".join(current_lines).strip()})
                current_lines = []
            current_title = line.lstrip("#").strip() or current_title
        else:
            current_lines.append(line)
    if current_lines or not sections:
        sections.append({"title": current_title, "content": "\n".join(current_lines).strip()})
    plain = re.sub(r"[#*_>`\-\[\]()]", " ", content)
    return re.sub(r"\s+", " ", plain).strip(), sections


def parse_html(content: str) -> tuple[str, list[dict[str, object]]]:
    text = html.unescape(re.sub(r"<[^>]+>", " ", content))
    text = re.sub(r"\s+", " ", text).strip()
    sections = [{"title": "Body", "content": text}] if text else []
    return text, sections


def parse_txt(content: str) -> tuple[str, list[dict[str, object]]]:
    paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]
    sections = [{"title": f"Section {i + 1}", "content": p} for i, p in enumerate(paragraphs)] or [{"title": "Body", "content": content.strip()}]
    return content.strip(), sections


def parse_pdf(content: str) -> tuple[str, list[dict[str, object]]]:
    text = re.sub(r"[^\x20-\x7EÀ-ÿ\n\r\t]", " ", content)
    text = re.sub(r"\s+", " ", text).strip()
    return text, [{"title": "Extracted PDF", "content": text}] if text else []


def parse_docx(content: str) -> tuple[str, list[dict[str, object]]]:
    text = re.sub(r"<[^>]+>", " ", content)
    text = re.sub(r"\s+", " ", text).strip()
    return text, [{"title": "Extracted DOCX", "content": text}] if text else []


def parse_document(format_name: str, content: str) -> tuple[str, list[dict[str, object]]]:
    fmt = format_name.lower()
    if fmt == "markdown":
        return parse_markdown(content)
    if fmt == "html":
        return parse_html(content)
    if fmt == "txt":
        return parse_txt(content)
    if fmt == "pdf":
        return parse_pdf(content)
    if fmt == "docx":
        return parse_docx(content)
    return parse_txt(content)
