"""Render inline math expressions to self-contained inline SVG strings.

Uses matplotlib's mathtext (no LaTeX installation required) to rasterize a
math expression as vector glyph paths, tightly cropped, and returns just the
``<svg>...</svg>`` fragment so it can be spliced directly inline into a
single-file HTML book. The output has no external resource references (no
``<image>``, no network ``xlink:href``/``href``, no ``@import``), so it works
offline. Glyph fills are rewritten to ``currentColor`` (or a caller-supplied
color) so the expression inherits the surrounding page's text color and
renders correctly in both light and dark themes.
"""

import io
import re

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402

# matplotlib's mathtext SVG backend may emit glyph fills as explicit black,
# in either the "fill:#000000" (style attribute) or fill="#000000"
# (attribute) form, depending on version. Replace both so the resulting
# glyphs inherit color.
_BLACK_FILL_STYLE_RE = re.compile(r"fill:#000000")
_BLACK_FILL_ATTR_RE = re.compile(r'fill="#000000"')
# Newer matplotlib versions omit any fill on glyph <use>/<path> elements and
# rely on the SVG default fill of black, so the substitutions above never
# match. Set fill explicitly on the <svg> root instead: it's the initial
# value for the inherited `fill` property, so every descendant that doesn't
# set its own fill (i.e. every glyph) picks it up via normal CSS cascade.
_SVG_OPEN_TAG_RE = re.compile(r"<svg(?=[\s>])")


def render(expr: str, color: str = "currentColor") -> str:
    """Render a math expression to a self-contained inline SVG string.

    ``expr`` is mathtext syntax (matplotlib's LaTeX-like subset), e.g.
    ``"E = IR"`` or ``"f_{IF} = |f_{RF} - f_{LO}|"``. It is wrapped in
    ``$...$`` and drawn with matplotlib, saved to SVG in-memory, tightly
    cropped to the expression, and returned as just the ``<svg>...</svg>``
    markup (no XML prolog or DOCTYPE), with glyph fills set to ``color``
    so the result is themeable inline.
    """
    fig = plt.figure()
    try:
        fig.text(0, 0, f"${expr}$", color="black")
        buf = io.BytesIO()
        fig.savefig(buf, format="svg", bbox_inches="tight", transparent=True)
    finally:
        plt.close(fig)

    svg = buf.getvalue().decode("utf-8")

    # Strip the XML prolog and DOCTYPE so the fragment splices cleanly inline.
    svg = re.sub(r"<\?xml[^>]*\?>\s*", "", svg)
    svg = re.sub(r"<!DOCTYPE[^>]*>\s*", "", svg, flags=re.DOTALL)

    # Make glyphs themeable: rewrite any rendered black fill to `color`...
    svg = _BLACK_FILL_STYLE_RE.sub(f"fill:{color}", svg)
    svg = _BLACK_FILL_ATTR_RE.sub(f'fill="{color}"', svg)
    # ...and set it as the inherited default on the root, for versions of
    # matplotlib that omit an explicit fill on glyph elements entirely.
    svg = _SVG_OPEN_TAG_RE.sub(f'<svg fill="{color}"', svg, count=1)

    return svg.strip()
