# The Deep Dive into APID 0x17
This document details our path from the complete dump of Space Packet Protocol (SPP) packets to focusing on APID 0x17, and finally identifying the specific message payload within it, which forms the crux of this narrative.

## 1. Initial APID Stream Separation
Our journey began with an extensive dump of SPP packets, derived from the TM data frames. We parsed the SPP headers, including the timestamps (detailing of which would be expanded later - #TODO), which, along with the last two bytes identified as a Cyclic Redundancy Check (CRC), helped us to define the boundaries of the headers and footers. Thus, we could create separate streams for each APID, enabling a targeted analysis.

## 2. Narrowing Down APID Selection
We used a short baseline of recordings captured by the observatories before the expected arrival of the simulated alien signal. By comparing the data from the baseline with the full capture, we were able to exclude APIDs that were present in the baseline, leading to a shortlist of potential APIDs.

Our attention was particularly drawn to APIDs 0x12, 0x16, and 0x17 because of their total size, as well as their timing correlation with the expected signal arrival. In particular, 0x12 and 0x16 contained nothing but identical headers, counters, and checksums. #TODO: Expand on the evidence leading to this conclusion.

During this phase, BatchDrake (EA1IYR) identify the "starmap" data, which proved to be the payload data. At the time, the ISO checksum following that payload data was suspected but unverified. @HaileyStorm performed *extensive* permutations of binary operations and was unable to crack the ISO checksum, and then @skywalker made a significant contribution by reverse engineering an algorithm achieving around a 95% accuracy rate (#TODO - details of @skywalker's algorithm). While this effort was later unnecessary due to the discovery of the PUS ISO checksum documentation, it provides secondary evidence and insight into the checksum process (and the history of the process).

We also made preliminary investigations into a few remaining smaller, less chronologically correlated APIDs (0x43, 0xb2, 0x2f2, 0x152, 0x15b). However, due to their limited timing correlation with the expected signal arrival, these were not pursued deeply. Further investigation that was conducted on these APIDs will be added later - #TODO.

## 3. A Closer Look at APID 0x17
While we had already mostly zeroed in on APID 0x17, additional supporting evidence was found by @Kikuchiyo in the presence of distinct packets within APID 0x17 that matched a specific pattern described in the [Packet Utilization Standard (PUS)](https://cwe.ccsds.org/moims/docs/Work%20Completed%20(Closed%20WGs)/Packet%20Utilization%20Standard%20Birds%20of%20a%20Feather/Meeting%20Materials/200909%20Background/ECSS-E-70-41A(30Jan2003).pdf). This document describes the Data Field Header structure in each SPP packet, where the 2nd and 3rd bytes determine the service type and subtype.

Kikuchiyo, using a packet dissector script, visually checked all APID streams. The observations suggested that APID 0x17 was the only one likely to contain memory dump information, aligning well with the PUS' description.

## 4. Memory Dump Service and ISO Checksum Confirmation
The service type 06, as found in APID 0x17 packets, corresponds to the memory dump service, more specifically, "Memory Dump using Absolute Addresses Report (6,6)" as per the PUS document. 

Moreover, the specification describes an ISO checksum; the checksum which had previously been largely reverse engineered. Along with teh PUS header, these checksum bytes, 2 bytes for the short 0x17 packets and 4 bytes for the long 0x17 packets, do not hold any new, independent information but confirmed our understanding of the packet structure.

## 5. Pattern Analysis of Packet Sequences and Packet Lengths
Intriguingly, the 0x17 packets were surrounded by sequences of other APIDs, 0x12 and 0x16, in a specific pattern: 12 16 12 17 12 16. It appeared that each 4 or 8 byte packet of the actual message is triggered or accompanied with a sequence of three telecommands.

According to Kikuchiyo, the first and third commands are responded with a 0x16 packet. They are almost identical, except for a 1 in the first and a 0 in the last. The middle command results in the actual data packet. This sequencing suggested a process: "switch on something - ok, switched on - gimme a chunk of data - here it is - switch off the something - ok switched off."

Janishri confirmed that this interpretation matches the newer PUS standard description, 6.13.3.3.1 c 1 (a).

BatchDrake (EA1IYR) added that there were 1800 of these memory dump packets, 3600 of APID 16, and 5400 of APID 12, which aligns well with the interpretation of the sequencing and supports the theory.

Furthermore, in the livestream YouTube announcement of the project (starting at the 40 minute mark), one of the scientists mentioned loading 1800 instructions into the satellite. This correlates with the 1800 0x17 packets sent during the message interval/recording and the intentional choice of packet lengths.

## 6. Service Types and Command Sequences
Three 0x12 packets are of type-subtype 0101, 0103, 0107, respectively, which, according to the PUS standard, correspond to "command accepted", "command started", and "command completed". This further supported our interpretation of the packet sequencing as a series of command and response patterns.

## 7. Message Payload within APID 0x17
With the PUS header and checksum removed, the only remaining content in the 0x17 packets is the payload, 4 bytes for the short packets and 8 bytes for the long packets.

The specific interpretation of the payload is currently a subject of speculation and beyond the scope of this document. Our next steps will be to further understand the potential meaning of the chosen order of short vs long packets, and to continue interpreting the payload within APID 0x17.
