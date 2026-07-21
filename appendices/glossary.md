# Appendix — Glossary

Standalone reference for the key technical terms of *200 Meters and Down*, ordered roughly by the era they first matter. Definitions are identical to and governed by the Accuracy Canon (`accuracy-canon.md`, "Glossary"); a chapter may expand a definition but must not contradict it. 60 terms.

| Term | Definition |
|---|---|
| Spark gap | An air gap across which a high-voltage discharge dumps stored capacitor energy into a tank circuit, exciting a burst of damped oscillations. |
| Damped wave | A carrier that rings down (decays exponentially) after each excitation rather than persisting, inherently occupying broad bandwidth. |
| Coherer | An early binary RF detector of loose metal filings that cohere (drop resistance) under a signal and must be tapped to reset. |
| Crystal detector | A passive point-contact semiconductor rectifier (e.g. galena and a "cat's-whisker" wire) that demodulates RF without gain. |
| Continuous wave (CW) | A pure, un-decaying sinusoidal carrier switched on and off for Morse keying, occupying far less bandwidth than spark. |
| Regeneration | Positive feedback of amplified output back to a tube's grid in phase, raising gain and selectivity and, taken further, causing oscillation. |
| Heterodyne | Mixing two frequencies to produce sum and difference outputs; the basis of both CW reception and the superheterodyne. |
| BFO (beat-frequency oscillator) | A local oscillator whose output beats against an incoming CW/SSB signal to produce an audible or intelligible tone. |
| Superheterodyne | A receiver that mixes the incoming signal with a local oscillator to a fixed intermediate frequency where most gain and selectivity live. |
| Intermediate frequency (IF) | The fixed frequency, after the mixer, at which a superheterodyne concentrates its amplification and filtering. |
| Image frequency | A spurious superhet response at the LO's opposite side (f_LO ± f_IF) that a poorly selective front end lets through. |
| MOPA | Master-Oscillator Power-Amplifier: a stable low-power oscillator buffered from the PA so antenna loading cannot pull its frequency. |
| Hartley oscillator | An LC feedback oscillator using a tapped inductor to set the feedback ratio. |
| Colpitts oscillator | An LC feedback oscillator using a tapped (divided) capacitor to set the feedback ratio. |
| Pierce oscillator | A Colpitts-derived oscillator with a quartz crystal replacing the inductor, giving very high frequency stability. |
| Crystal control | Using a quartz crystal's mechanical resonance to fix a transmitter's frequency far more stably than an LC tank. |
| Q (quality factor) | The dimensionless sharpness of a resonant circuit, Q = f₀ / BW, governing selectivity and losses. |
| Neutralization | A feedback-cancelling network that nulls a tube's plate-to-grid capacitance to prevent parasitic self-oscillation in an RF amplifier. |
| AGC (automatic gain control) | Feedback that reduces receiver gain on strong signals to level output and prevent overload. |
| AM (amplitude modulation) | Impressing audio on a carrier by varying its amplitude, producing a carrier plus two sidebands. |
| Plate modulation | AM produced by varying the high-voltage plate supply of the RF power-amplifier stage. |
| Pentode | A five-electrode tube adding screen and suppressor grids to a triode for higher gain and reduced neutralization need. |
| Class-C amplifier | An amplifier biased beyond cutoff, conducting under half a cycle, offering high efficiency but only for constant-envelope modes. |
| Pi-network | A π-shaped LC output-matching network that matches a wide impedance range while filtering harmonics. |
| Crystal (IF) filter | A quartz-based bandpass filter in the IF strip giving very sharp, high-Q selectivity. |
| Yagi–Uda antenna | A directional beam using parasitic reflector and director elements alongside a driven element. |
| Ionospheric skip | Sky-wave propagation in which shortwave signals refract off the ionosphere back to earth far beyond the horizon. |
| Skip zone | The dead annulus between a signal's ground-wave limit and its first sky-wave return, where no reception occurs. |
| FM (frequency modulation) | Impressing information on a carrier by varying its instantaneous frequency rather than amplitude. |
| Deviation | The peak amount an FM carrier's frequency swings above and below centre in response to modulation. |
| Carson's rule | An estimate of FM occupied bandwidth, BW = 2(Δf + f_m), capturing ~98% of the signal's power. |
| Capture effect | An FM receiver's tendency to reproduce only the stronger of two co-channel signals once it leads by a few dB. |
| Discriminator | An FM demodulator that converts instantaneous frequency deviation back into an audio voltage. |
| SSB (single sideband) | A bandwidth- and power-efficient mode transmitting one sideband of an AM signal with the carrier and other sideband suppressed. |
| Balanced modulator | A circuit that multiplies carrier and audio to output both sidebands while cancelling the carrier by symmetry (DSBSC). |
| Product detector | A receive-side mixer that demodulates a suppressed-carrier SSB/CW signal against a local carrier/BFO. |
| Filter method | SSB generation removing the unwanted sideband with a sharp bandpass (crystal or mechanical) filter. |
| Phasing method | SSB generation cancelling the unwanted sideband by combining two 90°-quadrature balanced-modulator outputs. |
| BJT common-emitter | The workhorse transistor amplifier stage giving both voltage and current gain with inverted output. |
| Repeater | An automatic station that receives on one frequency and simultaneously retransmits on another to extend range. |
| CTCSS | A sub-audible continuous tone (~67–254 Hz) carried on the signal to control repeater access and prevent co-channel triggering. |
| Transponder | A satellite payload that receives an uplink band and retransmits it, shifted, on a downlink band (linear transponders relay a whole slice). |
| Doppler shift | The frequency offset Δf = f·v/c caused by a satellite's line-of-sight motion relative to the ground station. |
| PLL (phase-locked loop) | A control loop that locks a VCO to a divided reference, enabling programmable frequency synthesis. |
| VCO | A voltage-controlled oscillator whose output frequency is steered by a control voltage, the tunable element of a PLL. |
| AX.25 | The amateur packet-radio link-layer protocol, an HDLC-framed derivative of X.25 addressed by callsign + SSID. |
| Digipeater | A digital repeater that relays AX.25 packet frames hop-by-hop along a path listed in the frame. |
| SSID | The 0–15 Secondary Station Identifier suffix distinguishing multiple logical stations under one callsign. |
| AMTOR | An amateur teleprinter mode with 4-of-7 error-detecting coding, run in FEC or ARQ, adapted from maritime SITOR. |
| ARQ | Automatic Repeat reQuest: an error-recovery scheme that acknowledges good data and retransmits what was not acknowledged. |
| TNC (Terminal Node Controller) | The modem-plus-controller that assembles and disassembles AX.25 packets between a computer and a radio. |
| I/Q | The In-phase and Quadrature (90°-apart) baseband pair that jointly preserves a signal's amplitude and phase for DSP. |
| Direct conversion | An SDR/receiver architecture mixing RF straight to 0 Hz baseband in one step rather than via an IF. |
| FFT waterfall | A scrolling time-vs-frequency display built from successive Fast Fourier Transforms of sampled data. |
| SDR (software-defined radio) | A radio in which demodulation, filtering, and mode decoding are done in software/DSP on digitized I/Q rather than fixed analog hardware. |
| PSK31 | A 31.25-baud BPSK keyboard mode ~31 Hz wide using Varicode, designed for efficient live HF conversation. |
| Varicode | A variable-length character code (common letters shorter) with self-synchronizing gaps, used by PSK31. |
| FT8 | A weak-signal 8-FSK mode on timed 15-second cycles with LDPC coding, decodable well below the noise floor. |
| LDPC | Low-Density Parity-Check: a powerful forward-error-correction code (FT8 uses a (174,91) codeword). |
| Vocoder | A low-bit-rate voice codec (e.g. AMBE/AMBE+2) that compresses speech for digital-voice modes before framing and modulation. |
