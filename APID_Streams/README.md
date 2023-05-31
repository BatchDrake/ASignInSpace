# Classification of APID streams

[In the previous step](../SPP) we produced an `encap_001.bin` that contained a long stream of concatenated space packets. [According to the specification](../SPP/doc/133x0b2e1.pdf), the 6-byte header is optionally followed by a secondary header contained inside the packet's data field. However, the size of this secondary header cannot be determined from the header data, being mission-specific.

In order to determine the size of the secondary header, we resorted to a comparative approach, in which we observed the bytes that remained the same from packet to packet. We did it by means of [sppextract-csv.c](tools/sppextract-csv.c), which turns the `encap_001.bin` into a CSV with the APID and contents of the data field of each space packet.

```
$ gcc sppextract-csv.c -o sppextract-csv
$ ./sppextract-csv encap_001.bin > spp.csv
```

`sppextract-csv` already removes the idle packets from the CSV. We can therefore focus on the data packets, most of them containing a secondary header:

```
$ cat spp.csv | most
"34c9","00b3",231,"10 03 19 00 0d 88 80 cb cc cd 00 00 00 aa (...)
"34ca","00b3",283,"10 03 19 00 0d 88 80 ce b3 33 00 00 00 ab (...)
"3c5e","00f3",971,"10 03 19 00 0d 88 80 ce cc cd 00 00 00 87 (...)
"34ca","00b3",231,"10 03 19 00 0d 88 80 cf cc cd 00 00 00 aa (...)
"304b","0053",112,"10 03 19 00 0d 88 80 cf e6 66 00 00 00 2a (...)
"34f0","0018",133,"10 03 1a 00 0d 88 80 d1 e6 66 00 00 00 81 (...)
"34ca","00b3",656,"10 03 19 00 0d 88 80 d2 b3 33 00 00 00 b2 (...)
"34ca","00b3",231,"10 03 19 00 0d 88 80 d3 cc cd 00 00 00 aa (...)
(...)
```
From these and many other packets with a secondary, we observed that the structure of the first 10 bytes (e.g. `10 03 19 00 0d 88 80 cb cc cd`) changed very little from APID to APID. **We therefore assumed that the size of the secondary header was 10**.

We used this observation to write [apidextract.c](tools/apidextract.c). This tool works in a similar way as `sppextract-csv.c`, except that it accepts the size of the secondary header as second argument and produces a series of `apid_xxxx.bin` files containing the actual payload of the space packets, stripping the specified secondary header first:

```
$ gcc apidextract.c -o apidextract
$ ./apidextract encap_001.bin 10
SPP [34c9] -> APID 00b3 S (size =   231) : 10 03 19 00 0d 88 80 cb cc cd 00 00 00 aa b5 50 00 09 36 (...)
SPP [34ca] -> APID 00b3 S (size =   283) : 10 03 19 00 0d 88 80 ce b3 33 00 00 00 ab 02 00 01 3f 07 (...)
SPP [3c5e] -> APID 00f3 S (size =   971) : 10 03 19 00 0d 88 80 ce cc cd 00 00 00 87 01 19 01 01 01 (...)
SPP [34ca] -> APID 00b3 S (size =   231) : 10 03 19 00 0d 88 80 cf cc cd 00 00 00 aa b4 9f ff f9 36 (...)
SPP [304b] -> APID 0053 S (size =   112) : 10 03 19 00 0d 88 80 cf e6 66 00 00 00 2a 10 07 00 00 00 (...)
SPP [34f0] -> APID 0018 S (size =   133) : 10 03 1a 00 0d 88 80 d1 e6 66 00 00 00 81 12 11 00 11 03 (...)
SPP [34ca] -> APID 00b3 S (size =   656) : 10 03 19 00 0d 88 80 d2 b3 33 00 00 00 b2 32 2e 02 05 00 (...)
SPP [34ca] -> APID 00b3 S (size =   231) : 10 03 19 00 0d 88 80 d3 cc cd 00 00 00 aa 35 a7 ff f8 36 (...)
SPP [3c26] -> APID 0000 . (size =     8) : 00 2e 0d 88 80 d3 fb 0f
SPP [3297] -> APID 0163 S (size =   224) : 10 03 19 00 0d 88 80 d4 cc cd 00 00 00 75 80 16 01 48 00 (...)
(...)
```

From the output, the number in brackets determines the sequence number. The column after the APID number is marked with an `S` if a secondary header is present and with a `.` if it is not. The resulting [APID files](artifacts/APID) are the raw byte stream contained in the space packets of each APID, and are ready to be used as input of the next analysis step.

For further details about how APID streams were analyzed and filtered for likely message content, etc., including idnetification and cleaning of a strong message candidate, please see [The Deep Dive into APID 0x17](./analysis/).
