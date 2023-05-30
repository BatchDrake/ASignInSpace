---

# ASignInSpace
This repository intends to be a centralized place and primary reference for documentation on existing findings, visualizations, sonifications, and other data products (artifacts) resulting from the analysis of the message data.

## Directory structure
The provided signal recording can be seen as an onion with multiple layers of encoding (and not encryption). We had to decode the lowest-level ones in order to arrive at the top-level ones. The analysis of the signal recording is therefore structured in directories according to the layers we are referring to. Bottom-up, these directories are:

* [**1_PHY**](1_PHY/): Analysis of the physical layer (from raw signal samples to demodulated symbols).
* [**2_TM**](2_TM/): Analysis of the CCSDS TM Data Link frames (MAC layer).
* [**3_SPP**](3_SPP/): Analysis of the CCSDS Space Packets protocol (transport layer).
* [**4_APID_Streams**](4_APID_Streams/): Analysis of the contents of the application layer encapsulated by the space packets, on a per APID basis.

Additionally, the following directories are also included:

* [**Meta**](Meta/): Other ancillary information, like time analysis.
* [**Candidates**](Candidates/): **Actual first-contact message candidates**.

The layer directories have the following subdirectory structure:

* `README.md`: Summary of the current state of the analysis of this layer, with appropriate links to files in this subdirectory.
* `analysis/`: Text describing how the analysis was done.
* `artifacts/`: Data products resulting from this analysis (this is an **output** or **results** folder, used as input for the next layer).
* `doc/`: Documents and specifications needed to understand the nature of the data being analyzed here.
* `sonifications/`: Sonifications of the data inputs of this layer.
* `tools/`: Tools and scripts that generated the data product of this layer.
* `visual/`: Plots, images, and visualizations of the data inputs of this layer.