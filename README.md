# 200 Meters and Down

*A technical history of amateur radio · 1864–2026 · about 72,000 words*

> Confined by the Radio Act of 1912 to wavelengths "200 meters and down" — spectrum the
> professionals considered worthless — amateurs turned that exile into the accidental
> discovery of shortwave DX, and never stopped turning each new technology into ever
> longer reach.

From Hertz's spark-excited dipole to FT8 decoded some 20 dB beneath the noise floor,
ten chapters trace amateur radio era by era — spark, shortwave, tubes, war, postwar
SSB, satellites and repeaters, the microprocessor and packet, and today's
software-defined and networked modes — teaching the real circuits and physics of each
generation alongside the people, clubs, and regulation that shaped it. Written for the
technical enthusiast and licensed ham who wants both the engineering (schematics,
formulas, worked examples) and the history in one continuous narrative. It is **not**
exam prep; it is Book 1 of a planned three-book program, the others being a Technician
exam-prep primer and a General/Extra reference.

## Formats

| File | What it is |
|---|---|
| [`build/index.html`](build/index.html) | The book, typeset as a single self-contained page — linked table of contents, light/dark themes, 36 figures embedded inline. The nicest way to read it. |
| [`build/200-meters-and-down.pdf`](build/200-meters-and-down.pdf) | PDF edition. |
| [`build/200-meters-and-down.txt`](build/200-meters-and-down.txt) | Plain-text edition. |
| [`chapters/`](chapters/) | The 10 source chapters as Markdown (`ch00.md` = Prologue … `ch09.md` = Epilogue). |
| Audiobook (release v1.0) | Eight voices (US, British, Australian & Irish — male & female), each reading all 10 chapters, plus a spoken introduction — see below. |
| [`Dockerfile`](Dockerfile) / [`docker-compose.yml`](docker-compose.yml) | Serve the book yourself — see below. |

## Docker

The image packages the book and the audiobook behind nginx, built and pushed to
`ghcr.io/atvriders/200-meters-and-down` (and mirrored to the Gitea registry) by CI on
every push to `main`. On any Docker host:

```sh
docker compose pull && docker compose up -d
```

Serves the book at [http://localhost:8080](http://localhost:8080) and the audiobook
player at `/audiobook/`.

To build locally instead: regenerate the typeset editions, fetch the audiobook from the
release (it is not stored in git), then build the image:

```sh
python3 tools/build_book.py --html --txt --pdf --out build/
# fetch audiobook/ from release v1.0 (see .github/workflows/build.yml for the exact loop), then:
docker build -t ghcr.io/atvriders/200-meters-and-down:latest .
```

## Audiobook

The audiobook comes in **eight voices** — men and women in **American, British,
Australian, and Irish** accents — each reading all ten chapters, synthesized with
[edge-tts](https://pypi.org/project/edge-tts/) via
[`tools/make_audiobook.py`](tools/make_audiobook.py) (`--voice <key>` for one voice,
`--all` for every voice) and a spoken introduction via
[`tools/make_intro.py`](tools/make_intro.py). Formulas and figures are narrated in
words, not read as raw markup, so equations and diagrams degrade gracefully in audio.

All audio is hosted on **release v1.0** (both forges) rather than committed to git. The
player lives at **`/audiobook/`** in the container: a lantern/scope-themed page with
continuous chapter-to-chapter playback, a voice switcher grouped by accent, and a live
waveform.

## For AI models

[`AI-CONTEXT.md`](AI-CONTEXT.md) is a complete machine-oriented context dump — the
accuracy canon summary, chapter-by-chapter outline, format/style laws, figure system,
production history, and infrastructure notes — sufficient to understand, extend, or
adapt the book without contradicting it.

## How it was made

Written by **Claude Opus 4.8** (1M context) running in Claude Code on **21 July 2026**,
via a multi-agent workflow over `accuracy-canon.md` — a bible-as-law accuracy canon
pinning every date, formula, notation choice, glossary term, Handbook anchor, and
copyright determination in the book — reusing the production machinery of its sibling
project, **[The Long Light](https://github.com/Atvriders/the-long-light)**.

| | |
|---|---|
| **Sections** | 10 (Prologue + 8 chapters + Epilogue) |
| **Words** | 72,162 |
| **Figures** | 36 (all original — hand-authored SVG schematics + matplotlib-plotted curves) |
| **Agents** | ~42: a 5-agent accuracy-canon workflow, an 11-agent figure-generation workflow, a 14-agent chapter-writing + technical-audit workflow (10 writers + 4 span auditors), plus 9 TDD'd tooling subagents and 3 research/front-matter agents |
| **Content-build workflow tokens** | 4.04 million (canon 0.44M · figures 1.21M · chapters 2.39M) |
| **Total subagent tokens** | ≈ 4.73 million (measured; excludes the orchestrator's own tokens) |
| **Workflow wall time** | ≈ 78 min for the three content workflows (canon ≈ 26 min · figures ≈ 22 min · chapters ≈ 30 min); ≈ 90 min including the tooling and research agents |

Measured at ship: the three content-build workflows consumed **4.04 million tokens**;
the full agent fleet (~42 agents including tooling, research, and front-matter) consumed
**≈ 4.73 million tokens** over roughly **90 minutes** of agent wall time. These count
subagent work only; the orchestrating session's own tokens are additional.
