# Physical layer (PHY)
We performed the analysis of the physical layer on the Green Bank Telescope (GBT) capture, as it was the one with the highest signal-to-noise (SNR) ratio. While the full name of the modulation is probably "RESIDUAL CARRIER, PCM / PSK / PM-SQUAREWAVE", in practice it consists of two identical, symmetrical BPSK subcarriers around the residual carrier, transmitting the exact amount of information.

The analysis of the signal was done with [SigDigger](https://github.com/BatchDrake/SigDigger), along with the [AmateurDSN plugin](https://github.com/BatchDrake/AmateurDSN). While the amplitude is fairly stable, the whole signal is affected by Doppler drifts (caused by the TGO orbiting around Mars) up to -76 Hz/s and ground station lock commands. This was determined by locking a [PLL with a 64 Hz cut-off on a 6.5 kHz channel around the residual carrier](visual/drift.png).  In order to improve the reception and keep the subcarrier more or less in the same place in the spectrum, a fixed order-1 Doppler correction of approximately +76 Hz/s was applied to the full-rate (1 Msps) signal:

![visual/driftplot.png](Doppler drift plot along the capture)

The cyclostarionary analysis of the BPSK subcarrier showed that its symbol rate was 52.6 kbaud, and the automatic frequency correction of the remaining uncorrected part was performed by means of an order-2 Costas loop. The soft symbols were saved to an I/Q file, all of them contained in the Q plane.

![visual/bpsk.png](BPSK demodulation)

