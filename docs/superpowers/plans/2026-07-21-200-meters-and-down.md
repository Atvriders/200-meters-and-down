# 200 Meters and Down — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce *200 Meters and Down: A Technical History of Amateur Radio* — a ~90–120k-word, ~40+-figure technical-history book — as a self-contained HTML/PDF/TXT edition plus Docker site and 8-voice audiobook, built by a multi-agent workflow against a verified accuracy canon.

**Architecture:** Two tracks. **(A) Tooling** — cross-platform Python build/verify/audiobook tools + Docker/CI, developed test-first against small fixtures (no book content required to test them). **(B) Content** — an `accuracy-canon.md` "bible-as-law", 10 per-chapter specs, ~40 figures, and 10 chapters, produced by parallel writer/figure/auditor agents and gated by the Track-A verification harness. Track A is built first so Track B has a green build+audit gate to write into.

**Tech Stack:** Python 3 (stdlib + `edge-tts`, `matplotlib` for math/plot SVG, optional `weasyprint`), headless Chromium for PDF, `ffmpeg` for audio, nginx/Docker, GitHub + Gitea Actions. Markdown chapters → single-file HTML. Reuses The Long Light's tooling at `/home/kasm-user/the-long-light/` (audiobook, player, Docker, CI) as the adaptation base.

## Global Constraints

- **ONE commit at the very end**, after the full verification suite passes (`tools/audit_book.py` green + build check + copyright-tag check). NO per-task or per-phase commits during the build (user standing preference). Each task below ends with a **verification step**, not a commit. The design spec was already committed separately (`39fa269`); this plan is committed with it or in the same final commit is acceptable, but book/tooling work is one commit.
- **Parallel fan-out when building** (user standing preference): figure production, chapter writing, and auditing run as parallel agents, not serially.
- **All repos and packages public.** Repo: `Atvriders/200-meters-and-down`, dual-homed Gitea (`git.waterburp.com`) + GitHub. Do not push until the user says go.
- **Prose is always original.** Never copy expression from any Handbook. Facts/dates/physics, FCC Part 97, and FCC/NCVEC question pools are free to use.
- **Copyright posture = safe + opportunistic unlock.** Reproduce archival images ONLY when the copyright ledger (`accuracy-canon.md`) marks that source public-domain: the **1927 edition is confirmed PD**; 1931/1933/1936/1940/1941/1951 only if a per-edition pre-1964 renewal check shows lapse; 1968–1983 editions are protected — never reproduced. Every figure is tagged `original` or `archival-PD` with a source.
- **Self-contained output.** The HTML must embed everything (SVG figures inline, math pre-rendered to inline SVG, CSS inline). NO external CDN/script/font references (matches The Long Light + Artifact CSP discipline).
- **Section numbering:** files `chapters/ch00.md` (Prologue) … `ch09.md` (Epilogue); `ch01`–`ch08` are the eight era-chapters. 10 sections total.
- **Every fact traces to the canon; the canon traces to a source.** Auditors enforce (Phase 6). The four flagged uncertainties (1919 restoration month; per-band WARC US dates; incentive-licensing framing; IARU 1925) must be resolved to a sourced value in the canon before any chapter that uses them is accepted.
- **Titles/naming:** book title *200 Meters and Down: A Technical History of Amateur Radio*; audio ID3 `artist=Claude Opus 4.8`, `album=200 Meters and Down`.

---

## File Structure

```
200-meters-and-down/
├── accuracy-canon.md                 # THE BIBLE (law): timeline, notation, glossary, anchor map, copyright ledger
├── AI-CONTEXT.md                     # full machine context dump (Phase 7)
├── README.md                         # overview + formats + "How it was made" stats block (Phase 7)
├── requirements.txt
├── .gitignore                        # ignores audiobook/ and build artifacts
├── docker-compose.yml
├── Dockerfile
├── chapters/
│   ├── ch00.md … ch09.md             # the 10 sections
│   └── specs/ch00.spec.md … ch09.spec.md   # per-chapter writer specs
├── figures/
│   ├── <id>.svg                      # original vector figures (schematics, plots)
│   ├── archival/<id>.<ext>           # verified-PD artifacts only
│   └── figures.json                  # registry: id, chapter, caption, kind(original|archival-PD), source
├── appendices/
│   ├── formulas-and-units.md
│   └── glossary.md                   # (glossary source of truth is the canon; this renders it)
├── tools/
│   ├── narration.py                  # shared: markup strip, formula→speech, figure spoken-desc, roman/number words
│   ├── mathsvg.py                    # inline LaTeX/mathtext → standalone inline SVG (matplotlib)
│   ├── figreg.py                     # figures.json load/validate
│   ├── build_book.py                 # chapters + figures + math → HTML, then TXT, then PDF
│   ├── audit_book.py                 # verification harness (the "test suite" for the book)
│   ├── make_audiobook.py             # adapted from The Long Light: 10 chapters + narration transform
│   └── make_intro.py                 # adapted spoken intro
├── docker/audiobook-index.html       # adapted lantern-style player (10 tracks)
├── .github/workflows/build.yml       # GitHub Actions → ghcr.io image
├── .gitea/workflows/build.yml        # Gitea Actions → gitea registry image
├── tests/                            # pytest for tooling (fixtures + assertions)
│   ├── fixtures/ch_sample.md
│   ├── fixtures/fig_sample.svg
│   ├── test_narration.py
│   ├── test_mathsvg.py
│   ├── test_figreg.py
│   ├── test_build_book.py
│   └── test_audit_book.py
└── docs/superpowers/{specs,plans}/…  # this plan + the design spec
```

---

## PHASE 0 — Scaffolding & shared libraries

### Task 0.1: Repo scaffold

**Files:**
- Create: `requirements.txt`, `.gitignore`, `docker-compose.yml`, `tests/fixtures/ch_sample.md`, `tests/fixtures/fig_sample.svg`

**Interfaces:**
- Produces: the fixture chapter + figure that every tooling test consumes.

- [ ] **Step 1:** Write `requirements.txt`:

```
edge-tts>=6.1
matplotlib>=3.7
weasyprint>=60 ; platform_system != "Windows"
pytest>=8
```

- [ ] **Step 2:** Write `.gitignore`:

```
audiobook/
build/
__pycache__/
*.pyc
.venv/
```

- [ ] **Step 3:** Write `docker-compose.yml` (adapt The Long Light's):

```yaml
services:
  two-hundred-meters-and-down:
    image: ghcr.io/atvriders/200-meters-and-down:latest
    container_name: 200-meters-and-down
    ports:
      - "8080:80"
    restart: unless-stopped
```

- [ ] **Step 4:** Write `tests/fixtures/ch_sample.md` — a minimal chapter exercising every feature the build must handle (heading, epigraph, attribution, a `## The Story`/`## How It Works` section, an inline math span `$E = IR$`, a figure ref `{{fig:sample}}`, a scene/section rule `***`, a worked-example callout, a "Meanwhile, Worldwide" sidebar marker):

```markdown
## 1. The Spark Era (1900–1917)

*"The set here described will put a clean note into the ether for a hundred miles."*
*— The Radio Amateur's Handbook, sample epigraph*

### The Story
The boom began before the law did.

> **Meanwhile, Worldwide:** a parallel note.

### How It Works
The tank stores energy, and by Ohm's law $E = IR$ across the gap.

{{fig:sample}}

> **Worked example:** with $I = 2$ and $R = 3$, $E = 6$.

***

And the era closed on a question it could not yet answer.
```

- [ ] **Step 5:** Write `tests/fixtures/fig_sample.svg` — a tiny valid standalone SVG:

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 40"><rect x="1" y="1" width="98" height="38" fill="none" stroke="currentColor"/><text x="50" y="24" text-anchor="middle" font-size="10" fill="currentColor">sample</text></svg>
```

- [ ] **Step 6 (verify):** `python -c "import pathlib,sys; [sys.exit('missing '+p) for p in ['requirements.txt','.gitignore','docker-compose.yml','tests/fixtures/ch_sample.md','tests/fixtures/fig_sample.svg'] if not pathlib.Path(p).exists()]; print('scaffold OK')"` → prints `scaffold OK`.

---

### Task 0.2: `tools/narration.py` — shared narration & text transforms (TDD)

**Files:**
- Create: `tools/narration.py`, `tests/test_narration.py`

**Interfaces:**
- Produces:
  - `strip_markup(s: str) -> str` — remove `*…*`/`**…**`, `{{fig:…}}` refs, `>` blockquote markers, heading `#`.
  - `speak_math(s: str) -> str` — replace `$…$` spans with spoken English (`E = IR` → "E equals I R"; `|x|` → "the magnitude of x"; `f_IF` → "f sub I F"; `≈`→"approximately"; `λ`→"lambda"; `×`→"times"; `Δf`→"delta f").
  - `speak_figures(s: str, descriptions: dict[str,str]) -> str` — replace `{{fig:ID}}` with `"(Figure N. <one-line description>.)"`.
  - `NUMBER_WORDS: list[str]`, `roman_to_int(s)` (reuse from The Long Light).

- [ ] **Step 1: Write the failing test** `tests/test_narration.py`:

```python
from tools.narration import strip_markup, speak_math, speak_figures

def test_strip_markup_removes_emphasis_and_refs():
    assert strip_markup("*hi* and **bold** {{fig:x}}") == "hi and bold"

def test_speak_math_ohms_law():
    assert speak_math("by $E = IR$ here") == "by E equals I R here"

def test_speak_math_symbols():
    assert speak_math("$c = f\\lambda$") == "c equals f lambda"
    assert speak_math("$\\Delta f \\approx f v / c$") == "delta f approximately f v over c"

def test_speak_figures_inserts_description():
    out = speak_figures("see {{fig:tank}} now", {"tank": ("4", "a spark-gap tank circuit")})
    assert out == "see (Figure 4. a spark-gap tank circuit.) now"
```

- [ ] **Step 2: Run to verify it fails** — `python -m pytest tests/test_narration.py -q` → FAIL (ModuleNotFoundError).

- [ ] **Step 3: Implement `tools/narration.py`** with the four functions. Core logic:

```python
import re

NUMBER_WORDS = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight",
                "Nine", "Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen"]
_ROMAN = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100}

def roman_to_int(s):
    t = 0
    for i, c in enumerate(s):
        v = _ROMAN[c]
        t += -v if i + 1 < len(s) and _ROMAN[s[i+1]] > v else v
    return t

def strip_markup(s):
    s = re.sub(r"\{\{fig:[^}]+\}\}", "", s)
    s = re.sub(r"^\s{0,3}#{1,6}\s*", "", s)
    s = re.sub(r"^\s*>\s?", "", s)
    s = re.sub(r"\*{1,2}([^*]+?)\*{1,2}", r"\1", s)
    return re.sub(r"\s{2,}", " ", s).strip()

_MATH = [(r"\\Delta", "delta"), (r"\\lambda", "lambda"), (r"\\approx", "approximately"),
         (r"\\times", "times"), (r"≈", "approximately"), (r"λ", "lambda"), (r"×", "times"),
         (r"\|([^|]+)\|", r"the magnitude of \1"), (r"_\{?([A-Za-z0-9]+)\}?", r" sub \1"),
         (r"/", " over "), (r"=", " equals ")]

def _speak_expr(e):
    for pat, rep in _MATH:
        e = re.sub(pat, rep, e)
    return re.sub(r"\s{2,}", " ", e).strip()

def speak_math(s):
    return re.sub(r"\$([^$]+)\$", lambda m: _speak_expr(m.group(1)), s)

def speak_figures(s, descriptions):
    def r(m):
        num, desc = descriptions.get(m.group(1), ("", ""))
        return f"(Figure {num}. {desc}.)" if num else ""
    return re.sub(r"\{\{fig:([^}]+)\}\}", r, s)
```

*(Refine regexes until the four asserts pass; keep the `sub _` spacing exact — "f_IF" → "f sub IF".)*

- [ ] **Step 4: Run to verify pass** — `python -m pytest tests/test_narration.py -q` → PASS (4 passed).

- [ ] **Step 5 (verify):** no commit (Global Constraint). Confirm green and move on.

---

### Task 0.3: `tools/figreg.py` — figure registry (TDD)

**Files:**
- Create: `tools/figreg.py`, `figures/figures.json`, `tests/test_figreg.py`

**Interfaces:**
- Produces: `load(path="figures/figures.json") -> dict[str, Figure]`; `validate(reg) -> list[str]` (returns error strings; empty = OK). `Figure` fields: `id, chapter(int), number(str), caption(str), kind("original"|"archival-PD"), source(str), file(str)`.
- Consumes: nothing.

- [ ] **Step 1: Write failing test** `tests/test_figreg.py`:

```python
import json, pathlib
from tools.figreg import load, validate

def test_validate_flags_protected_source(tmp_path):
    reg = {"x": {"id":"x","chapter":6,"number":"6.1","caption":"c",
                 "kind":"archival-PD","source":"1974 Handbook","file":"figures/archival/x.png"}}
    errs = validate(reg)
    assert any("1974" in e or "protected" in e.lower() for e in errs)

def test_validate_accepts_original(tmp_path):
    reg = {"x": {"id":"x","chapter":1,"number":"1.1","caption":"c",
                 "kind":"original","source":"authored","file":"figures/x.svg"}}
    assert validate(reg) == []
```

- [ ] **Step 2: Run to verify it fails** — `python -m pytest tests/test_figreg.py -q` → FAIL.

- [ ] **Step 3: Implement `tools/figreg.py`.** `validate` rules: every `archival-PD` figure's `source` must NOT reference an edition year in {1968,1974,1976,1977,1981,1983}; must reference a ledger-approved PD source (1927, or an edition flagged PD in the canon, or an external PD); `original` figures must have `file` ending `.svg` and exist; `number` must be unique; `chapter` in 0..9. Seed `figures/figures.json` as `{}`.

- [ ] **Step 4: Run to verify pass** — `python -m pytest tests/test_figreg.py -q` → PASS.

- [ ] **Step 5 (verify):** green; move on.

---

## PHASE 1 — Build & verification tooling (TDD)

### Task 1.1: `tools/mathsvg.py` — inline math → standalone SVG (TDD)

**Files:** Create `tools/mathsvg.py`, `tests/test_mathsvg.py`

**Interfaces:** Produces `render(expr: str, color="currentColor") -> str` returning a self-contained `<svg>…</svg>` string (matplotlib mathtext → SVG path, no external font dependency at view time), sized to the expression.

- [ ] **Step 1: Failing test** `tests/test_mathsvg.py`:

```python
from tools.mathsvg import render

def test_render_returns_inline_svg():
    svg = render("E = IR")
    assert svg.strip().startswith("<svg") and "</svg>" in svg
    assert "http" not in svg  # fully self-contained, no external refs
```

- [ ] **Step 2: Run → FAIL.**

- [ ] **Step 3: Implement** using matplotlib's `mathtext`/`figure.savefig(format="svg")` with `text(0.5,0.5, f"${expr}$")`, transparent background, `bbox_inches="tight"`, then strip the XML prolog/`<?xml…?>` and any `<!DOCTYPE>`; set glyph fill to `currentColor` so it themes in light/dark. Return the `<svg …>…</svg>` substring only.

- [ ] **Step 4: Run → PASS.**

- [ ] **Step 5 (verify):** render `c = f\\lambda` and `f_{IF} = |f_{RF} - f_{LO}|` manually; confirm both produce valid SVG. Green; move on.

---

### Task 1.2: `tools/build_book.py` — HTML build (TDD)

**Files:** Create `tools/build_book.py`, `tests/test_build_book.py`

**Interfaces:**
- Consumes: `chapters/ch*.md`, `figures/figures.json` (+ figure files), `tools/mathsvg.render`, `tools/figreg.load`.
- Produces CLI: `python tools/build_book.py --html [--txt] [--pdf] --out build/`. Function `build_html(chapter_paths, figreg) -> str`.
- HTML requirements: single file; `<h2 id="chNN">` per chapter with a linked TOC at top; epigraph rendered italic with attribution; `### section` → `<h3>`; `{{fig:ID}}` replaced by `<figure><svg inline>…<figcaption>Figure N. caption</figcaption></figure>`; `$…$` replaced by inline math SVG; `***` → `<hr class="rule">`; blockquote `>` → `<blockquote>` (sidebars/worked-examples styled by a leading `**Meanwhile, Worldwide:**`/`**Worked example:**`); inline CSS with light/dark via `prefers-color-scheme` + `:root[data-theme]`; an "About this edition" colophon; no external refs.

- [ ] **Step 1: Failing test** `tests/test_build_book.py`:

```python
import pathlib
from tools.build_book import build_html
from tools.figreg import load

def test_build_html_embeds_figure_toc_and_math(tmp_path):
    figreg = {"sample": {"id":"sample","chapter":1,"number":"1.1","caption":"A sample",
              "kind":"original","source":"authored","file":"tests/fixtures/fig_sample.svg"}}
    html = build_html([pathlib.Path("tests/fixtures/ch_sample.md")], figreg)
    assert '<svg' in html                       # figure inlined
    assert 'Figure 1.1' in html                 # caption numbered
    assert 'id="ch01"' in html                  # anchor
    assert 'href="#ch01"' in html               # TOC link resolves
    assert 'equals' not in html                 # math is SVG, not spoken text
    assert 'http://' not in html and 'https://' not in html   # self-contained
    assert 'Meanwhile, Worldwide' in html
```

- [ ] **Step 2: Run → FAIL.**

- [ ] **Step 3: Implement `build_html`** (markdown-subset parser tuned to the format laws — do NOT pull a heavyweight md lib; a focused parser is more reliable for this fixed format). Inline each figure by reading its `file` and splicing the `<svg>`; number figures per `figures.json`; render math spans via `mathsvg.render`; build the TOC from chapter headings. Then add `--txt` (use `narration.strip_markup` per line, drop figures to `[Figure N: caption]`, keep prose) and PDF (Task 1.4).

- [ ] **Step 4: Run → PASS.**

- [ ] **Step 5 (verify):** `python tools/build_book.py --html --out build/ ` on the fixture-only repo; open `build/index.html` byte-check for `<svg`, TOC, colophon. Green.

---

### Task 1.3: TXT edition (extends 1.2)

**Files:** Modify `tools/build_book.py`; add a test to `tests/test_build_book.py`.

- [ ] **Step 1: Failing test** — add:

```python
def test_txt_strips_markup_and_math():
    from tools.build_book import build_txt
    import pathlib
    txt = build_txt([pathlib.Path("tests/fixtures/ch_sample.md")])
    assert "*" not in txt and "{{fig" not in txt
    assert "E equals I R" in txt or "E = IR" in txt   # math rendered readably
    assert "[Figure" in txt                            # figure noted, not dropped silently
```

- [ ] **Step 2: Run → FAIL. Step 3:** implement `build_txt` (uses `narration.strip_markup`; math via `narration.speak_math` for readability; figures → `[Figure N: caption]`). **Step 4: Run → PASS. Step 5 (verify):** eyeball TXT output.

---

### Task 1.4: PDF edition (best-effort, extends 1.2)

**Files:** Modify `tools/build_book.py`.

- [ ] **Step 1:** Implement `build_pdf(html_path, out_pdf)`: try headless Chromium (`chromium`, `chromium-browser`, `google-chrome`, `google-chrome-stable` on PATH) via `--headless=new --no-sandbox --print-to-pdf=<out>`; on absence, try `weasyprint`; on both absent, print a clear `PDF skipped: no chromium/weasyprint` warning and continue (non-fatal). *(Per spec open item — PDF is best-effort.)*
- [ ] **Step 2 (verify):** run `python tools/build_book.py --html --pdf --out build/`; assert either `build/200-meters-and-down.pdf` exists OR the skip warning printed. Green.

---

### Task 1.5: `tools/audit_book.py` — the verification harness (TDD)

**Files:** Create `tools/audit_book.py`, `tests/test_audit_book.py`

**Interfaces:**
- Consumes: `chapters/ch*.md`, `accuracy-canon.md`, `figures/figures.json`, the built HTML.
- Produces CLI `python tools/audit_book.py` → exit 0 if all checks pass, else non-zero + a report. Checks:
  1. **Figure integrity** — every `{{fig:ID}}` in any chapter exists in `figures.json` and its file exists; no orphan registry entries.
  2. **Copyright-tag** — `figreg.validate` returns no errors (no protected image reproduced).
  3. **TOC/anchor** — build HTML; every TOC `href="#chNN"` has a matching `id`.
  4. **Math** — every `$…$` renders without mathsvg error.
  5. **Canon cross-check** — every 4-digit year and key figure that appears in a chapter's "pinned facts" block is present in `accuracy-canon.md`'s timeline (catch date drift). *(Heuristic: extract `**FACT:**`-tagged claims writers must place, cross-check verbatim against the canon.)*
  6. **Flagged-uncertainty** — the canon contains no unresolved `⚠️ UNVERIFIED` markers.
  7. **Format laws** — each `ch01`–`ch08` has an epigraph block, a `### How It Works`, ≥1 worked-example blockquote, and ends on non-moral text (no banned phrases: "little did they know", "in that moment", "a testament to").

- [ ] **Step 1: Failing test** `tests/test_audit_book.py`:

```python
from tools.audit_book import check_banned_phrases, check_figure_integrity

def test_banned_phrases_flagged():
    errs = check_banned_phrases("…and little did they know it would grow.")
    assert errs and "little did they know" in errs[0]

def test_figure_integrity_missing(tmp_path):
    errs = check_figure_integrity(["{{fig:ghost}}"], registry={})
    assert any("ghost" in e for e in errs)
```

- [ ] **Step 2: Run → FAIL. Step 3:** implement the check functions + a `main()` that runs all seven checks and aggregates. **Step 4: Run → PASS. Step 5 (verify):** run `python tools/audit_book.py` against the fixture repo; confirm it reports the (expected) absence of real chapters gracefully rather than crashing.

---

## PHASE 2 — Audiobook & serving tooling (adapt The Long Light)

### Task 2.1: `tools/make_audiobook.py` (adapt + narration transform)

**Files:** Create `tools/make_audiobook.py` (from `/home/kasm-user/the-long-light/tools/make_audiobook.py`); add `tests/test_audiobook_prepare.py`.

**Interfaces:** Keep the 8-voice `VOICES` map, chunking, retry/stitch, resumability, CLI verbatim. **Deltas:** chapter range `0..9` (not `0..30`); `spoken_heading` handles our headings (`"1. The Spark Era (1900–1917)"` → `"Chapter One. The Spark Era. 1900 to 1917."`, `Prologue`/`Epilogue` forms); `prepare()` calls `narration.strip_markup` + `narration.speak_math` + `narration.speak_figures` (loading one-line figure descriptions from `figures.json` — add a `spoken` field, or fall back to `caption`); intro line `"200 Meters and Down. A Technical History of Amateur Radio."`; ID3 `album=200 Meters and Down`, `artist=Claude Opus 4.8`, `track={n+1}/10`, `composer=<voice label>`.

- [ ] **Step 1: Failing test** `tests/test_audiobook_prepare.py`:

```python
from tools.make_audiobook import spoken_heading, prepare_text

def test_spoken_heading_era_chapter():
    assert spoken_heading("1. The Spark Era (1900–1917)") == \
        "Chapter One. The Spark Era. 1900 to 1917."

def test_prepare_text_speaks_math_and_drops_fig_markup():
    out = prepare_text("The tank obeys $E = IR$ here.\n\n{{fig:x}}\n", {"x": ("1", "a tank")})
    assert "E equals I R" in out
    assert "{{fig" not in out
    assert "Figure 1" in out
```

- [ ] **Step 2: Run → FAIL. Step 3:** copy the file; refactor `prepare()` into a testable `prepare_text(body, fig_desc)` + update `spoken_heading`, ranges, metadata. **Step 4: Run → PASS. Step 5 (verify):** `python tools/make_audiobook.py --test --voice ryan` (needs edge-tts network) OR, if offline, assert `prepare_text` on `ch01.md` once it exists. Green.

### Task 2.2: `tools/make_intro.py` (adapt)

- [ ] **Step 1:** Copy from The Long Light; rewrite `INTRO` text: what the book is, that it was written by Claude Opus 4.8 (1M context) in Claude Code, that it's a technical history across eras, eight voices offered, how it was made. **Step 2 (verify):** `python tools/make_intro.py --dry` prints the intro text; no synth needed to verify wording.

### Task 2.3: `docker/audiobook-index.html` player (adapt)

- [ ] **Step 1:** Copy The Long Light's 551-line player; change title to *200 Meters and Down*, track list to 10 (`ch00`–`ch09`), chapter labels to our headings, keep the lantern-beam canvas/voice-switcher/keyboard/resume logic. Keep the beam motif (a nod to the reused machinery) or restyle to a waveform-scope — cosmetic, author's choice. **Step 2 (verify):** open the file locally with 2–3 dummy MP3s; confirm playback, voice switch, keyboard controls work.

### Task 2.4: Docker + CI

**Files:** Create `Dockerfile`, `.github/workflows/build.yml`, `.gitea/workflows/build.yml`.

- [ ] **Step 1:** `Dockerfile` (adapt): copy `build/index.html`→`index.html`, `build/*.pdf`/`*.txt`, `chapters/`, `audiobook/`, `docker/audiobook-index.html`→`audiobook/index.html`.
- [ ] **Step 2:** CI (adapt both workflows): fetch audiobook from release `v1.0` (intro + 8 voices × 10 chapters = **81 files**; print `audiobook files: 81`), build+push image to `ghcr.io/atvriders/200-meters-and-down:latest` (GitHub) and the gitea registry (Gitea, gated by `github.server_url`). Add a build step that runs `python tools/build_book.py --html --txt --pdf --out build/` BEFORE the Docker build.
- [ ] **Step 3 (verify):** `yamllint`/`python -c "import yaml,glob; [yaml.safe_load(open(f)) for f in glob.glob('.g*/workflows/build.yml')]; print('workflows parse OK')"`. Green.

---

## PHASE 3 — The accuracy canon (content foundation)

### Task 3.1: Build & verify `accuracy-canon.md` (research fan-out)

**Files:** Create `accuracy-canon.md`, `appendices/formulas-and-units.md`, `appendices/glossary.md`.

**This is a parallel research fan-out**, not solo prose. Dispatch agents to:
- Resolve the four flagged uncertainties to sourced values: (a) exact 1919 WWI transmitting-restoration month; (b) per-band WARC US availability dates (30/17/12 m); (c) incentive-licensing framing (FCC Docket 15928, contentious, not ARRL); (d) IARU founding (Apr 1925, Paris, Maxim). Each → a dated line with an authoritative citation.
- Run **per-edition copyright-renewal checks** (Stanford Copyright Renewal DB / US Copyright Office) for the 1928–1963 editions (1931/1933/1936/1940/1941/1951) and record each as PD-if-lapsed / protected, plus confirm 1927 = PD and 1964+ = protected. → the **copyright ledger** table.
- Extract the pinned timeline (all §4 milestones + per-era technical facts) with sources.

- [ ] **Step 1:** Dispatch the research agents (parallel). Each returns structured, sourced findings.
- [ ] **Step 2:** Assemble `accuracy-canon.md` with sections: **Pinned Timeline** (date | event | source), **Notation & Units** (symbol table), **Glossary** (term | definition), **Per-era Anchor Map** (chapter → Handbook edition(s)), **Copyright Ledger** (edition | status | basis | reproducible?), **Resolved Uncertainties**. Every contested claim carries a citation. No `⚠️ UNVERIFIED` may remain.
- [ ] **Step 3:** Write `appendices/formulas-and-units.md` (every formula the book uses, in canon notation) and `appendices/glossary.md` (rendered from the canon glossary).
- [ ] **Step 4 (verify):** `grep -c "UNVERIFIED" accuracy-canon.md` → `0`; copyright ledger has all 13 editions; each flagged uncertainty has a citation. A reviewer agent confirms internal consistency.

### Task 3.2: Per-chapter writer specs

**Files:** Create `chapters/specs/ch00.spec.md … ch09.spec.md`.

- [ ] **Step 1:** From the design outline + Appendix A capsules + the canon, write one spec per section containing: heading (exact), era span, **story beats** (with canon-cited dates), **teach-list** (the specific circuits/physics + the required worked example), **figure list** (the 2–4 figure IDs to reference, matching `figures.json`), **anchor Handbook edition(s)** + the epigraph passage to use, **neighbor beats** (previous/next chapter's hook so seams connect), **word budget** (~8–12k core; prologue/epilogue shorter), and the **`**FACT:**` claims** the writer must embed for the auditor's canon cross-check.
- [ ] **Step 2 (verify):** each spec references only figure IDs present in `figures.json` (Phase 4 seeds these first — see ordering note) and only dates present in the canon.

### Task 3.3: Anchor-edition epigraph extraction

**Files:** Create `chapters/specs/epigraphs.md` (source-tagged candidate epigraphs).

- [ ] **Step 1:** For chapters with an owned anchor edition (ch2:1927, ch3:1931/33/36, ch4:1940/41, ch5:1951, ch6:1968/74/76, ch7:1977/81/83), extract a short quotable line from the PDF (targeted re-OCR of the specific page if needed). For ch1/prologue/ch8 (no owned anchor), select a period source line and tag it. **Copyright note:** a short factual quotation with attribution is fair; but where an edition is protected and you want a *longer* excerpt, paraphrase instead. **Step 2 (verify):** every section has a sourced epigraph candidate; protected-edition epigraphs are short-quote-with-attribution only.

---

## PHASE 4 — Figures (parallel fan-out)

### Task 4.1: Produce ~40 figures + register them

**Files:** Create `figures/<id>.svg`, `figures/archival/<id>.*`, populate `figures/figures.json`.

- [ ] **Step 1:** From the design's per-chapter figure lists (~4–6 × 8 chapters + prologue/epilogue), assign each a stable `id` and `number` (`<chapter>.<n>`), and seed `figures.json` (so Task 3.2 specs can reference IDs). 
- [ ] **Step 2 (parallel):** Dispatch figure-generation agents — one per figure or per small cluster:
  - **Schematics/block diagrams** (spark-gap TX, regen RX, superhet block, Pierce oscillator, pi-network, Yagi geometry, SSB filter/phasing, FM discriminator, repeater duplex, PLL, AX.25 frame, SDR I/Q, FT8 sequence): hand-authored clean **SVG**, house style (currentColor strokes so they theme), labeled.
  - **Plots/curves** (damped-wave vs CW, AM/SSB spectra, class-C plate current, IF filter response, Doppler-vs-time, azimuth radiation pattern, FFT waterfall, c=fλ nomograph): matplotlib → SVG.
  - **Archival-PD** (1BCG transmitter, Hertz apparatus, period photos): ONLY from ledger-approved PD sources; cleaned + captioned; saved under `figures/archival/`.
- [ ] **Step 3:** Register every figure in `figures.json` with `kind`+`source`+`spoken` (one-line description for the audiobook).
- [ ] **Step 4 (verify):** `python tools/audit_book.py` figure checks pass on the registry (`figreg.validate` empty; all files exist; every SVG parses; no protected source).

---

## PHASE 5 — Chapters (parallel fan-out)

### Task 5.1: Write the 10 sections

**Files:** Create `chapters/ch00.md … ch09.md`.

- [ ] **Step 1 (parallel):** Dispatch **≥8 chapter-writer agents** (prologue/epilogue can pair with a neighbor), each given: the full `accuracy-canon.md`, the whole outline, its `chapters/specs/chNN.spec.md`, its neighbors' hooks, its `figures.json` slice, and its extracted epigraph. Each writes original prose to the format laws (§5 of the spec): epigraph → The Story (+ "Meanwhile, Worldwide" sidebars) → How It Works (figures via `{{fig:ID}}`, math via `$…$`, ≥1 worked example) → State of the Art in [year] → forward hook. Embed the required `**FACT:**` claims for cross-check.
- [ ] **Step 2 (verify):** for each chapter, `python tools/build_book.py --html --out build/` succeeds with that chapter present; all `{{fig:ID}}` resolve; word count within budget (± tolerance); banned-phrase check clean.

---

## PHASE 6 — Technical-accuracy audit (parallel fan-out)

### Task 6.1: Auditor agents over chapter spans

**Files:** Modify `chapters/ch*.md` (surgical fixes only).

- [ ] **Step 1 (parallel):** Dispatch auditor agents over spans (e.g. 00–02, 03–05, 06–07, 08–09). Each verifies: every date/value/band-edge against the canon; every formula's correctness and notation; every figure reference resolves and is technically apt; format laws satisfied; **copyright** (no protected excerpt/image); the seams to neighboring chapters. Auditors edit files surgically and log each change.
- [ ] **Step 2 (verify):** `python tools/audit_book.py` → exit 0 (all seven checks green). Any failure loops back to a targeted fix, then re-audit.

---

## PHASE 7 — Assemble, verify, ship

### Task 7.1: Front matter — `AI-CONTEXT.md` + `README.md`

**Files:** Create `AI-CONTEXT.md`, `README.md`.

- [ ] **Step 1:** Write `AI-CONTEXT.md` — full context dump (mirroring The Long Light's): what the book is; the accuracy canon (timeline/notation/glossary/anchor-map/copyright-ledger, summarized with pointer to `accuracy-canon.md`); the chapter-by-chapter outline; the format/style laws; production history; infrastructure notes (build/audiobook/Docker/CI); guidance for AI models extending it. Credentials omitted.
- [ ] **Step 2:** Write `README.md` — overview, the vow-style hook line, formats table (HTML/PDF/TXT/chapters/audiobook release/Docker), Docker + local-build + audiobook instructions, "For AI models" pointer, and a **"How it was made"** section with placeholders for the stats block (filled in Task 7.3).
- [ ] **Step 3 (verify):** links resolve; formats table matches actual files.

### Task 7.2: Full verification gate

- [ ] **Step 1:** `python -m pytest -q` (all tooling tests green).
- [ ] **Step 2:** `python tools/build_book.py --html --txt --pdf --out build/` → HTML+TXT produced (PDF produced or explicitly skipped).
- [ ] **Step 3:** `python tools/audit_book.py` → exit 0.
- [ ] **Step 4 (verify):** manually open `build/index.html` — TOC navigates, figures render in light AND dark, math renders, no horizontal scroll, colophon present. Record word count + figure count.

### Task 7.3: Stats, single commit, and ship (on user go)

- [ ] **Step 1:** Gather production stats — number of agents, total tokens consumed (from the workflow/session), workflow wall time, end-to-end time, word count, figure count — and write them into the README **"How it was made"** block (the user explicitly requested tokens + time in the README). *(These are captured at build completion; the workflow/orchestration reports them.)*
- [ ] **Step 2:** **Single commit** of the entire build (Global Constraint): `git add -A && git commit` with a full message (co-author trailer: `Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>`).
- [ ] **Step 3 (on explicit user go):** create the `Atvriders/200-meters-and-down` repo (Gitea primary + GitHub), push, build the 8-voice audiobook (`python tools/make_audiobook.py --all` + intro), create release `v1.0`, upload the 81 audio files, let CI build/push the images. Then confirm the README stats are live on GitHub.
- [ ] **Step 4 (verify):** the pushed GitHub README shows the tokens + time stats; CI is green; the image serves the book + player.

---

## Ordering & execution notes

- **Track A (Phases 0–2) is fully testable now** with fixtures — do it first so Track B writes into a green gate.
- **Phase 4 (figures) seeds `figures.json` IDs before Phase 3.2 specs and Phase 5 chapters reference them** — so run 3.1 (canon) → 4.1 (figures + registry) → 3.2/3.3 (specs/epigraphs) → 5.1 (chapters) → 6.1 (audit) → 7.
- **Content phases (3.1, 4.1, 5.1, 6.1) are the parallel-agent fan-outs** — ideal for a Workflow (writers + auditors), mirroring The Long Light's 35-agent run.
- **No commits until Task 7.3** (one commit for the whole build).

---

## Self-Review — plan vs spec

**Spec coverage:** spine/eras/depth → Phases 3.2/5; 10-section outline → Task 3.2/5.1; per-chapter anatomy/format laws → 3.2 spec + 5.1 write + 6.1/audit checks; accuracy canon → 3.1; copyright discipline → Global Constraints + 0.3 `figreg.validate` + 3.1 ledger + 3.3 epigraph rule + 6.1; figure pipeline (hybrid) → 4.1; multi-agent workflow → 3.1/4.1/5.1/6.1 fan-outs; deliverables (HTML/PDF/TXT) → 1.2–1.4; Docker/repo/CI → 2.4/7.3; audiobook + narration transform → 2.1–2.3; AI-CONTEXT dump → 7.1; **README stats (tokens+time)** → 7.1/7.3; verification gate → 1.5/7.2; flagged uncertainties → 3.1; the "200 meters and down" correction → canon timeline. **No gaps found.**

**Placeholder scan:** none — the four `⚠️ UNVERIFIED` items are an explicit Task 3.1 deliverable to resolve, not plan placeholders; content tasks carry concrete acceptance criteria + verify commands rather than vague "write tests."

**Type consistency:** `narration.strip_markup/speak_math/speak_figures` used identically in 0.2, 1.3, 2.1; `figreg.load/validate` + the `Figure` fields used identically in 0.3, 4.1, 6.1; `mathsvg.render` signature consistent in 1.1/1.2; `build_html/build_txt/build_pdf` names consistent across 1.2–1.4 and 7.2. Consistent.
