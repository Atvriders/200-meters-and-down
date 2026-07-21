"""Generate figures/classc.svg: Class-C amplifier operation -- a sinusoidal
grid-drive waveform on top, and the resulting plate-current pulses (short,
conduction angle < 180 degrees, occurring only at the drive peaks) below.
Rendered in a single black color on a transparent background; post-processed
afterward to theme with currentColor.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

deg = np.linspace(-90, 810, 3000)
drive = np.cos(np.radians(deg))

# classic class-C pulse model: i_p(theta) = Imax*(cos(theta) - cos(theta_c))
# for |theta| < theta_c (theta measured from the nearest drive peak), else 0.
# theta_c = 60 deg -> full conduction angle = 120 deg < 180 deg.
theta_c = 60.0
cos_c = np.cos(np.radians(theta_c))
peaks = [0, 360, 720]

plate = np.zeros_like(deg)
for p in peaks:
    theta = deg - p
    raw = np.cos(np.radians(theta)) - cos_c
    pulse = np.clip(raw, 0, None)
    plate = np.maximum(plate, pulse)
plate = plate / plate.max()

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 5.2), sharex=True)

# top: sinusoidal grid drive, with the cutoff/conduction threshold marked
ax1.plot(deg, drive, color="black", linewidth=2)
ax1.axhline(cos_c, color="black", linewidth=1, linestyle="--", alpha=0.6)
ax1.text(760, cos_c + 0.05, "cutoff", color="black", fontsize=9, alpha=0.8)
ax1.set_ylabel("grid drive\n(volts, relative)", color="black", fontsize=10)
ax1.set_ylim(-1.3, 1.3)
ax1.tick_params(colors="black", labelsize=9)
for spine in ax1.spines.values():
    spine.set_color("black")
ax1.axhline(0, color="black", linewidth=0.6, alpha=0.3)
ax1.set_title("Class-C Amplifier: Grid Drive vs. Plate-Current Pulses", color="black", fontsize=12)

# bottom: plate current, narrow conduction pulses at each drive peak
ax2.plot(deg, plate, color="black", linewidth=2)
ax2.fill_between(deg, plate, color="black", alpha=0.15)
ax2.set_ylabel("plate current\n(relative)", color="black", fontsize=10)
ax2.set_xlabel("phase (degrees)", color="black", fontsize=10)
ax2.set_ylim(-0.05, 1.15)
ax2.tick_params(colors="black", labelsize=9)
for spine in ax2.spines.values():
    spine.set_color("black")

# annotate the conduction angle on the middle pulse (clear of the y-axis labels)
y_ann = 0.5
p_ann = 360
ax2.annotate(
    "", xy=(p_ann + theta_c, y_ann), xytext=(p_ann - theta_c, y_ann),
    arrowprops=dict(arrowstyle="<->", color="black", alpha=0.8, linewidth=1.2),
)
ax2.text(p_ann, y_ann + 0.06, "conduction angle < 180°", color="black",
          fontsize=9, ha="center", alpha=0.85)

ax2.set_xticks([-90, 0, 90, 180, 270, 360, 450, 540, 630, 720, 810])
ax2.set_xlim(-90, 810)

fig.tight_layout()
fig.savefig(
    "/home/kasm-user/200-meters-and-down/figures/classc.svg",
    transparent=True,
    bbox_inches="tight",
)
print("wrote classc.svg")
