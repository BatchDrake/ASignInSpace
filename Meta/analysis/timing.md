# Absolute packet timing
Once we managed to dump all the SPP packets and classify them by APID, we realized we had no idea where the message could be. We knew nonetheless two things:

* The message was expected to arrive at 19:16 UTC 
* The message took approximately 30 minutes to be transmitted

We therefore looked for a way to classify packets by time of occurrence and extract those that showed up for the first time in the time window of the message. This was easier said than done, as we did not find any time stamps in the headers and the exact location of each packet in the original bitstream is lost in the de-encapsulation process. We came up with the following solution:

1. Write [frames2stamped_packets.c](../tools/frames2stamped_packets.c) to extract SPP packets directly from the decoded TM data link frames and prefix them with an `offset` field, indicating the offset inside `frames.bin` in which each packet was found.
2. Write [sppextract-samplecount.c](../tools/sppextract-samplecount.c) to convert the prefixed frames into a CSV file (named [statistics.csv](../artifacts/statistics.csv))
3. Use [the following Jupyter Lab document](../tools/TimingAnalysis.ipynb) to produce occurrence plots of the packets per APID.

The stamped packets are created as:
```
$ gcc frames2stamped_packets.c -o frames2stamped_packets
$ ./frames2stamped_packets frames.bin
6591 frames
(xxx) FIRST FRAME
ENCAP FILE CREATED: spp_sc_001.bin
(28f) FRAME   124 [0fa]: 1097 bytes in the data field
(28f) FRAME   133 [0fb]: 1103 bytes in the data field
(28f) FRAME   134 [0fc]: 1103 bytes in the data field
(28f) FRAME   136 [0fd]: 1103 bytes in the data field
(28f) FRAME   142 [0fe]: 1103 bytes in the data field
(28f) FRAME   145 [0ff]: 1103 bytes in the data field
(28f) FRAME   147 [000]: 1103 bytes in the data field
(28f) FRAME   148 [001]: 1103 bytes in the data field
...
```

And they are converted to a CSV file with:

```
$ gcc sppextract-samplecount.c -o sppextract-samplecount
$ ./sppextract-samplecount spp_sc_001.bin > statistics.csv
```

The resulting CSV file can later be loaded by the Jupyter Lab document, which will produce the following occurence plot:

<img src="../visual/perapid.png" align="center" />

We clearly see something occurring at the expected arrival time! (red vertical line). If we filter out the packets that show up before the expected arrival time, we have a much cleaner plot:

<img src="../visual/perapid_filter.png" align="center" />

From which it is clear that APIDs 0012, 0016 and 0017 are our best candidate APIDs so far.
