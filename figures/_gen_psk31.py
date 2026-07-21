"""Generate figures/psk31.svg: a BPSK time-domain plot showing PSK31
180-degree phase reversals at symbol boundaries, with idle vs. data-bit
annotation. Single-color (black) vector output, transparent background,
post-processed to theme via currentColor.
"""

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ---- PSK31 timing -----------------------------------------------------
BAUD = 31.25
T_SYM = 1.0 / BAUD  # 32 ms per symbol
# Illustrative carrier: exactly 2 cycles/symbol, so individual reversals
# stay visually distinguishable rather than blurring into a dense hash.
F_C = 2.0 / T_SYM  # = 62.5 Hz

# Bit sequence to render. PSK31 convention: bit 0 -> phase reversal at the
# symbol boundary, bit 1 -> no phase change. A run of 0-bits is the idle
# condition (continuous reversals); the marked run below stands in for one
# Varicode character's bit pattern between the self-synchronizing 00 gaps.
IDLE_BITS = [0, 0, 0]
DATA_BITS = [1, 0, 1, 0]
GAP_BITS = [0, 0]
TAIL_BITS = [0, 0]
BITS = IDLE_BITS + DATA_BITS + GAP_BITS + TAIL_BITS
N = len(BITS)

# ---- Build continuous phase-per-symbol array ---------------------------
phase = np.zeros(N)
state = 0.0
for i, b in enumerate(BITS):
    if b == 0:
        state += np.pi
    phase[i] = state

# ---- Sample the waveform -----------------------------------------------
FS = 20000.0  # Hz, sampling rate for a smooth plotted curve
t = np.arange(0, N * T_SYM, 1.0 / FS)
y = np.zeros_like(t)
for i in range(N):
    mask = (t >= i * T_SYM) & (t < (i + 1) * T_SYM)
    y[mask] = np.cos(2 * np.pi * F_C * t[mask] + phase[i])

t_ms = t * 1000.0
T_SYM_MS = T_SYM * 1000.0

fig, ax = plt.subplots(figsize=(7.2, 3.4))

ax.plot(t_ms, y, color="black", linewidth=1.3)

# Symbol-boundary guide lines + bit labels
for i in range(N + 1):
    ax.axvline(i * T_SYM_MS, color="black", linewidth=0.5, linestyle=":", alpha=0.55)
for i in range(N):
    cx = (i + 0.5) * T_SYM_MS
    ax.text(
        cx, -2.05, str(BITS[i]), ha="center", va="top", fontsize=8, color="black"
    )

# Mark a couple of representative reversal / no-reversal points, tucked
# just under the waveform so they don't collide with the symbol-period
# ruler at the top of the plot.
rev_x = 1 * T_SYM_MS  # idle boundary, bit 0 -> reversal
ax.annotate(
    "phase reversal (bit = 0)",
    xy=(rev_x, -0.95),
    xytext=(rev_x, -1.45),
    fontsize=7.6,
    ha="center",
    va="top",
    arrowprops=dict(arrowstyle="->", color="black", linewidth=0.8),
    color="black",
)

# first bit=1 boundary (start of DATA_BITS) for the "no reversal" callout
no_rev_i = len(IDLE_BITS)
no_rev_x = no_rev_i * T_SYM_MS
ax.annotate(
    "no reversal\n(bit = 1)",
    xy=(no_rev_x, 0.95),
    xytext=(no_rev_x + 46, 1.55),
    fontsize=7.6,
    ha="center",
    va="bottom",
    arrowprops=dict(arrowstyle="->", color="black", linewidth=0.8),
    color="black",
)

# Idle bracket
idle_end = len(IDLE_BITS) * T_SYM_MS
ax.annotate(
    "",
    xy=(0, -2.35),
    xytext=(idle_end, -2.35),
    arrowprops=dict(arrowstyle="-", color="black", linewidth=0.9),
)
ax.text(
    idle_end / 2,
    -2.52,
    "idle: continuous\nreversals",
    ha="center",
    va="top",
    fontsize=7.3,
    color="black",
)

# Data bracket
data_start = len(IDLE_BITS) * T_SYM_MS
data_end = (len(IDLE_BITS) + len(DATA_BITS)) * T_SYM_MS
ax.annotate(
    "",
    xy=(data_start, -2.35),
    xytext=(data_end, -2.35),
    arrowprops=dict(arrowstyle="-", color="black", linewidth=0.9),
)
ax.text(
    (data_start + data_end) / 2,
    -2.52,
    "one character\n(Varicode bit pattern)",
    ha="center",
    va="top",
    fontsize=7.3,
    color="black",
)

# Gap bracket
gap_start = data_end
gap_end = gap_start + len(GAP_BITS) * T_SYM_MS
ax.annotate(
    "",
    xy=(gap_start, -2.35),
    xytext=(gap_end, -2.35),
    arrowprops=dict(arrowstyle="-", color="black", linewidth=0.9),
)
ax.text(
    (gap_start + gap_end) / 2,
    -2.52,
    "00\ngap",
    ha="center",
    va="top",
    fontsize=7.3,
    color="black",
)

# Symbol-period callout, placed over the clear tail region at the top
ruler_i = N - 2  # one symbol width within the trailing idle run
ruler_x0 = ruler_i * T_SYM_MS
ruler_x1 = (ruler_i + 1) * T_SYM_MS
ax.annotate(
    "",
    xy=(ruler_x0, 1.7),
    xytext=(ruler_x1, 1.7),
    arrowprops=dict(arrowstyle="<->", color="black", linewidth=0.8),
)
ax.text(
    (ruler_x0 + ruler_x1) / 2,
    1.85,
    f"1 symbol =\n{T_SYM_MS:.0f} ms (31.25 baud)",
    ha="center",
    va="bottom",
    fontsize=7.6,
    color="black",
)

ax.set_xlim(0, N * T_SYM_MS)
ax.set_ylim(-3.05, 2.5)
ax.set_xlabel("Time (ms)", fontsize=9, color="black")
ax.set_yticks([])
for spine in ("top", "right", "left"):
    ax.spines[spine].set_visible(False)
ax.spines["bottom"].set_color("black")
ax.tick_params(axis="x", colors="black", labelsize=8)
ax.set_title(
    "BPSK carrier: phase reversals at symbol boundaries carry Varicode bits",
    fontsize=9.5,
    color="black",
)

fig.tight_layout()
OUT = "figures/psk31.svg"
fig.savefig(
    OUT,
    format="svg",
    transparent=True,
    bbox_inches="tight",
)

# ---- Post-process: make the SVG theme-able ------------------------------
# matplotlib emits explicit "#000000" for strokes, but text glyphs are
# drawn as <path>/<use> elements with NO fill attribute at all (relying on
# the SVG spec's default fill of black). Swapping the literal hex/word
# occurrences handles the strokes; adding fill="currentColor" on the root
# <svg> supplies a themed default that the unset-fill glyphs inherit.
import re

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
