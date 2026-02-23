#!/usr/bin/env python3
"""
Converts content.md to index.html using only Python standard library.
No external packages required.
"""

import re
from datetime import date
from pathlib import Path


def md_to_html(text: str) -> str:
    """Convert basic Markdown to HTML."""
    lines = text.split("\n")
    result = []
    i = 0

    def parse_inline(s: str) -> str:
        """Parse inline Markdown: **bold**, *italic*, [text](url)."""
        s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
        s = re.sub(r"\*(.+?)\*", r"<em>\1</em>", s)
        s = re.sub(r"\[(.+?)\]\((.+?)\)", r'<a href="\2" target="_blank" rel="noopener noreferrer">\1</a>', s)
        return s

    while i < len(lines):
        line = lines[i]

        # Headers
        if match := re.match(r"^(#{1,6})\s+(.+)$", line):
            level = len(match.group(1))
            content = parse_inline(match.group(2))
            result.append(f"<h{level}>{content}</h{level}>")
            i += 1
            continue

        # Unordered list
        if re.match(r"^[-*]\s+", line):
            result.append("<ul>")
            while i < len(lines) and re.match(r"^[-*]\s+", lines[i]):
                content = parse_inline(re.sub(r"^[-*]\s+", "", lines[i]))
                result.append(f"<li>{content}</li>")
                i += 1
            result.append("</ul>")
            continue

        # Ordered list
        if re.match(r"^\d+\.\s+", line):
            result.append("<ol>")
            while i < len(lines) and re.match(r"^\d+\.\s+", lines[i]):
                content = parse_inline(re.sub(r"^\d+\.\s+", "", lines[i]))
                result.append(f"<li>{content}</li>")
                i += 1
            result.append("</ol>")
            continue

        # Empty line
        if not line.strip():
            i += 1
            continue

        # Paragraph
        result.append(f"<p>{parse_inline(line)}</p>")
        i += 1

    return "\n".join(result)


def main() -> None:
    base = Path(__file__).resolve().parent
    content_path = base / "content.md"
    output_path = base / "index.html"

    content = content_path.read_text(encoding="utf-8")
    content = re.sub(r"\n---\s*\naktualisiert am \d{2}\.\d{2}\.\d{4}\s*$", "", content)
    today = date.today().strftime("%d.%m.%Y")
    content = content.rstrip() + f"\n\n---\naktualisiert am {today}"
    body_html = md_to_html(content)

    html = f"""<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="Alexej Antropov – 20+ im Internet. Interim Product Manager, Dozent Business Innovation, Erfinder KI-Radar für Produktentwicklung, Co-Author Agile Product Manifesto.">
<title>Alexej Antropov | Digital Products &amp; Transformation</title>
<style>main{{max-width:1337px;margin:0 auto}}</style>
</head>
<body>
<main role="main">
{body_html}
</main>
</body>
</html>
"""

    output_path.write_text(html, encoding="utf-8")
    print(f"Generated {output_path}")


if __name__ == "__main__":
    main()
