"""Figure registry loader/validator for the 200 Meters and Down book build.

The registry (figures/figures.json) is a JSON object mapping figure id ->
entry, where an entry has the fields:

    id       (str)
    chapter  (int, 0..9)
    number   (str)   e.g. "6.1"
    caption  (str)
    kind     (str)   "original" | "archival-PD"
    source   (str)
    file     (str)   path to the figure asset

Copyright rule: this project reuses vintage ARRL Handbooks. Editions from
the protected years below may never be reproduced, so any "archival-PD"
figure whose source mentions one of those years is invalid.
"""

import json
from pathlib import Path

REQUIRED_FIELDS = ("id", "chapter", "number", "caption", "kind", "source", "file")
VALID_KINDS = ("original", "archival-PD")
PROTECTED_YEARS = ("1968", "1974", "1976", "1977", "1981", "1983")


def load(path="figures/figures.json") -> dict:
    """Read and parse the figure registry JSON file.

    Returns an empty dict if the file is missing or empty.
    """
    p = Path(path)
    if not p.exists():
        return {}
    text = p.read_text(encoding="utf-8").strip()
    if not text:
        return {}
    return json.loads(text)


def validate(reg: dict) -> list:
    """Validate a figure registry dict, returning a list of error strings.

    An empty list means the registry is valid. This function checks only
    metadata rules (required fields, kind, chapter range, unique numbers,
    original->svg, archival-PD->no protected-year source); it does NOT
    check that `file` exists on disk.
    """
    errors = []
    seen_numbers = {}

    for fig_id, entry in reg.items():
        missing = [f for f in REQUIRED_FIELDS if f not in entry]
        if missing:
            errors.append(
                f"{fig_id}: missing required field(s): {', '.join(missing)}"
            )
            continue

        kind = entry["kind"]
        if kind not in VALID_KINDS:
            errors.append(
                f"{fig_id}: invalid kind '{kind}' (must be one of {VALID_KINDS})"
            )

        chapter = entry["chapter"]
        if not isinstance(chapter, int) or isinstance(chapter, bool) or not (0 <= chapter <= 9):
            errors.append(f"{fig_id}: chapter must be an int in 0..9, got {chapter!r}")

        number = entry["number"]
        if number in seen_numbers:
            errors.append(
                f"{fig_id}: duplicate number '{number}' (also used by {seen_numbers[number]})"
            )
        else:
            seen_numbers[number] = fig_id

        if kind == "original":
            file_ = entry["file"]
            if not str(file_).endswith(".svg"):
                errors.append(f"{fig_id}: original figure file must end in .svg, got '{file_}'")

        if kind == "archival-PD":
            source = str(entry["source"])
            for year in PROTECTED_YEARS:
                if year in source:
                    errors.append(
                        f"{fig_id}: source '{source}' references protected {year} "
                        f"edition; archival images from protected editions are "
                        f"never reproducible"
                    )

    return errors
