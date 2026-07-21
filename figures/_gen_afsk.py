"""Generate figures/afsk.svg — Bell 202 1200-baud AFSK waveform.

Time-domain plot of an AFSK waveform switching continuously between the
mark tone (1200 Hz) and the space tone (2200 Hz) as an 8-bit stream is
sent at 1200 baud. Single-color (black) on transparent background; the
build post-processes the saved SVG to currentColor so it themes with the
page.
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ---- AFSK parameters (Bell 202, per accuracy-canon.md) ----
BAUD = 1200
F_MARK = 1200.0   # Hz, binary 1
F_SPACE = 2200.0  # Hz, binary 0
T_BIT = 1.0 / BAUD

bits = [1, 1, 0, 1, 0, 0, 1, 1]
n_bits = len(bits)

fs = 200_000.0  # sample rate for a smooth continuous-phase waveform
dt = 1.0 / fs
samples_per_bit = int(round(T_BIT * fs))

# Build instantaneous-frequency array, then integrate phase so tone
# transitions are continuous-phase (as real Bell 202 modems produce).
freq = np.empty(samples_per_bit * n_bits)
for i, b in enumerate(bits):
    freq[i * samples_per_bit:(i + 1) * samples_per_bit] = F_MARK if b else F_SPACE

phase = 2 * np.pi * np.cumsum(freq) * dt
wave = np.sin(phase)
t = np.arange(len(wave)) * dt * 1000.0  # ms

fig, ax = plt.subplots(figsize=(8.2, 3.1))

ax.plot(t, wave, color="black", linewidth=1.1)

# Bit-boundary guides + bit-value labels along the top.
t_bit_ms = T_BIT * 1000.0
for i in range(n_bits + 1):
    ax.axvline(i * t_bit_ms, color="black", linewidth=0.5, linestyle=(0, (1, 2)), alpha=0.6)
for i, b in enumerate(bits):
    xc = (i + 0.5) * t_bit_ms
    ax.text(xc, 1.32, str(b), ha="center", va="bottom", fontsize=10, color="black")

# mark/space callouts on the first '1' segment and first '0' segment.
first_mark_i = bits.index(1)
first_space_i = bits.index(0)
xc_mark = (first_mark_i + 0.5) * t_bit_ms
xc_space = (first_space_i + 0.5) * t_bit_ms
ax.annotate("mark\n1200 Hz", xy=(xc_mark, -1.05), xytext=(xc_mark, -1.85),
            ha="center", va="top", fontsize=9, color="black",
            arrowprops=dict(arrowstyle="-", color="black", linewidth=0.7))
ax.annotate("space\n2200 Hz", xy=(xc_space, -1.05), xytext=(xc_space, -1.85),
            ha="center", va="top", fontsize=9, color="black",
            arrowprops=dict(arrowstyle="-", color="black", linewidth=0.7))

# 1200-baud bit-period annotation (double-headed arrow over one bit cell).
bp_i = 4
x0, x1 = bp_i * t_bit_ms, (bp_i + 1) * t_bit_ms
ax.annotate("", xy=(x1, 1.62), xytext=(x0, 1.62),
            arrowprops=dict(arrowstyle="<->", color="black", linewidth=0.8))
ax.text((x0 + x1) / 2, 1.72, "1/1200 s  (1200 baud)", ha="center", va="bottom",
        fontsize=9, color="black")

ax.text(0.5 * n_bits * t_bit_ms, 2.35, "bit value", ha="center", va="bottom",
        fontsize=9, color="black")

ax.set_xlim(0, n_bits * t_bit_ms)
ax.set_ylim(-2.3, 2.6)
ax.set_xlabel("time (ms)", fontsize=9, color="black")
ax.set_xticks([i * t_bit_ms for i in range(n_bits + 1)])
ax.set_xticklabels([f"{i * t_bit_ms:.2f}" for i in range(n_bits + 1)], fontsize=7)
ax.set_yticks([])
for spine in ("top", "right", "left"):
    ax.spines[spine].set_visible(False)
ax.spines["bottom"].set_color("black")
ax.tick_params(axis="x", colors="black", length=3)
ax.set_title("Bell 202 AFSK — 1200-baud mark/space tone shift", fontsize=10, color="black")

fig.tight_layout()
fig.savefig("/home/kasm-user/200-meters-and-down/figures/afsk.svg",
            transparent=True, bbox_inches="tight")
print("wrote afsk.svg")
