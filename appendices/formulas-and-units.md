# Appendix — Formulas and Units

Every formula used in *200 Meters and Down*, in the canonical notation fixed by the Accuracy Canon (`accuracy-canon.md`, "Notation & Units"). Each entry gives the formula, its one-line meaning, and its variables. Frequencies are in hertz (kHz/MHz as convenient), wavelength in metres; Ohm's law is written **E = IR**. This appendix is derivative of the canon — if the two ever disagree, the canon governs.

## Symbols and units (quick reference)

| Symbol | Quantity | Unit |
|---|---|---|
| f | Frequency | Hz (kHz, MHz) |
| T | Period | s |
| λ | Wavelength | m |
| c | Speed of light | m/s (≈ 3×10⁸; exact 299,792,458) |
| E | Voltage / EMF | V |
| I | Current | A |
| R | Resistance | Ω |
| P | Power | W |
| L | Inductance | H |
| C | Capacitance | F |
| Q | Quality factor | dimensionless |
| Δf | Frequency change / FM deviation / Doppler shift | Hz |
| f_m | Highest modulating (audio) frequency | Hz |
| β | FM modulation index | dimensionless |
| m | AM modulation index | dimensionless |
| v | Relative (range-rate) velocity | m/s |
| N | PLL divider ratio | integer |

## Wave propagation

**c = f · λ** — the wave-speed relation; frequency and wavelength are reciprocal through the constant speed of light.
- c = speed of light (≈ 3×10⁸ m/s; exact 299,792,458 m/s); f = frequency (Hz); λ = wavelength (m).

**λ(m) = 300 / f(MHz)** — the working quick-conversion form used throughout the book.
- λ = wavelength (m); f = frequency (MHz). Anchor values: 200 m ⇔ 1.5 MHz; 110 m ⇔ ~2.73 MHz; 80 m ⇔ 3.75 MHz; 40 m ⇔ 7.5 MHz; 20 m ⇔ 15 MHz; 10 m ⇔ 30 MHz; 5 m ⇔ 60 MHz; 2½ m ⇔ 120 MHz.

**T = 1 / f** — period is the reciprocal of frequency.
- T = period (s); f = frequency (Hz).

## Circuit fundamentals

**E = IR** (Ohm's law) — voltage across a resistance equals current times resistance.
- E = voltage/EMF (V); I = current (A); R = resistance (Ω). Rearranged: I = E/R, R = E/I.

**P = E · I = I²·R = E²/R** — electrical power dissipated or delivered.
- P = power (W); E = voltage (V); I = current (A); R = resistance (Ω).

**f₀ = 1 / (2π · √(L·C))** — the resonant frequency of an LC tank, the natural frequency at which coil and capacitor exchange energy.
- f₀ = resonant frequency (Hz); L = inductance (H); C = capacitance (F).

**Q = f₀ / BW_3dB** — quality factor: the sharpness (selectivity) of a resonant circuit.
- Q = quality factor (dimensionless); f₀ = resonant/centre frequency (Hz); BW_3dB = −3 dB bandwidth (Hz). Higher Q = narrower, more selective response.

## Superheterodyne receiver

**f_IF = |f_RF − f_LO|** — the fixed intermediate frequency produced by mixing signal and local oscillator.
- f_IF = intermediate frequency (Hz); f_RF = received signal frequency (Hz); f_LO = local-oscillator frequency (Hz).

**f_image = f_LO ± f_IF = f_RF ± 2·f_IF** — the spurious image response on the far side of the LO from the wanted signal.
- f_image = image frequency (Hz); other terms as above. Front-end selectivity and IF choice set image rejection.

## Amplitude modulation (AM)

**BW_AM ≈ 2 · f_m** — the occupied bandwidth of a double-sideband AM signal is twice the highest audio frequency.
- BW_AM = occupied bandwidth (Hz); f_m = highest modulating audio frequency (Hz). Example: 3 kHz audio → ~6 kHz occupied.

**m = A_m / A_c** — AM modulation index (depth), the ratio of modulating amplitude to carrier amplitude.
- m = modulation index (0–1 for no overmodulation); A_m = peak modulating amplitude; A_c = carrier amplitude.

## Frequency modulation (FM)

**β = Δf / f_m** — FM modulation index: peak deviation divided by highest modulating frequency.
- β = modulation index (dimensionless); Δf = peak deviation (Hz); f_m = highest modulating frequency (Hz).

**BW = 2 · (Δf + f_m)** — Carson's rule: the bandwidth containing ~98% of an FM signal's power.
- BW = occupied bandwidth (Hz); Δf = peak deviation (Hz); f_m = highest modulating frequency (Hz). Standard ham wideband example: Δf = 5 kHz, f_m = 3 kHz → BW ≈ 16 kHz. Narrowband: Δf = 2.5 kHz.

## Satellite operation

**Δf = f · v / c** — Doppler shift of a received frequency due to relative line-of-sight motion.
- Δf = Doppler shift (Hz); f = nominal frequency (Hz); v = line-of-sight (range-rate) velocity (m/s, positive closing); c = speed of light (m/s). LEO along-track speed ~7.5 km/s gives several kHz on a 2 m uplink, proportionally more at 70 cm.

## Frequency synthesis

**f_VCO = N · f_ref** — a PLL synthesizer's output equals the reference times the divider ratio.
- f_VCO = synthesized VCO/output frequency (Hz); N = programmable divider ratio (integer); f_ref = reference (crystal) frequency (Hz). Changing N under microprocessor control selects any of thousands of channels from one crystal.

## Digital modes (reference values)

**PSK31: 31.25 baud, BPSK, ~31 Hz bandwidth** — narrow keyboard-to-keyboard mode using Varicode.
- baud = symbols/second; bandwidth ≈ the symbol rate for BPSK.

**FT8: 8-FSK, 79 symbols × 3 bits, BW ≈ 8 × 6.25 Hz ≈ 50 Hz; (174,91) LDPC; 15 s cycles.**
- 8 tones carry 3 bits/symbol; 77 info + 14 CRC = 91 payload bits → 174-bit LDPC codeword; decodes at roughly −20 to −24 dB SNR in a 2500 Hz reference bandwidth (a range, not a single figure).

## Decibels

**dB = 10 · log₁₀(P₂ / P₁)** — a power ratio expressed logarithmically; **dBm** references P₁ = 1 mW.
- dB = ratio (dimensionless log unit); P₁, P₂ = powers (W). Voltage ratios use 20·log₁₀(V₂/V₁) at equal impedance.
