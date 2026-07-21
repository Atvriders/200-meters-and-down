"""Build the "200 Meters and Down" HTML, TXT, and (best-effort) PDF editions.

Parses the book's chapter markdown files (a small, fixed dialect — see the
module-level regexes below), splices in figures from the figure registry and
inline math rendered as SVG, and produces:

  - build_html(chapter_paths, figreg) -> str
      A single self-contained HTML document. Every figure and math
      expression is embedded as inline ``<svg>``; all CSS is inline. No
      external resource references (no ``<link>``, no ``@import``, no
      ``src="http..."``), so the file works fully offline.

  - build_txt(chapter_paths) -> str
      A plain-text edition: markdown markup stripped, math spoken as
      English words, figures rendered as ``[Figure: ID]`` placeholders.

  - build_pdf(html_path, out_pdf) -> bool
      Best-effort PDF rendering of an already-built HTML file via a
      headless Chromium/Chrome binary, falling back to weasyprint, and
      returning False (non-fatal) if neither is available.

Chapter markdown format (fixed):
    line 1:  "## <heading>"                  e.g. "## 1. The Spark Era (1900-1917)"
    (blank line(s))
    line:    "*"<epigraph quote>"*"           italic epigraph
    line:    "*"-- attribution"*"             italic attribution
    body:    "### Section" subheads, "{{fig:ID}}" figure refs (own line),
             "$...$" inline math, "***" section rules, "> ..." blockquotes
             (a blockquote starting "**Meanwhile, Worldwide:**" is a
             sidebar; one starting "**Worked example:**" is a worked
             example), "**bold**" / "*italic*" emphasis.
"""

from __future__ import annotations

import argparse
import html
import pathlib
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass

# Allow running this file directly (`python3 tools/build_book.py`), where
# Python puts this script's own directory (tools/) on sys.path rather than
# the repo root, which would otherwise break the `tools.*` absolute imports
# below. Harmless no-op when already imported as the `tools.build_book`
# package (e.g. under pytest, where pyproject.toml's pythonpath already
# includes the repo root).
_REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from tools.figreg import load, validate
from tools.mathsvg import render
from tools.narration import speak_math, strip_markup

# --------------------------------------------------------------------------
# Chapter parsing
# --------------------------------------------------------------------------

_FIG_LINE_RE = re.compile(r"^\{\{fig:([^}]+)\}\}$")
_FIG_TXT_RE = re.compile(r"\{\{fig:([^}]*)\}\}")
_MATH_SPAN_RE = re.compile(r"\$(.+?)\$")
_BOLD_RE = re.compile(r"\*\*(.+?)\*\*")
_ITALIC_RE = re.compile(r"\*(.+?)\*")
_CHAPTER_STEM_RE = re.compile(r"^ch\d\d$")
_LEADING_NUMBER_RE = re.compile(r"^(\d+)\.")


@dataclass
class Chapter:
    path: pathlib.Path
    id: str
    heading: str
    epigraph: str
    attribution: str
    blocks: list


def compute_chapter_id(path: pathlib.Path, heading: str) -> str:
    """id = file stem if it matches ch\\d\\d, else ch + 2-digit chapter number
    parsed from the heading (Prologue -> ch00, Epilogue -> ch09, "N. ..." -> chNN).
    """
    stem = pathlib.Path(path).stem
    if _CHAPTER_STEM_RE.match(stem):
        return stem
    h = heading.strip()
    if h.startswith("Prologue"):
        return "ch00"
    if h.startswith("Epilogue"):
        return "ch09"
    m = _LEADING_NUMBER_RE.match(h)
    if m:
        return f"ch{int(m.group(1)):02d}"
    raise ValueError(f"{path}: cannot determine chapter id from heading {heading!r}")


def _strip_italic_wrap(s: str) -> str:
    if len(s) >= 2 and s.startswith("*") and s.endswith("*"):
        return s[1:-1]
    return s


def _parse_body(body_lines: list) -> list:
    blocks = []
    buf = []

    def flush():
        if buf:
            blocks.append(("p", " ".join(buf)))
            buf.clear()

    i = 0
    n = len(body_lines)
    while i < n:
        raw = body_lines[i]
        stripped = raw.strip()

        if stripped == "":
            flush()
            i += 1
            continue

        if stripped.startswith("### "):
            flush()
            blocks.append(("h3", stripped[4:].strip()))
            i += 1
            continue

        m = _FIG_LINE_RE.match(stripped)
        if m:
            flush()
            blocks.append(("fig", m.group(1)))
            i += 1
            continue

        if stripped == "***":
            flush()
            blocks.append(("hr", None))
            i += 1
            continue

        if stripped.startswith(">"):
            flush()
            quote_lines = []
            while i < n and body_lines[i].strip().startswith(">"):
                q = body_lines[i].strip()[1:].strip()
                quote_lines.append(q)
                i += 1
            blocks.append(("quote", " ".join(quote_lines)))
            continue

        buf.append(stripped)
        i += 1

    flush()
    return blocks


def parse_chapter(path: pathlib.Path) -> Chapter:
    path = pathlib.Path(path)
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    if not lines or not lines[0].startswith("## "):
        raise ValueError(f"{path}: expected first line to start with '## '")
    heading = lines[0][3:].strip()

    idx = 1
    while idx < len(lines) and lines[idx].strip() == "":
        idx += 1
    if idx + 1 >= len(lines):
        raise ValueError(f"{path}: missing epigraph/attribution lines")

    epigraph = _strip_italic_wrap(lines[idx].strip())
    attribution = _strip_italic_wrap(lines[idx + 1].strip())
    idx += 2

    blocks = _parse_body(lines[idx:])
    cid = compute_chapter_id(path, heading)
    return Chapter(path=path, id=cid, heading=heading, epigraph=epigraph,
                    attribution=attribution, blocks=blocks)


# --------------------------------------------------------------------------
# HTML rendering
# --------------------------------------------------------------------------

def _format_plain(s: str) -> str:
    s = html.escape(s, quote=False)
    s = _BOLD_RE.sub(r"<strong>\1</strong>", s)
    s = _ITALIC_RE.sub(r"<em>\1</em>", s)
    return s


def _inline_html(text: str) -> str:
    out = []
    pos = 0
    for m in _MATH_SPAN_RE.finditer(text):
        out.append(_format_plain(text[pos:m.start()]))
        svg = render(m.group(1))
        out.append(f'<span class="math">{svg}</span>')
        pos = m.end()
    out.append(_format_plain(text[pos:]))
    return "".join(out)


def _render_figure(fig_id: str, figreg: dict) -> str:
    safe_id = html.escape(fig_id, quote=False)
    entry = figreg.get(fig_id)
    if entry is None:
        return (
            f'<figure id="fig-{safe_id}" class="figure figure-missing">'
            f'<figcaption>[missing figure: {safe_id}]</figcaption></figure>'
        )
    file_path = pathlib.Path(entry["file"])
    svg_content = file_path.read_text(encoding="utf-8").strip()
    number = html.escape(str(entry.get("number", "")), quote=False)
    caption = _inline_html(str(entry.get("caption", "")))
    kind = html.escape(str(entry.get("kind", "")), quote=False)
    return (
        f'<figure id="fig-{safe_id}" class="figure figure-{kind}">'
        f'<div class="figure-media">{svg_content}</div>'
        f'<figcaption>Figure {number}. {caption}</figcaption>'
        f'</figure>'
    )


def _render_quote(raw: str) -> str:
    cls = "quote"
    if raw.startswith("**Meanwhile, Worldwide:**"):
        cls = "sidebar"
    elif raw.startswith("**Worked example:**"):
        cls = "worked-example"
    return f'<blockquote class="{cls}"><p>{_inline_html(raw)}</p></blockquote>'


def _render_chapter(c: Chapter, figreg: dict) -> str:
    parts = [f'<section class="chapter" aria-labelledby="{c.id}">']
    parts.append(f'<h2 id="{c.id}">{html.escape(c.heading, quote=False)}</h2>')
    parts.append(
        '<blockquote class="epigraph">'
        f'<p>{html.escape(c.epigraph, quote=False)}</p>'
        f'<p class="attribution">{html.escape(c.attribution, quote=False)}</p>'
        '</blockquote>'
    )
    for kind, content in c.blocks:
        if kind == "p":
            parts.append(f'<p>{_inline_html(content)}</p>')
        elif kind == "h3":
            parts.append(f'<h3>{_inline_html(content)}</h3>')
        elif kind == "fig":
            parts.append(_render_figure(content, figreg))
        elif kind == "hr":
            parts.append('<hr class="rule">')
        elif kind == "quote":
            parts.append(_render_quote(content))
    parts.append("</section>")
    return "".join(parts)


_CSS = """
:root {
  --bg: #fdfaf3;
  --fg: #1b1b1b;
  --muted: #666666;
  --rule: #cccccc;
  --link: #2a5db0;
  --sidebar-bg: #eef3f8;
  --worked-bg: #fff7e6;
}
@media (prefers-color-scheme: dark) {
  :root {
    --bg: #181818;
    --fg: #eaeaea;
    --muted: #aaaaaa;
    --rule: #444444;
    --link: #8ab4f8;
    --sidebar-bg: #1f2937;
    --worked-bg: #332b1a;
  }
}
:root[data-theme="light"] {
  --bg: #fdfaf3;
  --fg: #1b1b1b;
  --muted: #666666;
  --rule: #cccccc;
  --link: #2a5db0;
  --sidebar-bg: #eef3f8;
  --worked-bg: #fff7e6;
}
:root[data-theme="dark"] {
  --bg: #181818;
  --fg: #eaeaea;
  --muted: #aaaaaa;
  --rule: #444444;
  --link: #8ab4f8;
  --sidebar-bg: #1f2937;
  --worked-bg: #332b1a;
}
* { box-sizing: border-box; }
html, body { background: var(--bg); }
body {
  color: var(--fg);
  font-family: Georgia, "Times New Roman", serif;
  max-width: 40rem;
  margin: 0 auto;
  padding: 2rem 1.25rem 4rem;
  line-height: 1.65;
  overflow-x: hidden;
}
h1, h2, h3 { line-height: 1.25; }
a { color: var(--link); }
header.title-block { text-align: center; margin-bottom: 2.5rem; }
nav.toc { margin-bottom: 3rem; border-bottom: 1px solid var(--rule); padding-bottom: 1.5rem; }
nav.toc ul { list-style: none; padding: 0; }
nav.toc li { margin: 0.35rem 0; }
section.chapter { margin-bottom: 4rem; }
blockquote.epigraph {
  font-style: italic;
  color: var(--muted);
  border-left: 3px solid var(--rule);
  margin: 1.5rem 0 2rem;
  padding: 0.25rem 0 0.25rem 1.25rem;
}
blockquote.epigraph p.attribution { font-style: normal; margin-top: 0.5rem; }
blockquote.quote {
  border-left: 3px solid var(--rule);
  margin: 1.5rem 0;
  padding: 0.25rem 0 0.25rem 1.25rem;
  color: var(--muted);
}
blockquote.sidebar {
  background: var(--sidebar-bg);
  border-left: 3px solid var(--link);
  margin: 1.5rem 0;
  padding: 1rem 1.25rem;
  border-radius: 4px;
}
blockquote.worked-example {
  background: var(--worked-bg);
  border-left: 3px solid #c98a1a;
  margin: 1.5rem 0;
  padding: 1rem 1.25rem;
  border-radius: 4px;
}
figure.figure { margin: 2rem 0; text-align: center; }
figure.figure .figure-media { overflow-x: auto; }
figure.figure svg { max-width: 100%; height: auto; }
figure.figure .figure-media svg { max-width: none; }
figcaption { font-size: 0.85em; color: var(--muted); margin-top: 0.5rem; }
span.math { display: inline-block; vertical-align: middle; line-height: 0; }
span.math svg { height: 1em; width: auto; vertical-align: middle; }
hr.rule { border: none; border-top: 1px solid var(--rule); width: 4rem; margin: 2.5rem auto; }
footer.colophon {
  margin-top: 4rem;
  padding-top: 1.5rem;
  border-top: 1px solid var(--rule);
  font-size: 0.85em;
  color: var(--muted);
}
"""


def build_html(chapter_paths: list, figreg: dict) -> str:
    """Build a single self-contained HTML edition from chapter markdown files."""
    chapters = [parse_chapter(pathlib.Path(p)) for p in chapter_paths]

    toc_items = "".join(
        f'<li><a href="#{c.id}">{html.escape(c.heading, quote=False)}</a></li>'
        for c in chapters
    )
    sections = "".join(_render_chapter(c, figreg) for c in chapters)

    document = (
        "<!DOCTYPE html>\n"
        '<html lang="en">\n'
        "<head>\n"
        '<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        "<title>200 Meters and Down</title>\n"
        f"<style>{_CSS}</style>\n"
        "</head>\n"
        "<body>\n"
        '<header class="title-block"><h1>200 Meters and Down</h1></header>\n'
        '<nav class="toc" aria-label="Table of contents">'
        f"<h2>Contents</h2><ul>{toc_items}</ul></nav>\n"
        f"<main>{sections}</main>\n"
        '<footer class="colophon">'
        "<h2>About this edition</h2>"
        "<p>This is a self-contained digital edition: every figure and "
        "mathematical expression is embedded directly as inline SVG, and "
        "all styling lives in this one file, so it reads correctly with no "
        "network connection and adapts to your system's light or dark "
        "theme.</p>"
        "</footer>\n"
        "</body>\n"
        "</html>\n"
    )
    return document


# --------------------------------------------------------------------------
# TXT rendering
# --------------------------------------------------------------------------

def build_txt(chapter_paths: list) -> str:
    """Build a plain-text edition from chapter markdown files.

    For each line: (1) turn ``{{fig:ID}}`` into ``[Figure: ID]``, (2) speak
    math spans as English, (3) strip remaining markdown markup. The ``***``
    section-rule marker is converted to a blank line first, since
    narration.strip_markup's emphasis stripping would otherwise leave a
    stray "*" behind (it turns "***" into "*", not "").
    """
    chapter_texts = []
    for p in chapter_paths:
        path = pathlib.Path(p)
        lines = path.read_text(encoding="utf-8").splitlines()
        out_lines = []
        for line in lines:
            if line.strip() == "***":
                out_lines.append("")
                continue
            line = _FIG_TXT_RE.sub(lambda m: f"[Figure: {m.group(1)}]", line)
            line = speak_math(line)
            line = strip_markup(line)
            out_lines.append(line)
        chapter_texts.append("\n".join(out_lines))
    return "\n\n".join(chapter_texts)


# --------------------------------------------------------------------------
# PDF rendering (best-effort)
# --------------------------------------------------------------------------

_CHROME_BINARIES = ["chromium", "chromium-browser", "google-chrome", "google-chrome-stable"]


def build_pdf(html_path, out_pdf) -> bool:
    """Best-effort PDF rendering of a built HTML file. Non-fatal on failure."""
    html_path = pathlib.Path(html_path).resolve()
    out_pdf = pathlib.Path(out_pdf).resolve()
    out_pdf.parent.mkdir(parents=True, exist_ok=True)

    for binary in _CHROME_BINARIES:
        exe = shutil.which(binary)
        if not exe:
            continue
        cmd = [
            exe,
            "--headless=new",
            "--no-sandbox",
            "--disable-gpu",
            f"--print-to-pdf={out_pdf}",
            f"file://{html_path}",
        ]
        try:
            result = subprocess.run(cmd, capture_output=True, timeout=120)
        except Exception:
            continue
        if result.returncode == 0 and out_pdf.exists() and out_pdf.stat().st_size > 0:
            return True

    try:
        import weasyprint  # type: ignore

        weasyprint.HTML(filename=str(html_path)).write_pdf(str(out_pdf))
        if out_pdf.exists() and out_pdf.stat().st_size > 0:
            return True
    except Exception:
        pass

    print("PDF skipped: no chromium/weasyprint")
    return False


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Build the 200 Meters and Down editions.")
    parser.add_argument("--html", action="store_true", help="build the HTML edition")
    parser.add_argument("--txt", action="store_true", help="build the TXT edition")
    parser.add_argument("--pdf", action="store_true", help="build the PDF edition (best-effort)")
    parser.add_argument("--out", default="build", help="output directory (default: build/)")
    args = parser.parse_args(argv)

    out_dir = pathlib.Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    figreg = load()
    errors = validate(figreg)
    for err in errors:
        print(f"figure registry warning: {err}")

    chapter_paths = sorted(pathlib.Path("chapters").glob("ch*.md"))

    html_path = out_dir / "index.html"
    if args.html or args.pdf:
        document = build_html(chapter_paths, figreg)
        html_path.write_text(document, encoding="utf-8")
        if args.html:
            print(f"wrote {html_path}")

    if args.txt:
        txt = build_txt(chapter_paths)
        txt_path = out_dir / "200-meters-and-down.txt"
        txt_path.write_text(txt, encoding="utf-8")
        print(f"wrote {txt_path}")

    if args.pdf:
        pdf_path = out_dir / "200-meters-and-down.pdf"
        if build_pdf(html_path, pdf_path):
            print(f"wrote {pdf_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
