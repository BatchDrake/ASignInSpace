## PRNG Noise analysis
The PRNG noise of the idle frames was extracted with the [deencap](../tools/deencap.c) tool, passing 7 as second argument, indicating that we are interested in the virtual channel 7:

```
$ gcc deencap.c -o deencap
$  ./deencap frames.bin 7                         
6591 frames
(xxx) FIRST FRAME
ENCAP FILE CREATED: encap_001.bin
(28f) FRAME   123 [081]: (idle data) 1103 bytes in the data field
(28f) FRAME   125 [082]: (idle data) 1103 bytes in the data field
(28f) FRAME   126 [083]: (idle data) 1103 bytes in the data field
(28f) FRAME   127 [084]: (idle data) 1103 bytes in the data field
(28f) FRAME   128 [085]: (idle data) 1103 bytes in the data field
(28f) FRAME   129 [086]: (idle data) 1103 bytes in the data field
(28f) FRAME   130 [087]: (idle data) 1103 bytes in the data field
(28f) FRAME   131 [088]: (idle data) 1103 bytes in the data field
(...)
```

The resulting `encap_001.bin` consists of bits of the idle channel PRNG noise. Using [lfsrcrack](../tools/lfsrcrack), we obtain the following output:

```
$ hexdump -C encap_001.bin | head -1               
00000000  16 3a cb 3c 7d d0 6b 6e  c1 6b ea a0 52 bc bb 81  |.:.<}.kn.k..R...|
$ lfsrcrack 'hex:16 3a cb 3c 7d d0 6b 6e'      
Direct: x^9 + x^4 + 1
D-form: D[ 0], D[ 5], D[ 9]

Inverse: x^10 + x^9 + x^5 + x^4 + x + 1
D-form: D[ 0], D[ 1], D[ 5], D[ 6], D[ 9], D[10]
```

This is, the LFSR generating this PRNG noise is based on the polynomial $D^9+D^5+1$. We observe the same polynomial in all the data of the VC 7. This is different from what the CCSDS TM Data Link layer specification recommends: $D^{32}+D^{22}+D^2+D+1$.
