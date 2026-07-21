"""Generate figures/yagi-pattern.svg: a polar azimuth radiation pattern
for a directional (Yagi-type) beam antenna, in a single black color on a
transparent background. Post-processed afterward to theme with currentColor.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# angle axis in degrees, 0 = forward (boresight)
deg = np.linspace(0, 360, 2000)
rad = np.radians(deg)


def lobe(center_deg, width_deg, amplitude):
    """A smooth angular lobe (wrapped) centered at center_deg."""
    d = (deg - center_deg + 180) % 360 - 180  # signed angular distance, wrapped
    sigma = width_deg / 2.3548  # convert desired FWHM-ish width to a gaussian sigma
    return amplitude * np.exp(-(d ** 2) / (2 * sigma ** 2))


# main forward lobe (boresight), two small sidelobes, and a much smaller back lobe
pattern = (
    lobe(0, 50, 1.00)
    + lobe(100, 32, 0.24)
    + lobe(260, 32, 0.24)
    + lobe(180, 42, 0.14)
)
pattern = np.clip(pattern, 1e-3, None)

fig = plt.figure(figsize=(6, 6))
ax = fig.add_subplot(111, projection="polar")
ax.set_theta_zero_location("N")
ax.set_theta_direction(1)

ax.plot(rad, pattern, color="black", linewidth=2.2)
ax.fill(rad, pattern, color="black", alpha=0.08)

ax.set_rlabel_position(135)
ax.set_rticks([0.25, 0.5, 0.75, 1.0])
ax.set_yticklabels(["-12 dB", "-6 dB", "-3 dB", "0 dB"], color="black", fontsize=9)
ax.set_xticks(np.radians([0, 45, 90, 135, 180, 225, 270, 315]))
ax.set_xticklabels(
    ["0°\n(forward)", "45°", "90°", "135°", "180°\n(back)", "225°", "270°", "315°"],
    color="black",
    fontsize=9,
)
ax.tick_params(colors="black")
ax.grid(color="black", alpha=0.25, linewidth=0.8)
ax.spines["polar"].set_color("black")
ax.set_title("Yagi Beam Azimuth Pattern (relative gain)", color="black", fontsize=12, pad=18)

fig.savefig(
    "/home/kasm-user/200-meters-and-down/figures/yagi-pattern.svg",
    transparent=True,
    bbox_inches="tight",
)
print("wrote yagi-pattern.svg")
