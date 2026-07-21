"""Generate figures/am-spectrum.svg — Figure 3.3, the spectrum of a
plate-modulated AM signal: a tall carrier at f_c flanked by symmetric
lower and upper sidebands at f_c - f_m and f_c + f_m, with the occupied
bandwidth 2*f_m annotated.

Rendered in pure black on a transparent background, then post-processed
so the black recolors to `currentColor` and the file splices inline as
a themeable SVG fragment.
"""
import re
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = "/home/kasm-user/200-meters-and-down/figures/am-spectrum.svg"

fm = 1.0   # one normalized "modulating-frequency" unit
fc = 0.0   # carrier reference position

x = [fc - fm, fc, fc + fm]
y = [0.32, 1.0, 0.32]

fig, ax = plt.subplots(figsize=(6, 4))

markerline, stemlines, baseline = ax.stem(x, y, basefmt=" ")
plt.setp(markerline, color="black", markersize=8, zorder=3)
plt.setp(stemlines, color="black", linewidth=2.4)

# carrier / sideband labels
ax.text(fc, 1.06, "Carrier", ha="center", va="bottom", fontsize=11)
ax.text(fc, 1.20, r"$f_c$", ha="center", va="bottom", fontsize=11)

ax.text(fc - fm, 0.40, "Lower\nsideband", ha="center", va="bottom", fontsize=9.5)
ax.text(fc + fm, 0.40, "Upper\nsideband", ha="center", va="bottom", fontsize=9.5)

# occupied-bandwidth annotation
y_bw = -0.26
ax.annotate(
    "", xy=(fc + fm, y_bw), xytext=(fc - fm, y_bw),
    arrowprops=dict(arrowstyle="<->", color="black", linewidth=1.4),
)
ax.text(fc, y_bw - 0.07, r"Occupied bandwidth $= 2f_m$",
         ha="center", va="top", fontsize=10)

ax.set_xlim(fc - fm * 1.9, fc + fm * 1.9)
ax.set_ylim(y_bw - 0.30, 1.42)

ax.set_xticks([fc - fm, fc, fc + fm])
ax.set_xticklabels([r"$f_c-f_m$", r"$f_c$", r"$f_c+f_m$"], fontsize=10.5)
ax.set_yticks([])

ax.set_xlabel("Frequency", fontsize=11)
ax.set_ylabel("Amplitude", fontsize=11)

for spine in ("top", "right", "left"):
    ax.spines[spine].set_visible(False)
ax.spines["bottom"].set_color("black")
ax.spines["bottom"].set_linewidth(1.2)

ax.tick_params(axis="x", colors="black", length=4)
ax.xaxis.label.set_color("black")
ax.yaxis.label.set_color("black")

fig.tight_layout()
fig.savefig(OUT, transparent=True, bbox_inches="tight")
plt.close(fig)

# ---- post-process: recolor black -> currentColor, strip xml prolog ----
svg = open(OUT, encoding="utf-8").read()

svg = re.sub(r"<\?xml[^>]*\?>\s*", "", svg)
svg = re.sub(r"<!DOCTYPE[^>]*>\s*", "", svg)

svg = re.sub(r"#000000", "currentColor", svg, flags=re.IGNORECASE)
svg = re.sub(r"#000\b", "currentColor", svg, flags=re.IGNORECASE)
svg = re.sub(r"\bblack\b", "currentColor", svg, flags=re.IGNORECASE)

svg = svg.strip() + "\n"
open(OUT, "w", encoding="utf-8").write(svg)

assert svg.startswith("<svg"), "output does not start with <svg"
assert "currentColor" in svg, "no currentColor found after recoloring"
print("wrote", OUT, len(svg), "bytes")
