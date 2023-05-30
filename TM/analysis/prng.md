## PRNG Noise analysis
The PRNG noise of the idle frames was extracted with the [deencap](../tools/deencap.c) tool, passing 7 as second argument, indicating that we are interested in the virtual channel 7:

```
$ gcc deencap.c -o deencap
$  ./deencap frames.bin 7 | head                                 
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
00000010  ce 93 d7 51 21 9c 2f 6c  d0 ef 0f f8 3d f1 73 20  |...Q!./l....=.s |
00000020  94 ed 1e 7c d8 a9 1c 6d  5c 4c 44 02 11 84 e5 58  |...|...m\LD....X|
00000030  6f 4d c8 a1 5a 7e c9 2d  f9 35 33 01 8c a3 4b fa  |oM..Z~.-.53...K.|
00000040  2c 75 96 78 fb a0 d6 dd  82 d7 d5 40 a5 79 77 03  |,u.x.......@.yw.|
00000050  9d 27 ae a2 43 38 5e d9  a1 de 1f f0 7b e2 e6 41  |.'..C8^.....{..A|
00000060  29 da 3c f9 b1 52 38 da  b8 98 88 04 23 09 ca b0  |).<..R8.....#...|
00000070  de 9b 91 42 b4 fd 92 5b  f2 6a 66 03 19 46 97 f4  |...B...[.jf..F..|
00000080  58 eb 2c f1 f7 41 ad bb  05 af aa 81 4a f2 ee 07  |X.,..A......J...|
00000090  3a 4f 5d 44 86 70 bd b3  43 bc 3f e0 f7 c5 cc 82  |:O]D.p..C.?.....|
$ lfsrcrack 'hex:16 3a cb 3c 7d d0 6b 6e'      
Direct: x^9 + x^4 + 1
D-form: D[ 0], D[ 5], D[ 9]

Inverse: x^10 + x^9 + x^5 + x^4 + x + 1
D-form: D[ 0], D[ 1], D[ 5], D[ 6], D[ 9], D[10]
```

This is, the LFSR generating this PRNG noise is based on the polynomial $D^9+D^5+1$. We observe the same polynomial in all the data of the VC 7. This is different from what the CCSDS TM Data Link layer specification recommends: $D^{32}+D^{22}+D^2+D+1$.
