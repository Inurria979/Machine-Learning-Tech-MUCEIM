"""Build report.pdf from lean_network_challenge.md (no pandoc/LaTeX needed).

Usage (from the repo root):
    .venv\\Scripts\\python.exe report\\build.py

Step 1: converts the markdown source to report/report.html with a tiny converter.
Step 2: prints the HTML to report/report.pdf with headless Microsoft Edge.
The placeholder [MAIN COLAB LINK] is left in the .md until the link is known.
"""
import html, re, subprocess, sys, pathlib

HERE = pathlib.Path(__file__).resolve().parent
SRC = HERE / "lean_network_challenge.md"
HTML = HERE / "report.html"
PDF = HERE / "report.pdf"
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

CSS = """
/* Style modelled on the lab handout: Carlito/Calibri body, Caladea/Cambria title, blue accent #0563C1,
   light-grey table headers (#EAEEF2), pale boxes (#F6F8FA), thin grey rules (#D0D7DE), page counter footer. */
@page { size: A4; margin: 17mm 18mm 18mm 18mm;
  @bottom-right { content: "Page " counter(page) " of " counter(pages); font: 8pt Carlito, Calibri, sans-serif; color: #595959; } }
body { font-family: Carlito, Calibri, 'Segoe UI', sans-serif; font-size: 10.2pt; line-height: 1.34; color: #212121; }
.course { font-size: 10.5pt; font-weight: bold; color: #0563C1; margin: 0 0 4px; }
.title { font-family: Caladea, Cambria, Georgia, serif; font-size: 20pt; font-weight: bold; line-height: 1.15;
  color: #212121; margin: 0 0 4px; }
.meta { font-size: 10.5pt; color: #595959; margin: 0 0 8px; padding-bottom: 6px; border-bottom: 2px solid #0563C1; }
h1 { font-size: 14pt; color: #212121; margin: 16px 0 5px; padding-bottom: 2px; border-bottom: 1px solid #D0D7DE; }
h2 { font-size: 12pt; color: #0563C1; margin: 11px 0 3px; }
h1, h2 { page-break-after: avoid; }
p { margin: 3px 0 6px; text-align: justify; }
b { color: #212121; }
a { color: #0563C1; text-decoration: none; }
table { border-collapse: collapse; margin: 6px auto 2px; font-size: 9pt; border: 1px solid #D0D7DE; page-break-inside: avoid; }
th, td { border: 1px solid #D0D7DE; padding: 2.5px 7px; }
th { background: #EAEEF2; font-weight: bold; text-align: left; }
tr:nth-child(even) td { background: #F6F8FA; }
figure { margin: 7px 0; text-align: center; page-break-inside: avoid; }
figure img { max-width: 100%; max-height: 64mm; }
figcaption, .cap { font-size: 8.8pt; color: #595959; margin: 3px 0 8px; text-align: left; }
figcaption { background: #F6F8FA; border-left: 3px solid #0563C1; padding: 3px 7px; }
.box { background: #F6F8FA; border: 1px solid #D0D7DE; border-left: 3px solid #0563C1; padding: 2px 9px; margin: 6px 0; }
code { font-family: 'DejaVu Sans Mono', Consolas, monospace; font-size: 8.8pt; background: #F6F8FA; padding: 0 2px; }
"""

def inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r"(https?://[^\s<]+)", r'<a href="\1">\1</a>', t)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"(?<![*\w])\*([^*]+)\*(?![*\w])", r"<i>\1</i>", t)
    return t

lines = SRC.read_text(encoding="utf-8").splitlines()
out, i = [], 0
title = []
while i < len(lines) and lines[i].startswith("%"):
    title.append(lines[i][1:].strip()); i += 1
if title:
    out.append('<div class="course">Machine Learning Technologies (MUCEIM) &middot; First Practical Laboratory</div>')
    out.append(f'<div class="title">{inline(title[0])}</div>')
    out.append(f'<div class="meta">Author: {inline(title[1])} &nbsp;&middot;&nbsp; Date: {inline(title[2])}</div>')

while i < len(lines):
    l = lines[i]
    if not l.strip():
        i += 1; continue
    m = re.match(r"(#{1,2}) (.*)", l)
    if m:
        n = len(m.group(1)); out.append(f"<h{n}>{inline(m.group(2))}</h{n}>"); i += 1; continue
    m = re.match(r"!\[(.*)\]\((.*)\)", l)
    if m:
        out.append(f'<figure><img src="{m.group(2)}"><figcaption>{inline(m.group(1))}</figcaption></figure>')
        i += 1; continue
    if l.startswith("|"):
        rows = []
        while i < len(lines) and lines[i].startswith("|"):
            rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")]); i += 1
        t = ["<table>"]
        for r, row in enumerate(rows):
            if r == 1 and all(set(c) <= set("-: ") for c in row):
                continue
            tag = "th" if r == 0 else "td"
            t.append("<tr>" + "".join(f"<{tag}>{inline(c)}</{tag}>" for c in row) + "</tr>")
        t.append("</table>")
        out.append("\n".join(t)); continue
    if l.startswith("*") and l.endswith("*") and not l.startswith("**"):
        out.append(f'<p class="cap">{inline(l)}</p>'); i += 1; continue
    # paragraph (single line per paragraph in the source)
    cls = ' class="box"' if l.startswith(("Main run (", "Reproducibility run (")) else ""
    out.append(f"<p{cls}>{inline(l)}</p>"); i += 1

HTML.write_text(f'<!doctype html><html><head><meta charset="utf-8"><title>Lean Network Challenge</title>'
                f"<style>{CSS}</style></head><body>\n" + "\n".join(out) + "\n</body></html>", encoding="utf-8")

cmd = [EDGE, "--headless", "--disable-gpu", "--no-pdf-header-footer",
       f"--print-to-pdf={PDF}", HTML.as_uri()]
r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
print(r.stdout, r.stderr)
print("PDF written:", PDF, PDF.exists())
