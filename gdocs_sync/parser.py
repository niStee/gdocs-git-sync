from typing import Any


def _element_to_text(elem: dict[str, Any]) -> str:
    text_run = elem.get("textRun")
    if not text_run:
        return ""

    content = text_run.get("content", "")
    style = text_run.get("textStyle", {})

    is_bold = style.get("bold", False)
    is_italic = style.get("italic", False)
    link = style.get("link", {}).get("url")

    text = content
    # Preserve trailing newlines outside formatting
    trailing_newlines = ""
    while text.endswith("\n"):
        trailing_newlines += "\n"
        text = text[:-1]

    if not text:
        return trailing_newlines

    if is_bold and is_italic:
        text = f"***{text}***"
    elif is_bold:
        text = f"**{text}**"
    elif is_italic:
        text = f"*{text}*"

    if link:
        text = f"[{text}]({link})"

    return text + trailing_newlines


def doc_to_markdown(doc: dict[str, Any]) -> str:
    body = doc.get("body", {})
    content = body.get("content", [])

    lines: list[str] = []

    for item in content:
        para = item.get("paragraph")
        if not para:
            continue

        style_type = para.get("paragraphStyle", {}).get("namedStyleType", "NORMAL_TEXT")
        is_bullet = "bullet" in para

        para_text = ""
        for elem in para.get("elements", []):
            para_text += _element_to_text(elem)

        clean_text = para_text.rstrip("\n")

        if not clean_text.strip():
            lines.append("")
            continue

        if style_type == "HEADING_1":
            lines.append(f"# {clean_text}")
        elif style_type == "HEADING_2":
            lines.append(f"## {clean_text}")
        elif style_type == "HEADING_3" or style_type == "HEADING_4":
            lines.append(f"### {clean_text}")
        elif style_type == "TITLE":
            lines.append(f"# {clean_text}")
        elif style_type == "SUBTITLE":
            lines.append(f"> {clean_text}")
        elif is_bullet:
            lines.append(f"- {clean_text}")
        else:
            lines.append(clean_text)

    # Normalize multiple blank lines
    md_output = "\n".join(lines).strip() + "\n"
    return md_output
