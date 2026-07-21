# AI-CONTEXT — 200 Meters and Down

This document is a complete, machine-oriented context dump for AI models (and humans)
working with this repository. It contains everything needed to understand, extend,
adapt, or continue *200 Meters and Down* without contradicting the finished book: what
the book is, its governing accuracy canon, the chapter-by-chapter outline, the
format/style laws, the figure system, the production history, and the infrastructure
around the book. Treat **`accuracy-canon.md`** as law — the published chapters already
conform to it exactly, and this file only summarizes it.

Credentials, API tokens, and personal contact details from the production session are
deliberately omitted.

---

## 1. What this is

*200 Meters and Down: A Technical History of Amateur Radio* is a **~72,000-word**
(72,162 words, per the chapter markdown) technical history of amateur radio, in **ten
sections**: a Prologue, eight era-chapters running spark to software-defined radio, and
an Epilogue. It was written **21 July 2026** by **Claude Opus 4.8** (1M context)
orchestrating a multi-agent workflow in Claude Code.

The audience is the **technical enthusiast / ham** — a reader who wants engineering
rigor (schematics, formulas, worked examples) *and* the human and regulatory story,
told as one continuous chronological narrative. Every era-chapter teaches how that
era's radio technology actually works *and* tells that era's history: the people,
organizations, and laws.

This is **Book 1 of a planned three-book educational program**:

1. **200 Meters and Down — A Technical History of Amateur Radio** *(this book)*
2. A Technician exam-prep primer targeting the 2026–2030 Technician question pool
3. A General + Extra (upgrade path) / all-classes reference

Books 2 and 3 are not started; each gets its own brainstorm → spec → plan → build
cycle. This book is **not** exam prep and does not aim to certify a reader for a
license — it aims to make the art and its history understood.

## 2. The spine / thesis

The book's organizing idea: **how amateurs turned each generation's technology into
ever-longer reach** — from a spark heard across town to FT8 decoded roughly 20 dB
beneath the noise floor. Every era-chapter reframes its circuits and its history
through that same lens: what could this generation of hams hear, and how far, that the
last generation could not. It is the nonfiction analogue of The Long Light's "keeping
the light" spine (see §7) — one throughline that survives ten independently drafted
chapters spanning 160+ years.

## 3. The accuracy canon is LAW

**`accuracy-canon.md`** is the single, binding source of truth for every date, number,
notation choice, glossary definition, per-era Handbook anchor, and copyright
determination in the book. Every chapter writer, illustrator, and auditor conformed to
it exactly; where a draft chapter ever disagreed with the canon, the canon won. **Prose
is always original — the canon and the Handbooks are learned from and cross-referenced,
never copied.** Facts, dates, physics, and FCC Part 97 / question-pool content are free
to teach.

Summary of what the canon pins down (read the file itself before adding or changing any
fact):

- **Pinned timeline** — 80 dated entries, Maxwell's 1864 Royal Society paper through
  FT8's 29 June 2017 release, each with a citable source. Four previously-contested
  facts are explicitly resolved in a **Resolved Uncertainties** section (1919
  transmitting-restoration date, WARC-79 band access dates, the Incentive Licensing
  origin/framing, and the IARU founding date) — no open uncertainty markers remain
  anywhere in the canon; the build audit greps for this.
- **Notation & Units** — one consistent symbol set for the whole book (f, λ, c, E/I/R
  for Ohm's law, Q, f_RF/f_LO/f_IF, Δf, β, BW, SSID, dB/dBm, etc.), each with its
  canonical formula (e.g. **c = f·λ**, **f₀ = 1/(2π√(LC))**, **f_IF = |f_RF − f_LO|**,
  Carson's rule **BW = 2(Δf + f_m)**, Doppler **Δf = f·v/c**, PLL **f_VCO = N·f_ref**).
- **Glossary** — 60 canonical one-sentence definitions, from *spark gap* and *coherer*
  through *LDPC* and *vocoder*; a chapter may expand a term but must not contradict its
  canon definition.
- **Per-era Handbook anchor map** — which ARRL *Radio Amateur's Handbook* edition(s)
  ground each chapter's technical claims and illustrations:

  | Chapter | Owned Handbook edition(s) |
  |---|---|
  | Prologue | none (pre-Handbook) |
  | Ch 1 — The Spark Era | none (pre-1926) |
  | Ch 2 — The Shortwave Revolution | 1927 |
  | Ch 3 — The Golden Age of Tubes | 1931, 1933, 1936 |
  | Ch 4 — On the Eve of War | 1940, 1941 |
  | Ch 5 — The Postwar Reinvention | 1951 |
  | Ch 6 — Reaching for Space | 1968, 1974, 1976 |
  | Ch 7 — The Microprocessor and the First Digital Modes | 1977, 1981, 1983 |
  | Ch 8 — The Digital, Networked, and Software-Defined Era | none (post-archive; modern refs + public-domain FCC Part 97) |
  | Epilogue | — |

- **Copyright ledger** — of the 13 owned Handbook editions, **7 are public domain and
  reproducible: 1927, 1931, 1933, 1936, 1940, 1941, 1951** (each affirmatively
  evidenced — either pre-1928 age or a confirmed absence of any 28-year renewal in the
  US Copyright Office's Catalog of Copyright Entries). The **6 editions spanning
  1968–1983 are protected** (automatic renewal or current-law 95-year term) and **must
  never be reproduced** — no archival image, no scanned schematic, no quoted running
  text from those six. Chapters 6 and 7, which are anchored to protected editions,
  teach from them but illustrate only with original redrawn diagrams or public-domain
  equivalents.

## 4. Chapter-by-chapter outline

| # | Heading (exact) | Era span | Core technology taught |
|---|---|---|---|
| 00 | Prologue — Before the Amateurs | 1864–1900 | Maxwell's equations; **c = f·λ**; LC resonance (f₀ = 1/2π√LC); Hertz's damped-oscillator apparatus; the coherer detector; Marconi's grounded antenna/earth return; no modulation yet — everything is on/off keying of a damped carrier |
| 01 | The Spark Era | 1900–1917 | Spark-gap transmitter / LC tank; why damped waves are inherently broadband; the crystal ("cat's-whisker") detector superseding the coherer; Q and selectivity; ground-wave propagation; the 200 m ⇔ 1500 kHz numeric anchor |
| 02 | The Shortwave Revolution | 1919–1927 | The triode as amplifying/oscillating device; regeneration (tickler feedback); CW vs. damped spark; the heterodyne principle and BFO; the superheterodyne (f_IF = \|f_RF − f_LO\|); MOPA; Hartley and Colpitts oscillators; ionospheric skip and the skip zone |
| 03 | The Golden Age of Tubes | 1928–1936 | The superheterodyne becomes dominant; image frequency; the IF strip; AGC; AM via plate modulation and its ≈2×audio bandwidth; pentode tubes; neutralization; the Pierce crystal oscillator |
| 04 | On the Eve of War | 1937–1945 | Class-C amplifiers (~60–80%+ efficiency); the pi-network output match; crystal IF filters; the Yagi–Uda beam; HF skip vs. VHF line-of-sight; FM fundamentals (deviation, not amplitude) |
| 05 | The Postwar Reinvention | 1945–1960 | SSB two ways — filter method vs. phasing method — both from a balanced modulator producing DSBSC; the product detector; the BJT common-emitter stage; the Collins KWM-1 as anchor rig |
| 06 | Reaching for Space | 1961–1976 | FM deviation and Carson's rule (BW = 2(Δf+f_m)); the capture effect; the discriminator; repeater duplex offset and CTCSS; satellite linear transponders (OSCAR 6/7); Doppler shift (Δf = f·v/c) |
| 07 | The Microprocessor and the First Digital Modes | 1977–1990 | PLL frequency synthesis (f_VCO = N·f_ref); the AX.25 packet protocol (HDLC framing, callsign+SSID, CRC-CCITT, ARQ, Bell 202 1200-baud AFSK); digipeaters; AMTOR |
| 08 | The Digital, Networked, and Software-Defined Era | 1991–present | SDR/DSP fundamentals (I/Q sampling, direct conversion, FFT waterfall); PSK31 (31.25-baud BPSK, Varicode); FT8 (8-FSK, (174,91) LDPC, ~−20 to −24 dB SNR decode); digital-voice vocoders (D-STAR/DMR/Fusion) |
| 09 | Epilogue — Where the Art Is Heading | 2026 → | Geostationary transponders (QO-100-style), mesh / ham-over-IP, ML-assisted decoding, demographics and spectrum defense |

Geographic lens: US/ARRL is the main spine (the natural lens of the owned Handbook
archive), with **"Meanwhile, Worldwide"** sidebars carrying the load-bearing global
milestones — Maxwell/Hertz/Marconi, Deloy's 1923 transatlantic contact, the IARU,
ITU/WARC/WRC spectrum and Morse decisions, PSK31 (G3PLX, UK), and the international
OSCAR fleet.

## 5. Format / style laws

Every core chapter (01–08; the Prologue and Epilogue follow the same skeleton minus the
Handbook-anchored parts) follows one fixed skeleton so ten independently drafted
chapters read as one book:

1. **Exact `##` heading** — the heading text is canon; do not reword it.
2. **Epigraph** — either a **genuine, sourced quotation** or a **plainly factual period
   datum with attribution** (e.g. a Handbook figure or a dated fact, attributed to its
   source and year). **Never a fabricated quote.** This is the load-bearing integrity
   rule of the whole book: nothing in an epigraph position may be invented dialogue or
   invented text presented as real.
3. **`### The Story`** — narrative history: people, organizations, events, regulation.
   Includes a **`> **Meanwhile, Worldwide:**`** sidebar carrying that era's global
   (non-US) milestone.
4. **`### How It Works`** — rigorous technical teaching. Formulas are written inline as
   `$...$` in the canon's notation (rendered to SVG at build time by `tools/mathsvg.py`;
   never a bare Unicode approximation). Figures are referenced as `{{fig:id}}` and
   resolved against the figure registry. Includes a **`> **Worked example:**`** block
   that traces or builds a real stage (e.g. "trace this superhet's image frequency").
5. **`### The State of the Art in <year>`** — a tight, Handbook-anchored snapshot: what
   a ham of that year actually built and operated.
6. **Forward hook ending** — the chapter ends on the unsolved technical tension driving
   the next era: an image, an artifact, an open question. **Never a moral summary.**
   Banned phrases (checked by the audit): *"little did they know"*, *"in that moment"*,
   *"a testament to"*.
7. **3–5 `**FACT:**` lines**, copied **verbatim** from `accuracy-canon.md`. The build
   audit (`tools/audit_book.py`, check 5) greps every `**FACT:**` line in every chapter
   against the canon text and fails the build if any doesn't match exactly — this is
   the mechanical enforcement that keeps prose from silently drifting off the pinned
   facts.

Only two devices carry over from The Long Light's fiction style laws: the epigraph
device itself, and "end on a forward hook, never a moral." Everything else about this
book's voice is the opposite of The Long Light's — explicit, worked, and repeated for
retention rather than underwritten.

## 6. Figures

**36 original figures** (`figures/figures.json` is the registry; `figures/*.svg` the
assets), a mix of:

- **Hand-authored SVG schematics/diagrams** — e.g. `spark-tx.svg`, `superhet-block.svg`,
  `pi-network.svg`, `yagi.svg`, `ax25-frame.svg`, `sdr-iq.svg`, `pll.svg`.
- **Matplotlib-plotted curves**, generated by paired `_gen_<id>.py` scripts and
  committed as static SVG — e.g. `_gen_damped-vs-cw.py` → `damped-vs-cw.svg`,
  `_gen_doppler.py` → `doppler.svg`, `_gen_yagi-pattern.py` → `yagi-pattern.svg`,
  `_gen_ft8`-style timing/waterfall plots.

All figures are **themeable via `currentColor`** so they render correctly in both the
book's light and dark themes, and every figure is embedded inline in the built HTML
(no external image references). **No protected (1968–1983) archival Handbook image is
ever reproduced** — figures for the two chapters anchored to protected editions
(Ch 6, Ch 7) are original redraws, never scans. `tools/audit_book.py` check 1
(figure integrity) and check 2 (copyright tags) enforce this at build time via
`tools/figreg.py`'s `validate()`.

## 7. Production history

Built by reusing **The Long Light's** production machinery (`~/the-long-light`): the
same "bible/canon as law" discipline, the same `chapters/*.md` → single-file
HTML/PDF/TXT build shape, the same edge-tts 8-voice audiobook pipeline with a themed
player, and the same Docker/nginx + dual-homed Gitea/GitHub CI deployment pattern —
retargeted from narrative continuity to **technical correctness**, and from a fiction
style bible to `accuracy-canon.md`.

The content build ran as a multi-agent workflow on top of ~9 TDD'd tooling subagents
(which built `tools/build_book.py`, `audit_book.py`, `mathsvg.py`, `figreg.py`,
`narration.py`, `make_audiobook.py`, and `make_intro.py`):

- **A 5-agent accuracy-canon workflow** — researched and assembled the pinned timeline,
  notation, glossary, per-era anchor map, and copyright ledger into `accuracy-canon.md`
  before any chapter prose was drafted.
- **An 11-agent figure-generation workflow** — authored the 36 original SVG
  schematics and matplotlib-plotted curves against the figure list, respecting the
  copyright ledger (no protected-edition reproductions).
- **A 14-agent chapter-writing + technical-audit workflow** — 10 parallel
  chapter-writers (one per `chapters/ch*.md` file, each fed the canon, the whole arc,
  its own chapter spec, and its neighbors' beats) plus 4 span auditors who verified
  every formula, date, value, and band edge against the canon, checked format-law
  compliance, and edited surgically.

Roughly **4.0 million workflow tokens** were consumed across the content build (canon +
figures + chapters/audit). Exact final token and wall-clock totals for the complete
production (including orchestration, infrastructure, and audiobook generation) are
written into `README.md` at push time, following The Long Light's convention.

## 8. Infrastructure

- **`tools/build_book.py`** — parses the fixed chapter-markdown dialect and produces a
  self-contained single-file **HTML** edition (inline SVG figures, inline rendered
  math, linked TOC, light/dark themes, no external resource references), a plain
  **TXT** edition, and a best-effort **PDF** (headless Chromium/Chrome, falling back to
  weasyprint).
- **`tools/audit_book.py`** — the verification gate; runs **7 checks**: (1) figure
  integrity, (2) copyright tags, (3) TOC/anchor consistency, (4) math rendering,
  (5) canon cross-check of every `**FACT:**` line, (6) no unresolved-uncertainty
  markers left in the canon, (7) format-law compliance (epigraph, How It Works, worked
  example, banned phrases).
- **`tools/mathsvg.py`** — renders inline `$...$` math to embedded SVG.
- **`tools/figreg.py`** — loads and validates `figures/figures.json` (existence,
  copyright tags, orphan detection).
- **`tools/narration.py`** / **`tools/make_audiobook.py`** — an audiobook pipeline
  (edge-tts, **8 voices**: US/British/Australian/Irish × male/female, matching The
  Long Light's voice set) with a narration transform for formulas and figures; **
  `tools/make_intro.py`** generates a spoken introduction. `docker/audiobook-index.html`
  is the lantern/scope-themed audiobook player.
- **`appendices/formulas-and-units.md`** and **`appendices/glossary.md`** mirror the
  canon's Notation & Units and Glossary sections as the book's printed back matter.
- **Deployment** — `Dockerfile` (nginx serving `build/index.html`, the TXT/PDF,
  `chapters/`, and `audiobook/`) + `docker-compose.yml`; CI on both
  `.github/workflows/` (GitHub → `ghcr.io/atvriders/200-meters-and-down`) and
  `.gitea/workflows/` (Gitea → `git.waterburp.com/atvriders/200-meters-and-down`),
  each fetching the audiobook from release `v1.0` before building the image. Repo:
  **`Atvriders/200-meters-and-down`**, dual-homed Gitea + GitHub.

**Regenerate the book:**
```
python3 tools/build_book.py --html --txt --pdf --out build/
```

**Verify (the accuracy/format gate):**
```
python3 tools/audit_book.py
```

**Run the test suite:**
```
python3 -m pytest
```

## 9. Guidance for AI models extending this book

- **Obey `accuracy-canon.md` exactly.** It is the single source of truth for dates,
  values, notation, glossary wording, Handbook anchors, and copyright status. Do not
  re-date an event or restate a formula from a chapter draft — trace every fact back to
  the canon, and if the canon needs a new entry, add it there first, sourced, before
  touching chapter prose.
- **Keep epigraph integrity.** An epigraph is either a genuine, sourced quotation or a
  plainly factual, attributed period datum. Never fabricate a quote and present it as
  real, even for a plausible-sounding period voice.
- **Never reproduce a protected Handbook image.** The 1968, 1974, 1976, 1977, 1981, and
  1983 editions are under copyright — no scans, no traced reproductions, no quoted
  running text from them. Teach from them; illustrate only with original or
  public-domain material.
- **Run `python3 tools/audit_book.py` before considering any change done.** It is the
  mechanical enforcement of everything above (facts, format laws, figure copyright
  tags, math rendering, TOC integrity) — a change that doesn't pass it is not finished,
  regardless of how it reads.
