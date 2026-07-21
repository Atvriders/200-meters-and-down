"""Shared narration/text transforms used by the audiobook and TXT builders.

Pure-stdlib helpers for turning lightly-marked-up manuscript text into
narration-friendly plain text:

- strip_markup: drop figure refs, heading/blockquote markers, and
  emphasis markup, leaving plain prose.
- speak_math: turn inline ``$...$`` math spans into spoken English.
- speak_figures: expand ``{{fig:ID}}`` references into a spoken
  parenthetical using a supplied figure-description table.
"""

import re

# index 0 is unused ("") so that NUMBER_WORDS[n] gives the word for n.
NUMBER_WORDS = [
    "",
    "One",
    "Two",
    "Three",
    "Four",
    "Five",
    "Six",
    "Seven",
    "Eight",
    "Nine",
    "Ten",
    "Eleven",
    "Twelve",
    "Thirteen",
    "Fourteen",
    "Fifteen",
    "Sixteen",
    "Seventeen",
    "Eighteen",
    "Nineteen",
    "Twenty",
]

_ROMAN_VALUES = {
    "I": 1,
    "V": 5,
    "X": 10,
    "L": 50,
    "C": 100,
    "D": 500,
    "M": 1000,
}


def roman_to_int(s: str) -> int:
    """Convert a Roman numeral string (e.g. "XIV") to an int."""
    s = s.strip().upper()
    total = 0
    prev = 0
    for ch in reversed(s):
        val = _ROMAN_VALUES.get(ch, 0)
        if val < prev:
            total -= val
        else:
            total += val
            prev = val
    return total


_FIG_REF_RE = re.compile(r"\{\{fig:[^}]*\}\}")
_HEADING_RE = re.compile(r"(?m)^\s*#+\s*")
_BLOCKQUOTE_RE = re.compile(r"(?m)^\s*>\s*")
_BOLD_RE = re.compile(r"\*\*(.+?)\*\*")
_ITALIC_RE = re.compile(r"\*(.+?)\*")
_WHITESPACE_RE = re.compile(r"\s+")


def strip_markup(s: str) -> str:
    """Strip figure refs, heading/blockquote markers, and emphasis markup."""
    s = _FIG_REF_RE.sub("", s)
    s = _HEADING_RE.sub("", s)
    s = _BLOCKQUOTE_RE.sub("", s)
    s = _BOLD_RE.sub(r"\1", s)
    s = _ITALIC_RE.sub(r"\1", s)
    s = _WHITESPACE_RE.sub(" ", s).strip()
    return s


_MATH_SPAN_RE = re.compile(r"\$(.+?)\$")

# Tokens are matched in priority order: multi-character LaTeX commands and
# unicode symbols first, then structural tokens, then single letters (so
# that runs of variable letters like "IR" are spoken as separate letters),
# then numbers, then whitespace, then anything else falls through as a
# literal token.
_MATH_TOKEN_RE = re.compile(
    r"\\Delta|\\lambda|\\times|\\approx"
    r"|Δ|λ|×|≈"
    r"|\|[^|]*\|"
    r"|_\{[^}]*\}|_\w"
    r"|=|/"
    r"|[A-Za-z]"
    r"|\d+(?:\.\d+)?"
    r"|\s+"
    r"|."
)

_MATH_WORDS = {
    "\\Delta": "delta",
    "Δ": "delta",
    "\\lambda": "lambda",
    "λ": "lambda",
    "\\times": "times",
    "×": "times",
    "\\approx": "approximately",
    "≈": "approximately",
    "=": "equals",
    "/": "over",
}


def _speak_math_span(expr: str) -> str:
    words = []
    for m in _MATH_TOKEN_RE.finditer(expr):
        tok = m.group(0)
        if tok in _MATH_WORDS:
            words.append(_MATH_WORDS[tok])
        elif tok.startswith("|") and tok.endswith("|") and len(tok) >= 2:
            words.append("the magnitude of " + tok[1:-1])
        elif tok.startswith("_{"):
            words.append("sub " + tok[2:-1])
        elif tok.startswith("_"):
            words.append("sub " + tok[1:])
        elif tok.isspace():
            continue
        else:
            words.append(tok)
    return " ".join(words)


def speak_math(s: str) -> str:
    """Replace each ``$...$`` math span with spoken English."""

    def repl(m: "re.Match[str]") -> str:
        return _speak_math_span(m.group(1))

    out = _MATH_SPAN_RE.sub(repl, s)
    out = _WHITESPACE_RE.sub(" ", out).strip()
    return out


_FIG_CAPTURE_RE = re.compile(r"\{\{fig:([^}]*)\}\}")


def speak_figures(s: str, descriptions: "dict[str, tuple[str, str]]") -> str:
    """Replace ``{{fig:ID}}`` refs with a spoken figure description."""

    def repl(m: "re.Match[str]") -> str:
        fig_id = m.group(1)
        if fig_id not in descriptions:
            return ""
        num, desc = descriptions[fig_id]
        return f"(Figure {num}. {desc}.)"

    return _FIG_CAPTURE_RE.sub(repl, s)
