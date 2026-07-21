"""Verification harness ("test suite") for the finished 200 Meters and Down book.

Cross-checks the book against the accuracy canon and the production plan's
format laws, and exits non-zero if anything fails. Reuses the existing
tooling modules rather than re-implementing their logic:

    tools.figreg      -- figure registry load/validate
    tools.mathsvg      -- inline math -> SVG rendering
    tools.build_book   -- HTML assembly (TOC/anchor check)

Run as a script:

    python3 tools/audit_book.py

Consumes (all optional at this stage of the project -- the checks that
depend on missing inputs are skipped, not failed):

    chapters/ch*.md        -- chapter markdown files
    figures/figures.json   -- figure registry (via figreg.load())
    accuracy-canon.md      -- the accuracy canon / "bible"

Runs seven checks:
    1. Figure integrity      (registry refs + files-on-disk + orphans)
    2. Copyright tags        (figreg.validate)
    3. TOC/anchor consistency (build_book.build_html)
    4. Math rendering        (mathsvg.render on every $...$ span)
    5. Canon cross-check     (**FACT:** claims appear verbatim in the canon)
    6. Flagged uncertainties (no UNVERIFIED markers left in the canon)
    7. Format laws           (epigraph, How It Works, worked example, banned phrases)
"""

from __future__ import annotations

import pathlib
import re
import sys
from glob import glob

# Allow running this file directly (`python3 tools/audit_book.py`), where
# Python puts this script's own directory (tools/) on sys.path rather than
# the repo root, which would otherwise break the `tools.*` absolute imports
# below. Harmless no-op when already imported as the `tools.audit_book`
# package (e.g. under pytest, where pyproject.toml's pythonpath already
# includes the repo root).
_REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from tools.figreg import load, validate
from tools.mathsvg import render
from tools.build_book import build_html

# --------------------------------------------------------------------------
# Constants
# --------------------------------------------------------------------------

BANNED_PHRASES = ("little did they know", "in that moment", "a testament to")

_FIG_REF_RE = re.compile(r"\{\{fig:([^}]+)\}\}")
_MATH_SPAN_RE = re.compile(r"\$(.+?)\$")
_FACT_RE = re.compile(r"(?m)^\s*\*\*FACT:\*\*\s*(.+?)\s*$")
_HREF_RE = re.compile(r'href="#(ch\d\d)"')
_ID_RE = re.compile(r'id="(ch\d\d)"')
_EPIGRAPH_RE = re.compile(r'(?m)^\s*\*"')
_HOW_IT_WORKS_RE = re.compile(r"(?m)^#{2,3}\s*How It Works\s*$")
_WORKED_EXAMPLE_RE = re.compile(r">\s*\*\*Worked example")

CANON_PATH = "accuracy-canon.md"
FIGREG_PATH = "figures/figures.json"
CHAPTERS_GLOB = "chapters/ch*.md"

# Chapters exempt from the "How It Works" / worked-example format laws
# (prologue and epilogue are narrative bookends, not teaching chapters).
_EXEMPT_FROM_TEACHING_LAWS = ("ch00", "ch09")


# --------------------------------------------------------------------------
# Pure check functions (unit-tested directly)
# --------------------------------------------------------------------------

def check_banned_phrases(text: str) -> list[str]:
    """Flag any banned "moralizing"/cliche phrase in ``text`` (case-insensitive).

    Returns one error string per hit (containing the offending phrase).
    Empty list if the text is clean.
    """
    errors = []
    lowered = text.lower()
    for phrase in BANNED_PHRASES:
        if phrase in lowered:
            errors.append(f"banned phrase found: '{phrase}'")
    return errors


def check_figure_integrity(chapter_texts: list[str], registry: dict) -> list[str]:
    """Check that every ``{{fig:ID}}`` reference across ``chapter_texts`` is
    registered in ``registry``.

    Does NOT check that the registered file exists on disk -- that's a
    separate, filesystem-touching check performed in main().
    """
    errors = []
    for text in chapter_texts:
        for m in _FIG_REF_RE.finditer(text):
            fig_id = m.group(1)
            if fig_id not in registry:
                errors.append(f"figure ref '{fig_id}' is not registered in figures.json")
    return errors


# --------------------------------------------------------------------------
# main() -- runs the full audit against the real repo
# --------------------------------------------------------------------------

def main() -> int:
    errors = []
    warnings = []

    chapter_paths = sorted(glob(CHAPTERS_GLOB))
    chapter_texts = []
    for p in chapter_paths:
        chapter_texts.append(pathlib.Path(p).read_text(encoding="utf-8"))

    registry = load(FIGREG_PATH)

    canon_path = pathlib.Path(CANON_PATH)
    canon_text = canon_path.read_text(encoding="utf-8") if canon_path.exists() else None

    print("=== 200 Meters and Down: book audit ===\n")

    # 1. Figure integrity -------------------------------------------------
    print("[1/7] Figure integrity")
    fig_errors = check_figure_integrity(chapter_texts, registry)
    for e in fig_errors:
        errors.append(f"figure integrity: {e}")

    referenced_ids = set()
    for text in chapter_texts:
        for m in _FIG_REF_RE.finditer(text):
            referenced_ids.add(m.group(1))

    for fig_id, entry in registry.items():
        file_ = entry.get("file")
        if not file_ or not pathlib.Path(file_).exists():
            errors.append(f"figure integrity: '{fig_id}' file does not exist on disk: {file_!r}")

    orphans = sorted(set(registry) - referenced_ids)
    if orphans:
        for fig_id in orphans:
            warnings.append(f"figure integrity: '{fig_id}' is registered but never referenced by any chapter (orphan)")

    if not chapter_texts:
        print("  skipped (no chapters): no {{fig:ID}} refs to check")
    print(f"  {len([e for e in errors if e.startswith('figure integrity')])} error(s), {len(orphans)} orphan warning(s)")

    # 2. Copyright tags -----------------------------------------------------
    print("[2/7] Copyright tags")
    copyright_errors = validate(registry)
    for e in copyright_errors:
        errors.append(f"copyright tag: {e}")
    print(f"  {len(copyright_errors)} error(s)")

    # 3. TOC/anchors ----------------------------------------------------
    print("[3/7] TOC/anchor consistency")
    if chapter_paths:
        try:
            html = build_html(chapter_paths, registry)
            hrefs = set(_HREF_RE.findall(html))
            ids = set(_ID_RE.findall(html))
            missing = sorted(hrefs - ids)
            for m in missing:
                errors.append(f"toc/anchor: TOC link '#{m}' has no matching id=\"{m}\"")
            print(f"  {len(missing)} error(s)")
        except Exception as exc:  # noqa: BLE001 -- surface build failures as audit failures
            errors.append(f"toc/anchor: build_html raised: {exc}")
            print(f"  1 error(s) (build_html raised)")
    else:
        print("  skipped (no chapters)")

    # 4. Math -------------------------------------------------------------
    print("[4/7] Math rendering")
    math_errors = 0
    if chapter_texts:
        for path, text in zip(chapter_paths, chapter_texts):
            for m in _MATH_SPAN_RE.finditer(text):
                expr = m.group(1)
                try:
                    render(expr)
                except Exception as exc:  # noqa: BLE001
                    math_errors += 1
                    errors.append(f"math: {path}: '{expr}' failed to render: {exc}")
        print(f"  {math_errors} error(s)")
    else:
        print("  skipped (no chapters)")

    # 5. Canon cross-check --------------------------------------------------
    print("[5/7] Canon cross-check (**FACT:** claims)")
    if canon_text is None:
        print("  skipped (no canon)")
    elif not chapter_texts:
        print("  skipped (no chapters)")
    else:
        fact_errors = 0
        for path, text in zip(chapter_paths, chapter_texts):
            for m in _FACT_RE.finditer(text):
                claim = m.group(1).strip()
                if claim not in canon_text:
                    fact_errors += 1
                    errors.append(f"canon cross-check: {path}: FACT not found verbatim in canon: {claim!r}")
        print(f"  {fact_errors} error(s)")

    # 6. Flagged uncertainties -----------------------------------------
    print("[6/7] Flagged uncertainties")
    if canon_text is None:
        print("  skipped (no canon)")
    else:
        unverified_count = canon_text.count("UNVERIFIED")
        if unverified_count:
            errors.append(f"flagged uncertainties: {unverified_count} UNVERIFIED marker(s) remain in {CANON_PATH}")
        print(f"  {unverified_count} error(s)")

    # 7. Format laws ------------------------------------------------------
    print("[7/7] Format laws")
    if not chapter_paths:
        print("  skipped (no chapters)")
    else:
        format_errors = 0
        for path, text in zip(chapter_paths, chapter_texts):
            stem = pathlib.Path(path).stem
            if not re.match(r"^ch0[0-9]$", stem):
                continue

            top_lines = "\n".join(text.splitlines()[:8])
            if not _EPIGRAPH_RE.search(top_lines):
                format_errors += 1
                errors.append(f"format law: {path}: no epigraph block found near the top")

            if stem not in _EXEMPT_FROM_TEACHING_LAWS:
                if not _HOW_IT_WORKS_RE.search(text):
                    format_errors += 1
                    errors.append(f"format law: {path}: missing '### How It Works' (or '## How It Works') subhead")
                if not _WORKED_EXAMPLE_RE.search(text):
                    format_errors += 1
                    errors.append(f"format law: {path}: no worked-example blockquote ('> **Worked example')")

            phrase_errors = check_banned_phrases(text)
            for pe in phrase_errors:
                format_errors += 1
                errors.append(f"format law: {path}: {pe}")

        print(f"  {format_errors} error(s)")

    # ----------------------------------------------------------------
    print("\n=== Report ===")
    if warnings:
        print(f"\n{len(warnings)} warning(s):")
        for w in warnings:
            print(f"  WARN: {w}")

    if errors:
        print(f"\n{len(errors)} error(s):")
        for e in errors:
            print(f"  FAIL: {e}")
        print(f"\nAudit FAILED: {len(errors)} error(s), {len(warnings)} warning(s).")
        return 1

    print(f"\nAudit PASSED: 0 errors, {len(warnings)} warning(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
