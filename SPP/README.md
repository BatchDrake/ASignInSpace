# SPP layer

The SPP (**Space Packet Protocol**) layer is the transport layer of the TGO's downlink. It is documented in the [Space Packet Protocol specification](doc/133x0b2e1.pdf). It basically consists of a series of non-empty packets of variable length, multiplexed by certain number named APID (Application Process IDentifier), akin to the port of a TCP / UDP packet. 

While APIDs are mostly mission specific, some are defined by the specification (like 0 for the timestamp and `0x7ff` for idle space packets).

All of the space packets are located in the **virtual channel 0** of the TM Data Link layer, and can be extracted by means of the [deencap](../TM/tools/deencap.c) program:

```
$ gcc deencap.c -o deencap
$ ./deencap frames.bin 0
6591 frames
(xxx) FIRST FRAME
ENCAP FILE CREATED: encap_001.bin
(28f) FRAME   124 [0fa]: 1097 bytes in the data field
(28f) FRAME   133 [0fb]: 1103 bytes in the data field
(28f) FRAME   134 [0fc]: 1103 bytes in the data field
(28f) FRAME   136 [0fd]: 1103 bytes in the data field
(28f) FRAME   142 [0fe]: 1103 bytes in the data field
...
```

`deencap` will analyze both the virtual channel ID and master channel counter of the TM frames in order to determine at which points a frame was lost. Every time a frame is lost, a new `encap_xxx.bin` is created, with `xxx` being incremented in one unit with respect to the previous one.

Every `encap_xxx.bin` is aligned to the first byte of the header of the first packet found in the TM frames, right after its creation. If no TM frames were lost, only one encap file (`encap_001.bin`) is created.

In our case, only [encap_001.bin](artifacts/encap_001.bin) was created, meaning that **no packets were lost during the recording of the signal**.
