# TM artifacts

* **[frames.bin](frames.bin)**: decoded CCSDS TM data link frames. These frames are the vast majority of the data recorded by GBT, starting seconds after 19:11 UTC. No intermediate frames failed to decode, so this is a contiguous capture. This file has been produced by [ccsds-tool](../ccsds-tc) with the command line:

```
$ ccsds-tool -r 1/2 -f channel-capture-PM-52639-baud-0001.raw -S 15 > frames.bin
```
