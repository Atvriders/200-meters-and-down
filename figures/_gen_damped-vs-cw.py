"""Generate figures/damped-vs-cw.svg (Figure 1.2).

Two stacked time-domain plots, single black line on transparent background:
  top    - a spark transmitter's damped wave-train: repeated bursts, each an
           exponentially-decaying ringing oscillation, with silent gaps
           between bursts (the spark gap fires, rings down, and waits).
  bottom - a pure continuous wave (CW): constant-amplitude sinusoid, same
           time axis, for direct visual contrast.

Post-processed after saving so the SVG themes via `currentColor` (see the
shell step that follows this script).
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------
# Damped wave-train (top): several bursts of a decaying RF oscillation.
# Each burst starts when the spark gap fires and rings down before the
# next firing. Carrier frequency is chosen only for a legible number of
# visible cycles per burst -- not to scale with any real spark frequency.
# ---------------------------------------------------------------------
fs = 4000.0          # samples per second (time unit is arbitrary "ms")
t_total = 10.0        # ms
t = np.linspace(0, t_total, int(fs * t_total))

burst_period = 2.5    # ms between spark-gap firings
burst_carrier = 6.0   # cycles per ms within a burst (arbitrary display units)
decay_rate = 3.0      # decay constant per ms (sets the ringdown length)

damped = np.zeros_like(t)
n_bursts = int(t_total / burst_period) + 1
for k in range(n_bursts):
    t0 = k * burst_period
    local = t - t0
    mask = local >= 0
    envelope = np.exp(-decay_rate * local)
    # burst effectively ends well before the next one fires
    envelope = np.where(local < burst_period, envelope, 0.0)
    damped += np.where(mask, envelope * np.sin(2 * np.pi * burst_carrier * local), 0.0)

# ---------------------------------------------------------------------
# Continuous wave (bottom): constant-amplitude sinusoid, same time axis.
# ---------------------------------------------------------------------
cw_freq = 6.0  # match the damped burst's carrier for a fair visual comparison
cw = np.sin(2 * np.pi * cw_freq * t)

# ---------------------------------------------------------------------
# Plot: two stacked panels, shared time axis, single black line, no fill.
# ---------------------------------------------------------------------
fig, axes = plt.subplots(2, 1, figsize=(7.5, 4.6), sharex=True)

ax_top, ax_bot = axes

ax_top.plot(t, damped, color="#000000", linewidth=1.3)
ax_top.axhline(0, color="#000000", linewidth=0.6, alpha=0.4)
ax_top.set_ylim(-1.15, 1.15)
ax_top.set_title("Damped wave (spark)", fontsize=11, color="#000000", loc="left")
ax_top.set_ylabel("amplitude", fontsize=9, color="#000000")
for spine in ("top", "right"):
    ax_top.spines[spine].set_visible(False)
ax_top.spines["left"].set_color("#000000")
ax_top.spines["bottom"].set_color("#000000")
ax_top.tick_params(colors="#000000", labelsize=8)
ax_top.set_yticks([])

ax_bot.plot(t, cw, color="#000000", linewidth=1.3)
ax_bot.axhline(0, color="#000000", linewidth=0.6, alpha=0.4)
ax_bot.set_ylim(-1.15, 1.15)
ax_bot.set_title("Continuous wave (CW)", fontsize=11, color="#000000", loc="left")
ax_bot.set_xlabel("time", fontsize=9, color="#000000")
ax_bot.set_ylabel("amplitude", fontsize=9, color="#000000")
for spine in ("top", "right"):
    ax_bot.spines[spine].set_visible(False)
ax_bot.spines["left"].set_color("#000000")
ax_bot.spines["bottom"].set_color("#000000")
ax_bot.tick_params(colors="#000000", labelsize=8)
ax_bot.set_yticks([])
ax_bot.set_xticks([])

fig.tight_layout()

out_path = "/home/kasm-user/200-meters-and-down/figures/damped-vs-cw.svg"
fig.savefig(out_path, format="svg", transparent=True, bbox_inches="tight")
print("wrote", out_path)
