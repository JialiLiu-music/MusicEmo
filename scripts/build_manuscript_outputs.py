from __future__ import annotations

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MD = ROOT / "manuscript_en.md"
OUT_HTML = ROOT / "manuscript_en.html"
OUT_DOCX = ROOT / "manuscript_en.docx"


def inline_html(text: str) -> str:
    text = html.escape(text, quote=False)
    text = re.sub(r"!\[([^]]*)\]\(([^)]+)\)", r'<figure><img src="\2" alt="\1"><figcaption>\1</figcaption></figure>', text)
    text = re.sub(r"\[([^]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", text)
    return text


def parse_table(lines: list[str], start: int):
    header = [c.strip() for c in lines[start].strip().strip("|").split("|")]
    rows = []
    i = start + 2
    while i < len(lines) and lines[i].strip().startswith("|"):
        rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
        i += 1
    return header, rows, i


def markdown_to_html(text: str) -> str:
    lines = text.splitlines()
    out: list[str] = []
    i = 0
    paragraph: list[str] = []
    def flush():
        if paragraph:
            out.append("<p>" + inline_html(" ".join(paragraph)) + "</p>")
            paragraph.clear()
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            flush(); i += 1; continue
        if line.startswith("# "):
            flush(); out.append(f"<h1>{inline_html(line[2:])}</h1>"); i += 1; continue
        if line.startswith("## "):
            flush(); out.append(f"<h2>{inline_html(line[3:])}</h2>"); i += 1; continue
        if line.startswith("### "):
            flush(); out.append(f"<h3>{inline_html(line[4:])}</h3>"); i += 1; continue
        if line.startswith("!["):
            flush(); out.append(inline_html(line)); i += 1; continue
        if line.startswith("**Figure"):
            flush(); out.append(f"<p class=caption>{inline_html(line)}</p>"); i += 1; continue
        if line.startswith("**Table"):
            flush(); out.append(f"<p class=caption>{inline_html(line)}</p>"); i += 1; continue
        if line.startswith("\\["):
            flush(); eq = []
            while i < len(lines):
                eq.append(lines[i])
                if lines[i].strip() == "\\]":
                    i += 1; break
                i += 1
            out.append('<div class="equation"><pre>' + html.escape("\n".join(eq)) + '</pre></div>')
            continue
        if line.startswith("|") and i + 1 < len(lines) and lines[i+1].strip().startswith("|"):
            flush(); header, rows, i = parse_table(lines, i)
            out.append("<table><thead><tr>" + "".join(f"<th>{inline_html(c)}</th>" for c in header) + "</tr></thead><tbody>")
            for row in rows:
                out.append("<tr>" + "".join(f"<td>{inline_html(c)}</td>" for c in row) + "</tr>")
            out.append("</tbody></table>")
            continue
        if line.startswith("-"):
            flush(); items = []
            while i < len(lines) and lines[i].startswith("-"):
                items.append("<li>" + inline_html(lines[i][1:].strip()) + "</li>"); i += 1
            out.append("<ul>" + "".join(items) + "</ul>"); continue
        paragraph.append(line.strip()); i += 1
    flush()
    return "\n".join(out)


def add_markdown_to_docx(doc, text: str):
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.shared import Inches, Pt
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    lines = text.splitlines(); i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip(): i += 1; continue
        if line.startswith("# "):
            p = doc.add_heading(line[2:], level=1); p.alignment = WD_ALIGN_PARAGRAPH.CENTER; i += 1; continue
        if line.startswith("## "):
            doc.add_heading(line[3:], level=2); i += 1; continue
        if line.startswith("### "):
            doc.add_heading(line[4:], level=3); i += 1; continue
        if line.startswith("!["):
            m = re.match(r"!\[[^]]*\]\(([^)]+)\)", line)
            if m:
                image = (ROOT / m.group(1)).resolve()
                if image.exists():
                    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    p.add_run().add_picture(str(image), width=Inches(6.5))
            i += 1; continue
        if line.startswith("**Figure") or line.startswith("**Table"):
            p = doc.add_paragraph(line.replace("**", "")); p.style = doc.styles["Caption"]; i += 1; continue
        if line.startswith("\\["):
            eq = []
            while i < len(lines):
                eq.append(lines[i]);
                if lines[i].strip() == "\\]": i += 1; break
                i += 1
            p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = p.add_run("\n".join(eq)); run.font.name = "Cambria Math"; run.font.size = Pt(10); i += 0
            continue
        if line.startswith("|") and i + 1 < len(lines) and lines[i+1].strip().startswith("|"):
            header, rows, i = parse_table(lines, i)
            table = doc.add_table(rows=1, cols=len(header)); table.style = "Table Grid"
            for j, c in enumerate(header): table.rows[0].cells[j].text = c
            for row in rows:
                cells = table.add_row().cells
                for j, c in enumerate(row):
                    if j < len(cells): cells[j].text = c
            continue
        if line.startswith("-"):
            p = doc.add_paragraph(line[1:].strip(), style="List Bullet"); i += 1; continue
        p = doc.add_paragraph()
        # Remove lightweight markdown markers for readable DOCX output.
        clean = re.sub(r"\*\*([^*]+)\*\*", r"\1", line)
        clean = re.sub(r"`([^`]+)`", r"\1", clean)
        p.add_run(clean); i += 1


def main():
    text = MD.read_text(encoding="utf-8")
    body = markdown_to_html(text)
    style = """
    body{font-family:Georgia,'Times New Roman',serif;max-width:900px;margin:40px auto;line-height:1.65;color:#202124}
    h1{text-align:center;font-size:2em;line-height:1.2;margin-bottom:1.4em} h2{margin-top:2em;border-bottom:1px solid #bbb;padding-bottom:.2em} h3{margin-top:1.4em}
    table{border-collapse:collapse;width:100%;margin:1em 0;font-size:.92em} th,td{border:1px solid #aaa;padding:6px 8px;vertical-align:top} th{background:#f1f3f4}
    figure{text-align:center;margin:1.3em 0} figure img{max-width:100%;height:auto} figcaption,.caption{font-size:.9em;color:#4b5563} .equation{overflow:auto;text-align:center;margin:1em 0} .equation pre{display:inline-block;text-align:left;font-family:'Cambria Math',serif;font-size:1em} code{font-family:Consolas,monospace}
    """
    OUT_HTML.write_text("<!doctype html><html><head><meta charset='utf-8'><title>Low-Label Output Calibration</title><style>" + style + "</style></head><body>" + body + "</body></html>", encoding="utf-8")
    from docx import Document
    from docx.shared import Inches, Pt
    doc = Document()
    sec = doc.sections[0]; sec.top_margin = Inches(.7); sec.bottom_margin = Inches(.7); sec.left_margin = Inches(.8); sec.right_margin = Inches(.8)
    normal = doc.styles["Normal"]; normal.font.name = "Times New Roman"; normal.font.size = Pt(10.5)
    for name in ["Heading 1", "Heading 2", "Heading 3"]:
        doc.styles[name].font.name = "Times New Roman"
    add_markdown_to_docx(doc, text)
    doc.save(OUT_DOCX)
    print(json.dumps({"html": str(OUT_HTML), "docx": str(OUT_DOCX), "markdown_lines": len(text.splitlines())}, ensure_ascii=False, indent=2))

if __name__ == "__main__": main()
