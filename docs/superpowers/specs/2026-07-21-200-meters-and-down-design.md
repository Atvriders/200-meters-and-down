# 200 Meters and Down — Design Spec

**Full title:** *200 Meters and Down: A Technical History of Amateur Radio*
**Type:** Educational nonfiction — a rigorous technical history of ham radio
**Date:** 2026-07-21
**Status:** Design approved; awaiting spec review before implementation planning.

This is **Book 1 of a three-book program** of educational ham radio books:

1. **200 Meters and Down — A Technical History of Amateur Radio** *(this spec — built first)*
2. Technician primer + exam prep, targeting the current **2026–2030 Technician question pool**
3. General + Extra (upgrade path) / all-classes reference

Books 2 and 3 are deferred; each will get its own brainstorm → spec → plan → build cycle. This document covers Book 1 only.

---

## 1. Purpose & audience

A single-volume **technical history of amateur radio** for the **technical enthusiast / ham** — a reader who wants both the engineering rigor (schematics, formulas, worked examples) *and* the human story, told in one continuous chronological narrative.

Every era-chapter does two jobs at once:
- **Teaches how that era's radio technology actually works**, to real depth.
- **Tells that era's human and regulatory story** — the people, organizations, and laws.

**Spine (the book's organizing idea):** *how amateurs turned each generation's technology into ever-longer reach* — from a spark heard across town to FT8 decoded 20 dB beneath the noise floor. This is the nonfiction analogue of The Long Light's "keeping the light" spine.

**Non-goals:** This is **not** an exam-prep book (that is Book 2). It does not aim to certify a reader for a license; it aims to make them *understand* the art and its history.

## 2. Relationship to The Long Light (what we reuse)

Book 1 reuses The Long Light's **production machinery and disciplines**, not its content:

| Reused from The Long Light | Retargeted to |
|---|---|
| `AI-CONTEXT.md` "story bible as law" | **`accuracy-canon.md`** — verified facts/dates/values/notation as law (§6) |
| Log-entry epigraph device | **Period-artifact epigraphs** from the era's anchor Handbook (§5) |
| 31 parallel chapter-writers + 4 continuity auditors | **8 chapter-writers + figure agents + technical-accuracy auditors** (§8) |
| `chapters/*.md` → single-file HTML/PDF/TXT build | Same build + **embedded SVG figures & rendered math** (§9) |
| edge-tts 8-voice audiobook + themed player | Same pipeline + a **narration transform** for formulas/figures (§9) |
| Docker/nginx serve + dual-homed Gitea/GitHub + CI | Same, as `Atvriders/200-meters-and-down` (§9) |

**Explicitly NOT reused:** The Long Light's literary style laws (underwrite big moments, no morals, sparing exposition). An educational book wants the opposite — explicit, worked, repeated-for-retention. Only the *epigraph device* and the *"chapter ends on a forward hook, never a moral"* rule carry over.

## 3. Source materials

**Primary archive (owned, from the callbook project):** 13 editions of the ARRL *Radio Amateur's Handbook* at `/home/kasm-user/leehite-callbooks/handbooks-arrl/` — years **1927, 1931, 1933, 1936, 1940, 1941, 1951, 1968, 1974, 1976, 1977, 1981, 1983**. Each is a state-of-the-art snapshot of its year and serves as the "primary source artifact" anchoring its era.

**Supporting owned material:** `A History of Amateur Radio License Changes.pdf`, `An Overview of Amateur Call Signs Past and Present (1994)`, the ARRL operating-event explainers in `arrl-calendar/src/data/rules.ts`, and a 31-question public-domain FCC pool sample in `ham-radio-clicker/src/data/questions.ts` (more relevant to Book 2, noted for reuse).

**External cross-reference (required):** ARRL history pages, Wikipedia "Amateur radio history," ITU/FCC records, IEEE/history-of-technology sources. Every load-bearing fact is cross-referenced against at least one authoritative external source, per §6.

## 4. Chapter outline (10 sections, ~90–120k words, ~40+ figures)

Core era-chapters run ~8,000–12,000 words each. Eras are technological, so spans overlap slightly at the seams (a technology is born before it defines an era).

| # | Title | Span | Core technology taught | Handbook anchor |
|---|---|---|---|---|
| 00 | **Prologue — Before the Amateurs** | 1864–1900 | Maxwell → Hertz; the radiated EM wave (E⊥H⊥propagation); resonance & the LC circuit; c = fλ | *(pre-series)* |
| 1 | **The Spark Era** | 1900–1917 | Spark-gap + LC tank, damped waves & why they're broadband; coherer → electrolytic → crystal (cat's-whisker) detectors; Q; ground-wave; inverted-L antenna | *(pre-1926)* |
| 2 | **The Shortwave Revolution** | 1919–1927 | Triode/audion as amp & oscillator; **regeneration** (tickler feedback); Hartley/Colpitts; MOPA; BFO; **ionospheric skip & the skip zone** | **1927** |
| 3 | **The Golden Age of Tubes** | 1928–1936 | **Crystal control** (Pierce) & multiplier chains; the **superheterodyne** in depth (mixing, image freq, IF, AGC); AM plate modulation & spectrum; pentodes & neutralization | **1931, 1933, 1936** |
| 4 | **On the Eve of War** | 1937–1945 | Class-C amps & **pi-network** matching; crystal IF filters; **Yagi-Uda beams** (gain, F/B); HF-skip vs VHF line-of-sight/tropo | **1940, 1941** |
| 5 | **The Postwar Reinvention** | 1945–1960 | **SSB two ways — filter vs phasing method**; balanced modulator & product detector; the transistor & BJT common-emitter stages | **1951** |
| 6 | **Reaching for Space** | 1961–1976 | **FM** (deviation, Carson's rule, capture effect, discriminator); **repeater duplex** (offset, CTCSS); **satellites** (transponders, uplink/downlink, **Doppler**) | **1968, 1974, 1976** |
| 7 | **The Microprocessor & First Digital Modes** | 1977–1990 | **PLL frequency synthesis** (VCO/phase-detector/divider); **AX.25 packet** (framing, callsign+SSID, CRC, ARQ, digipeating, Bell 202 1200-baud AFSK); AMTOR/RTTY | **1977, 1981, 1983** |
| 8 | **The Digital, Networked & Software-Defined Era** | 1991–present | **SDR/DSP** (I/Q sampling, direct conversion, FFT waterfall); **PSK31** (BPSK + varicode) vs **FT8** (8-FSK, LDPC FEC, decode ~20 dB under noise); digital voice & internet linking | *(post-archive; modern refs + PD Part 97)* |
| 09 | **Epilogue — Where the Art Is Heading** | present → | Geostationary transponders (QO-100-style), mesh / ham-over-IP, ML-assisted decoding, demographics & spectrum defense | — |

### Key milestones pinned into the narrative (verified in research pass)
- **Radio Act of 1912** (signed Aug 13, 1912): first US federal licensing; amateurs confined to **"200 meters and down"** (wavelengths *shorter* than 200 m / frequencies *above* 1500 kHz) — the banishment that accidentally forced the discovery of shortwave DX, and the book's title.
- **ARRL founded April 6, 1914** by Hiram Percy Maxim (1AW) & Clarence Tuska, Hartford CT.
- **WWI shutdown April 6, 1917.**
- **ARRL Transatlantic Tests** Dec 1921 (Godley/2ZE copies 1BCG); **first two-way transatlantic Nov 27, 1923** (Deloy F-8AB ↔ US 1MO/1XAM).
- **IARU founded April 1925, Paris** (Maxim first president).
- **Radio Act of 1927 → FRC; Communications Act of 1934 → FCC.**
- **WWII shutdown Dec 8, 1941; WERS June 1942.**
- **1951 FCC license restructuring** (Novice/Technician/General/Conditional/Advanced/Amateur Extra).
- **OSCAR 1 launched Dec 12, 1961** (first non-government satellite); **AMSAT founded 1969.**
- **Incentive licensing effective Nov 22, 1968** — FCC-initiated (Docket 15928) and contentious; **not** an ARRL program (framing matters).
- **No-code Technician 1991; FCC ends all Morse testing Feb 23, 2007.**
- **PSK31 (G3PLX, 1998); WSJT-X/FT8 released June 29, 2017** (Taylor K1JT & Franke K9AN).

### Geographic lens
US/ARRL as the main spine (the archive's natural lens) + **"Meanwhile, Worldwide" sidebars** for load-bearing global milestones: Maxwell/Hertz/Marconi, Deloy's 1923 contact, IARU, ITU/WARC/WRC spectrum & Morse decisions, PSK31 (G3PLX, UK), the international OSCAR fleet. The physics and modes are global even when the licensing story is American.

## 5. Per-chapter anatomy (the "format laws")

Every core chapter follows one skeleton so parallel writers produce a coherent book:

1. **Period-artifact epigraph** — a short quoted line or figure from the era's anchor Handbook (or a period source pre-1926), attributed (e.g. *"— The Radio Amateur's Handbook, 1927"*). The recurring device; the analogue of The Long Light's log epigraphs.
2. **The Story** — narrative history of the era: people, organizations, events, regulation. US/ARRL spine + "Meanwhile, Worldwide" sidebars.
3. **How It Works** — the rigorous technical teaching: the defining circuits and physics, with numbered figures, formulas in the canon's notation, and at least one **worked example** ("trace/build this stage").
4. **The State of the Art in [year]** — a tight "as the Handbook shows it" snapshot: what a ham of that year actually built and operated, tied to the anchor edition.
5. **Forward hook** — the unsolved technical tension that drives the next era. Chapters end on that hook, an image, or an artifact — **never a moral summary**, never "little did they know."

## 6. The accuracy canon (`accuracy-canon.md`) — law for all agents

The nonfiction analogue of The Long Light's story bible. Every writer and auditor conforms to it exactly:

- **Pinned timeline** — verified dates/values/events (seeded from §4 and the research pass), each with its authoritative source.
- **Notation & units standard** — one consistent symbol set across all chapters; a **units/formulas appendix**.
- **Glossary** — canonical definition for every technical term.
- **Per-era anchor mapping** — which Handbook edition backs which chapter.
- **Copyright ledger** (§7) — the authoritative record of what may be reproduced.
- **Flagged uncertainties (verify before print, never guess):**
  1. Exact 1919 WWI **transmitting**-restoration month (working value: Oct 1, 1919; receiving lifted ~April 1919).
  2. Per-band **WARC** US release dates (30 m ~1982 solid; 17 m & 12 m later in the 1980s — confirm each).
  3. **Incentive-licensing** framing — FCC-initiated & contentious, not an ARRL program.
  4. **IARU** founding (April 1925, Paris, Maxim president) — high confidence, re-verify.

**Correctness rule:** any fact, date, formula value, or band edge that appears in a chapter must trace to the canon; the canon traces to an authoritative source. Auditors enforce this (§8).

## 7. Copyright discipline (load-bearing)

- **Prose is always original.** We learn from the Handbooks and cross-reference ARRL/online; we never copy expression.
- **Facts, dates, and physics are free** to teach. **FCC Part 97** and the **published FCC/NCVEC question pools** are public-domain-status and freely quotable/reproducible.
- **Archival image reproduction — posture chosen: "safe + opportunistic unlock":**
  - **1927 edition = confirmed public domain** (US 1927 works entered PD Jan 1, 2023). Freely reproducible. ✅
  - **1928–1963 editions (1931/1933/1936/1940/1941/1951):** presumed protected **unless** a per-edition **pre-1964 copyright-renewal check** (Stanford Copyright Renewal DB / US Copyright Office) shows the renewal lapsed — in which case the edition is PD and reproducible. **Verify per edition; never assume.**
  - **1964–1983 editions (1968/1974/1976/1977/1981/1983):** protected (auto-renewal / post-1978 term). **No reproduction.**
- **Every figure is tagged** in the canon as `original` (our SVG/plot) or `archival-PD` (with its verified PD source). Auditors reject any protected image.

## 8. Production architecture (multi-agent workflow)

Mirrors The Long Light's orchestration, retargeted from narrative continuity to **technical correctness**:

1. **Orchestration** builds `accuracy-canon.md` and the 10 chapter specs.
2. **8 parallel chapter-writer agents** — each fed the canon, the whole arc, its chapter spec, its neighbors' beats, and OCR'd excerpts of its anchor Handbook edition(s). (Prologue & epilogue written alongside.)
3. **Figure-generation agents** — author original SVG schematics/block-diagrams/antenna-patterns and code-plotted waveforms/curves per the figure list; pull verified-PD archival artifacts where the ledger allows.
4. **Technical-accuracy auditor agents** over chapter spans — verify every formula, date, value, and band edge against the canon; cross-check against external sources; enforce the format laws (§5); check every figure's copyright tag (§7); edit surgically.
5. **Copyright-renewal research** (opportunistic, §7) — per-edition checks to unlock more archival images.
6. **Typeset build** (§9).

Independent-task fan-out follows the user's standing preference (parallel agents while building; a single commit at the end of the full build after verification).

## 9. Deliverables & build

- **The book:** `chapters/ch00.md … ch09.md` (+ `figures/*.svg`) → a single self-contained **HTML** edition (embedded SVG, rendered math, linked TOC, light/dark themes) → **PDF** (headless Chromium on Linux) → **TXT** (de-marked concatenation). Mirrors The Long Light's typeset pipeline.
- **Repo & hosting:** `Atvriders/200-meters-and-down`, dual-homed Gitea + GitHub, **Docker/nginx** image, CI on push to `main` — the user's standard pattern. All repos/packages public.
- **Audiobook:** `tools/make_audiobook.py` retargeted with a **narration transform** — formulas spoken in words ("E equals I times R"); each figure announced with a one-line authored spoken description ("Figure 4 shows…") so equations/diagrams degrade gracefully in audio. edge-tts, 8 voices (US/British/Australian/Irish × M/F), lantern-style player. Large audio attached to a release, not committed to git.
- **`AI-CONTEXT.md`** — a **full machine-oriented context dump**, matching The Long Light's convention: the complete book bible (the accuracy canon, the chapter-by-chapter outline, the pinned timeline & facts, style/format laws, the copyright ledger, production history, and infrastructure notes) — everything needed to understand, extend, adapt, or continue *200 Meters and Down* without contradicting the finished book. Credentials/tokens omitted.
- **`README.md`** — front-page overview + formats table + Docker/audiobook instructions, and a **"How it was made" stats block** mirroring The Long Light's: number of agents, **total tokens consumed**, **workflow wall-clock time**, **end-to-end time**, and word/figure counts. These production stats are captured at build time and **written into the README when the repo is pushed to GitHub.**

## 10. Verification (what "done" means)

Not unit tests, but a real gate — nothing ships until all pass:
1. **Auditor pass** — facts, formulas, dates, and band edges reconciled against the canon and external sources; format laws satisfied.
2. **Build check** — HTML/PDF/TXT render; all figures present and embedded; every TOC link resolves; all math renders.
3. **Copyright-tag check** — no protected image reproduced; every `archival-PD` figure has a verified PD source in the ledger.
4. **Flagged-uncertainties check** — every §6 flag resolved to a sourced value before print.

## 11. Open items / risks

- **PDF on Linux:** The Long Light rendered PDF via headless Edge on Windows; here we'll use headless Chromium/Chrome. Confirm availability during implementation; fall back to a Node/Puppeteer or wkhtmltopdf path if needed.
- **OCR quality:** older Handbook scans OCR poorly; where an anchor excerpt is needed as an epigraph or fact source, budget for targeted re-OCR or manual transcription of the specific passage.
- **Math rendering in a self-contained HTML:** must inline the math (pre-rendered SVG/MathML) so the single-file/CSP constraints hold — no external MathJax CDN.
- **Chapter 8 & prologue have no owned Handbook anchor** — they lean on external + modern references and PD Part 97; the epigraph device uses a period source instead of an owned edition.

## Appendix A — Per-chapter capsules (story beats + figures)

**Prologue (1864–1900):** Maxwell's equations (1864/1873); Hertz demonstrates EM waves (1887); Marconi's practical wireless (1895) & first transatlantic signal (Dec 1901). *Figures:* Hertz spark-oscillator/resonator; EM-wave field diagram; c = fλ nomograph across the ham bands.

**Ch1 Spark (1900–1917):** pre-1912 unlicensed boom (~10,000 stations); *Titanic* (1912) → Radio Act of 1912; ARRL founded 1914; WWI shutdown 1917. *Figures:* spark-gap TX schematic; damped-wave vs pure-CW waveform; crystal/cat's-whisker detector; inverted-L over ground.

**Ch2 Shortwave (1919–1927):** transmitting restored ~Oct 1919; Armstrong regeneration & superhet mature; tube kills spark; transatlantic tests 1921–23; IARU 1925; FRC 1927. *Figures:* regenerative RX (tickler loop); Hartley oscillator; ionospheric skip/skip-zone; the 1BCG transmitter (historical).

**Ch3 Golden Age of Tubes (1928–1936):** HF band structure settles (80/40/20/10 m); crystal control spreads; superhet standard; AM phone grows; FCC 1934; the Handbook becomes "the bible." *Figures:* superhet block diagram w/ conversion math; Pierce crystal oscillator; plate-modulated AM stage + spectrum; pentode element diagram.

**Ch4 Eve of War (1937–1945):** bigger PAs & selectivity; first VHF push (5 m, 2½ m); Armstrong wideband FM exists; WWII shutdown 1941; WERS 1942; wartime radar/VHF/FM R&D. *Figures:* pi-network matching; Yagi geometry + azimuth pattern; class-C plate-current waveform; crystal IF filter response.

**Ch5 Postwar (1945–1960):** surplus boom; SSB via phasing (Norgaard, 1948) & the "sideband wars"; transistor (1947) → first solid-state rigs; 1951 license restructuring; the transceiver. *Figures:* filter-method vs phasing-method SSB (side by side); SSB vs AM spectrum; NPN common-emitter + mechanical-filter cutaway.

**Ch6 Space (1961–1976):** OSCAR 1 (1961); AMSAT (1969); OSCAR 6/7 transponders; 2 m FM repeater explosion; incentive licensing (1968, FCC-initiated, divisive); PLL synthesis begins. *Figures:* FM discriminator; repeater duplex/offset; Doppler-vs-time over a pass; linear-transponder block diagram.

**Ch7 Microprocessor & Digital Dawn (1977–1990):** synthesized microprocessor radios; packet/AX.25 & TNCs; AMTOR/RTTY; WARC-79 bands reach US hams (30 m ~1982, 17/12 m later). *Figures:* PLL synthesizer block; AX.25 frame; Bell 202 1200-baud AFSK modem; packet/digipeater topology.

**Ch8 Digital/SDR (1991–present):** no-code Tech (1991); PSK31 (G3PLX, 1998); ITU drops Morse mandate (WRC-2003) → FCC ends Morse testing (2007); SDR mainstream (FlexRadio 2003, SoftRock, RTL-SDR); D-STAR/DMR/Fusion & EchoLink/IRLP; WSJT-X/FT8 (2017) overtakes CW/SSB. *Figures:* SDR I/Q direct-conversion RX; FFT waterfall; PSK31 BPSK constellation + varicode; FT8 15-second time/frequency sequence.

**Epilogue (present →):** geostationary transponders, mesh/ham-over-IP, ML-assisted decoding, aging demographics & spectrum defense.

## Appendix B — Key sources (from research pass)
ARRL: Ham Radio History; WWI blackout centennial; Transatlantic Tests; SSB history (McElroy); 2017 digital-modes evaluation. Wikipedia: History of amateur radio; Radio Acts 1912/1927; Communications Act 1934; OSCAR 1; WARC bands; FT8; WSJT. Licensing: EMA-ARRL license-change history; OnAllBands Novice history. Tech: Internet Archive 1926 1st-ed Handbook; Armstrong regeneration/superhet; AMSAT-UK satellite timeline; SDR-in-amateur-radio. Copyright: LoC 1930-works-PD; Public Domain Day 2026.
