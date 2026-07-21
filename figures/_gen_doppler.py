"""Generate figures/doppler.svg: received-frequency Doppler shift over the
course of a LEO satellite pass. Physically: line-of-sight range-rate (and
hence Delta f = f*v/c) is near its maximum magnitude at AOS/LOS (low
elevation, mostly along-track motion) and passes through zero at TCA
(closest approach, motion perpendicular to the line of sight) -- the classic
S-shaped Doppler curve, steepest right at TCA. Rendered in a single black
color on a transparent background; post-processed afterward to theme with
currentColor.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# time axis: seconds from closest approach (TCA), a ~15-minute pass
t = np.linspace(-450, 450, 2000)

df_max = 3.0      # kHz, asymptotic peak shift near AOS/LOS (2 m uplink, ~7.5 km/s LEO)
tau = 90.0         # s, characteristic width of the steep zero-crossing region

df = -df_max * t / np.sqrt(t**2 + tau**2)

fig, ax = plt.subplots(figsize=(7.2, 4.6))

ax.plot(t / 60.0, df, color="black", linewidth=2.4)
ax.axhline(0, color="black", linewidth=1, alpha=0.4)
ax.axvline(0, color="black", linewidth=1, linestyle="--", alpha=0.5)

ax.set_xlim(-7.5, 7.5)
ax.set_ylim(-3.5, 3.5)
ax.set_xlabel("time from closest approach, TCA (minutes)", color="black", fontsize=11)
ax.set_ylabel(r"received frequency offset  $\Delta f = f \cdot v/c$  (kHz)", color="black", fontsize=11)
ax.set_title("Doppler Shift Across a Satellite Pass (2 m uplink)", color="black", fontsize=13)

ax.tick_params(colors="black", labelsize=9.5)
for spine in ax.spines.values():
    spine.set_color("black")

# annotate AOS / TCA / LOS, offset clear of the curve and the TCA dashed line
ax.annotate("AOS\n(rising, approaching\n→ shift high)", xy=(-6.6, df_max * 0.45),
            color="black", fontsize=9, ha="center", va="center")
ax.annotate("TCA, Δf = 0", xy=(1.0, 1.0), color="black", fontsize=9.5,
            ha="left", va="center")
ax.annotate("LOS\n(setting, receding\n→ shift low)", xy=(6.6, -df_max * 0.45),
            color="black", fontsize=9, ha="center", va="center")

ax.plot([0], [0], marker="o", color="black", markersize=4)

fig.tight_layout()
fig.savefig(
    "/home/kasm-user/200-meters-and-down/figures/doppler.svg",
    transparent=True,
    bbox_inches="tight",
)
print("wrote doppler.svg")
