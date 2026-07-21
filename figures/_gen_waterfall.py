"""Generate figures/waterfall.svg: an FFT waterfall (spectrogram) of a busy
band -- frequency across, time down, several vertical signal traces of
varying brightness against a noise floor.

Rendered as pure vector shapes (scatter stipple + line segments), all in a
single color (black) with varying opacity to encode "brightness," on a
transparent background. This keeps the figure a true vector SVG (no
embedded raster image) so post-processing can retheme it to currentColor
and it will still read correctly in both light and dark page themes.
"""

import re

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

rng = np.random.default_rng(20260721)

FREQ_MAX = 3000.0  # Hz, a typical SSB/digital-mode waterfall passband
TIME_MAX = 60.0  # s

fig, ax = plt.subplots(figsize=(7.0, 4.4))

# ---- Noise floor: an even stipple of low-alpha points -------------------
n_noise = 3500
nx = rng.uniform(0, FREQ_MAX, n_noise)
ny = rng.uniform(0, TIME_MAX, n_noise)
ax.scatter(nx, ny, s=2.2, marker="s", color="black", alpha=0.10, linewidths=0)

# ---- Signal traces: vertical bands built from segments of varying ------
# alpha (brightness) with a little frequency jitter (a real carrier
# wobbles slightly rather than sitting on one exact bin).
signal_freqs = [330, 690, 1180, 1550, 2080, 2460, 2760]
n_segments = 14
seg_len = TIME_MAX / n_segments

for fc in signal_freqs:
    # a couple of signals fade toward the noise floor for part of their
    # run, others stay strong throughout -- "varying brightness"
    fade_prob = rng.uniform(0.15, 0.55)
    for i in range(n_segments):
        y0 = i * seg_len
        y1 = y0 + seg_len * 1.05
        jitter = rng.normal(0, 4.0)
        alpha = rng.uniform(0.55, 0.98)
        if rng.uniform() < fade_prob:
            alpha = rng.uniform(0.08, 0.25)
        ax.plot(
            [fc + jitter, fc + jitter],
            [y0, y1],
            color="black",
            linewidth=6.5,
            solid_capstyle="butt",
            alpha=alpha,
        )

# ---- Callouts ------------------------------------------------------------
ax.annotate(
    "signal",
    xy=(signal_freqs[2], 46),
    xytext=(signal_freqs[2] + 260, 40),
    fontsize=9,
    color="black",
    arrowprops=dict(arrowstyle="->", color="black", linewidth=0.9),
)
ax.annotate(
    "noise floor",
    xy=(2250, 10),
    xytext=(2400, 4),
    fontsize=9,
    color="black",
    arrowprops=dict(arrowstyle="->", color="black", linewidth=0.9),
)

ax.set_xlim(0, FREQ_MAX)
ax.set_ylim(0, TIME_MAX)
ax.invert_yaxis()  # newest activity enters at the top, scrolls down
ax.set_xlabel("Frequency (Hz)", fontsize=10, color="black")
ax.set_ylabel("Time (s)  ↓  (older)", fontsize=10, color="black")
ax.set_xticks(np.arange(0, FREQ_MAX + 1, 500))
ax.set_yticks(np.arange(0, TIME_MAX + 1, 10))
ax.tick_params(axis="both", colors="black", labelsize=8)
for spine in ax.spines.values():
    spine.set_color("black")
    spine.set_linewidth(0.8)
ax.set_title(
    "FFT waterfall: frequency across, time down, signals as bright traces",
    fontsize=9.5,
    color="black",
)

fig.tight_layout()
OUT = "figures/waterfall.svg"
fig.savefig(OUT, format="svg", transparent=True, bbox_inches="tight")

# ---- Post-process: make the SVG theme-able -------------------------------
svg = open(OUT, encoding="utf-8").read()
svg = re.sub(r"<\?xml[^>]*\?>\s*", "", svg)
svg = re.sub(r"<!DOCTYPE[^>]*>\s*", "", svg, flags=re.DOTALL)
svg = svg.replace("#000000", "currentColor")
svg = re.sub(r"\bblack\b", "currentColor", svg)
svg = re.sub(r"(<svg\b)", r'\1 fill="currentColor"', svg, count=1)
svg = svg.strip() + "\n"

assert svg.startswith("<svg"), "post-processed SVG must start with <svg"
assert "currentColor" in svg, "post-processed SVG must reference currentColor"

with open(OUT, "w", encoding="utf-8") as f:
    f.write(svg)

print(f"wrote {OUT}")
