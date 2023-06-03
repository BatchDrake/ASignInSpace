# Candidate Message Artifacts
This directory contains a set of artifacts which are different representations of our candidate message. This message was derived from binary data transmitted via a satellite, which our team has identified as potentially being of significant interest. Please see, in particular, [The Deep Dive into APID 0x17](../../APID_Streams/analysis/README.md) for more details on how we got here.

The candidate message was transmitted within a total of 1800 packets which contained payloads of two distinct sizes: 4 bytes and 8 bytes. The division and/or order of these packets/payload lengths might carry significance in the interpretation of the message, but this remains a topic for further investigation.

Below, we describe each artifact by file name and explain its relevance.

## Binary Files
**[data17.bin](data17.bin)** ([in plain text too](data17.txt)): This is the complete message payload. It represents the raw binary form of the candidate message, extracted from the transmission data.

data17_short.bin, data17_long.bin: These files contain the payload separated into two files based on payload/packet size: one for 4-byte payloads (short) and one for 8-byte payloads (long). This separation might be significant and could reveal patterns not readily observable in the combined data.

data17square.bin: This file, known as the "starmap" payload, contains the full message payload minus the first and last 10 bytes. This results in a binary file with a number of bytes that is a perfect square, potentially offering unique insights when the data is arranged in a 2D grid. The specific selection of which 20 bytes to exclude was performed by BatchDrake - #TODO: document this.

## Hexadecimal Files (as CSV)
data17.csv: This file contains the complete message payload represented as hexadecimal values, each byte represented as a separate value in the CSV.

data17_short.csv, data17_long.csv: These files contain the payload separated into two files based on packet size: one for 4-byte payloads (short) and one for 8-byte payloads (long), represented as hexadecimal values in a CSV.

data17square.csv: This is the "starmap" payload represented as hexadecimal values in a CSV.

data17_packet_rows.csv, data17_short_packet_rows.csv, data17_long_packet_rows.csv: These are CSV files similar to data17.csv, data17_short.csv, and data17_long.csv, respectively, but with newlines added at each packet boundary. This format may provide clearer insights into patterns within the data.

The specific interpretation of these artifacts is still under investigation, and we encourage anyone interested to explore these files. Understanding these artifacts could be key to unlocking the secrets held within the candidate message.
