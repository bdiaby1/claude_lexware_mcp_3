#!/usr/bin/env python3
"""Convert Benjamin's table-format script .docx files to linear markdown.

The scripts are 3-column Word tables (time / Skript / Shots). This walks the
document XML directly so every word survives verbatim — no manual retyping.

Usage: python3 docx_table_script_to_md.py script.docx > script.md
"""
import sys
import zipfile
import xml.etree.ElementTree as ET

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def _flag_on(rpr, tag):
    el = rpr.find(W + tag) if rpr is not None else None
    if el is None:
        return False
    val = el.get(W + "val")
    return val not in ("false", "0", "none")


def run_text(run):
    parts = []
    for child in run:
        if child.tag == W + "t":
            parts.append(child.text or "")
        elif child.tag in (W + "br", W + "cr"):
            parts.append("\n")
        elif child.tag == W + "tab":
            parts.append("\t")
    return "".join(parts)


def para_md(p):
    """One paragraph -> markdown string, merging adjacent same-format runs."""
    pieces = []  # (bold, italic, text)
    for run in p.findall(W + "r"):
        rpr = run.find(W + "rPr")
        bold = _flag_on(rpr, "b")
        ital = _flag_on(rpr, "i")
        text = run_text(run)
        if not text:
            continue
        if pieces and pieces[-1][0] == bold and pieces[-1][1] == ital:
            pieces[-1] = (bold, ital, pieces[-1][2] + text)
        else:
            pieces.append([bold, ital, text])
    out = []
    for bold, ital, text in pieces:
        # markers must hug non-space chars; keep leading/trailing spaces outside
        stripped = text.strip()
        if not stripped:
            out.append(text)
            continue
        lead = text[: len(text) - len(text.lstrip())]
        trail = text[len(text.rstrip()):]
        if bold and ital:
            stripped = f"**_{stripped}_**"
        elif bold:
            stripped = f"**{stripped}**"
        elif ital:
            stripped = f"_{stripped}_"
        out.append(lead + stripped + trail)
    return "".join(out)


def cell_paras(tc):
    return [para_md(p) for p in tc.findall(W + "p")]


def cell_plain(tc):
    return " ".join(
        run_text(r) for p in tc.findall(W + "p") for r in p.findall(W + "r")
    ).strip()


def cell_all_bold(tc):
    runs = [r for p in tc.findall(W + "p") for r in p.findall(W + "r")
            if run_text(r).strip()]
    return bool(runs) and all(_flag_on(r.find(W + "rPr"), "b") for r in runs)


def convert(path):
    with zipfile.ZipFile(path) as z:
        root = ET.fromstring(z.read("word/document.xml"))
    body = root.find(W + "body")
    lines = []
    for el in body:
        if el.tag == W + "p":
            md = para_md(el)
            if md.strip():
                lines.append(md)
                lines.append("")
        elif el.tag == W + "tbl":
            for row in el.findall(W + "tr"):
                cells = row.findall(W + "tc")
                if len(cells) != 3:
                    continue
                t, script, shots = cells
                t_txt = cell_plain(t)
                script_txt = cell_plain(script)
                shots_txt = cell_plain(shots)
                if {t_txt, script_txt} == {"🕒", "Skript"} or script_txt == "Skript":
                    continue  # header row
                if script_txt and not shots_txt and cell_all_bold(script):
                    lines.append(f"## {script_txt}")
                    lines.append("")
                    continue
                stamp = f"**[{t_txt}]** " if t_txt else ""
                paras = [p for p in cell_paras(script) if p.strip()]
                if paras:
                    lines.append(stamp + paras[0])
                    lines.extend(paras[1:])
                elif stamp:
                    lines.append(stamp.strip())
                if shots_txt:
                    lines.append("> 🎬 " + " ".join(
                        p for p in cell_paras(shots) if p.strip()))
                lines.append("")
    return "\n".join(lines).rstrip() + "\n"


if __name__ == "__main__":
    sys.stdout.write(convert(sys.argv[1]))
