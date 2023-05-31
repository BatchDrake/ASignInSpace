# Our First Candidate Message
This document provides a non-technical summary of how we arrived at a candidate for the simulated alien message. For a detailed technical journey, you may want to read [The Deep Dive into APID 0x17](../APID_Streams/analysis/README.md).

## What do we mean by "Candidate"?
"Candidate" refers to our best guess for the original simulated alien message. The use of this term emphasizes our high, but not absolute, confidence in the candidate. The original message, in whatever form, was converted into binary for transmission via a satellite. We have extracted one such possible ~8KB selection of binary data, from amongst ~4MB of all the "space packets" demodulated and extracted from the original raw radio data, based on extensive evidence. However, we can't confirm this binary data as the definitive message until/unless the creators of the project verify it.

## Understanding Binary and Hexadecimal Data
Binary data is simply data that can be represented as a sequence of 0s and 1s. This binary data can be saved as a *.bin file, which you can view, edit, visualize, sonify, or otherwise manipulate with various tools such as text editors, hex editors, audio software, or even data visualization software.

Binary data can also be represented in a more compact form using the hexadecimal (or hex) system, a base-16 system that uses numbers 0-9 and letters A-F. In this project, we provide the artifacts as raw binary files (.bin) and as hexadecimal data in CSV files (.csv).

## What are the "Artifacts"?
The artifacts are cleaned-up versions of the candidate message payload data, processed for easier analysis. They are provided as binary (*.bin) and CSV files containing hex data. You can find these artifacts in the [artifacts](./artificats/) directory. They offer different perspectives of the message payload, each with their own purpose and representation, details of which are covered extensively in the artifacts directory.

## Interpreting the Artifacts
The next step involves interpreting these artifacts. The concept of alignment is crucial here as it involves choosing how to arrange or divide the binary data. There are countless ways to do this. You might treat the raw data as rows of 256 bytes (provided, for the choice of 256-byte alignment specifically, you adjust for a discrepancy of 20 bytes for full payload), or divide it into several files of X bytes each. Alternatively, you could treat the data as a grid with a variable number of columns (e.g. by splitting at every packet/payload of 4 or 8 bytes as they were sent in the short or long packets), or consider different byte alignments (such as 16-bit or 32-bit). Perhaps you might even find some meaningful pattern when viewing the data in a spiral layout.

This interpretation aims to derive meaning from the message and understand the potential significance of its various aspects, such as the chosen order of short vs long packets.

We encourage anyone interested to explore these artifacts and contribute to interpreting the simulated alien message. Your unique perspective could be key in unlocking the secrets held within this data.
