"""
Generates figures/ssb-vs-am.svg — occupied-spectrum comparison, AM vs SSB.

Uses the canon's worked example: 3 kHz audio -> AM occupies ~6 kHz
(carrier +/- 3 kHz), SSB occupies ~3 kHz (one sideband, no carrier).
Single-color (black) on transparent background; post-processed to
currentColor so it themes with the page.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

OUT = "/home/kasm-user/200-meters-and-down/figures/ssb-vs-am.svg"

fm = 3.0  # audio bandwidth, kHz (canon worked example)
XLIM = (-4.6, 4.6)
YLIM = (0, 1.55)

fig, (axL, axR) = plt.subplots(1, 2, figsize=(9.2, 4.2), sharey=True)

for ax in (axL, axR):
    ax.set_xlim(*XLIM)
    ax.set_ylim(*YLIM)
    ax.axhline(0, color="black", linewidth=1.2)
    ax.set_yticks([])
    for spine in ("top", "right", "left"):
        ax.spines[spine].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.set_xlabel("frequency relative to carrier  $f_c$  (kHz)", fontsize=9)

# ---------------- Left: AM ----------------
axL.set_title("AM — carrier + two sidebands", fontsize=11)

# lower and upper sideband, shown as occupied bands
axL.fill_between([-fm, 0], 0, 0.55, color="black", alpha=0.35, linewidth=0)
axL.fill_between([0, fm], 0, 0.55, color="black", alpha=0.35, linewidth=0)
axL.plot([-fm, -fm, 0, 0], [0, 0.55, 0.55, 0], color="black", linewidth=1.3)
axL.plot([0, 0, fm, fm], [0, 0.55, 0.55, 0], color="black", linewidth=1.3)

# carrier: tall spike at f_c
axL.plot([0, 0], [0, 1.3], color="black", linewidth=2.4)
axL.text(0, 1.38, "carrier", ha="center", va="bottom", fontsize=9)

axL.text(-fm / 2, 0.62, "LSB", ha="center", va="bottom", fontsize=9)
axL.text(fm / 2, 0.62, "USB", ha="center", va="bottom", fontsize=9)

axL.set_xticks([-fm, 0, fm])
axL.set_xticklabels([f"$f_c-f_m$\n(-{fm:g})", "$f_c$\n(0)", f"$f_c+f_m$\n(+{fm:g})"], fontsize=8)

# occupied-bandwidth bracket
yb = -0.30
axL.annotate("", xy=(fm, yb), xytext=(-fm, yb),
             arrowprops=dict(arrowstyle="<->", color="black", linewidth=1.1))
axL.text(0, yb - 0.10, f"occupied ≈ 2×$f_m$  (≈ {2*fm:g} kHz)",
          ha="center", va="top", fontsize=9)

# ---------------- Right: SSB ----------------
axR.set_title("SSB — one sideband, no carrier", fontsize=11)

axR.fill_between([0, fm], 0, 0.55, color="black", alpha=0.35, linewidth=0)
axR.plot([0, 0, fm, fm], [0, 0.55, 0.55, 0], color="black", linewidth=1.3)
axR.text(fm / 2, 0.62, "USB", ha="center", va="bottom", fontsize=9)

# carrier suppressed: dashed ghost spike, low alpha
axR.plot([0, 0], [0, 1.3], color="black", linewidth=2.0, linestyle=(0, (2, 2)), alpha=0.4)
axR.text(0, 1.38, "carrier\nsuppressed", ha="center", va="bottom", fontsize=8, alpha=0.7)

axR.set_xticks([0, fm])
axR.set_xticklabels(["$f_c$\n(0)", f"$f_c+f_m$\n(+{fm:g})"], fontsize=8)

axR.annotate("", xy=(fm, yb), xytext=(0, yb),
             arrowprops=dict(arrowstyle="<->", color="black", linewidth=1.1))
axR.text(fm / 2, yb - 0.10, f"occupied ≈ $f_m$  (≈ {fm:g} kHz)",
          ha="center", va="top", fontsize=9)

fig.suptitle("Occupied Spectrum: AM vs. SSB", fontsize=13, y=1.03)
fig.tight_layout()

fig.savefig(OUT, format="svg", transparent=True, bbox_inches="tight")
plt.close(fig)

# ---- post-process: strip xml/doctype prolog, force theme-able color ----
with open(OUT, "r", encoding="utf-8") as f:
    svg = f.read()

# drop leading <?xml ...?> and (possibly multi-line) <!DOCTYPE ...> by
# slicing from the first real '<svg' tag onward.
idx = svg.find("<svg")
assert idx != -1, "no <svg tag found in matplotlib output"
svg = svg[idx:]

for old in ("#000000", "#000", "stroke:#000000", "fill:#000000", "black"):
    svg = svg.replace(old, "currentColor")

# matplotlib omits an explicit fill on many elements (glyph paths, the
# fill_between bands) and relies on the SVG spec's default fill (black),
# which would NOT re-theme in dark mode. Force a default via the
# existing stylesheet rule so untouched elements inherit currentColor too.
svg = svg.replace(
    "*{stroke-linejoin: round; stroke-linecap: butt}",
    "*{stroke-linejoin: round; stroke-linecap: butt; fill: currentColor}",
)

with open(OUT, "w", encoding="utf-8") as f:
    f.write(svg)

assert svg.lstrip().startswith("<svg"), "SVG does not start with <svg after prolog strip"
assert "currentColor" in svg, "no currentColor found after color substitution"
print("wrote", OUT)
