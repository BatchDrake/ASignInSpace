This is over 1300 permutations of binary operations performed on the message data. Note that for now this is all on the FULL message data. 

So, for 3 chunk sizes: 1, 4, 8, I perform up to 4 binary operations (combinations of rotation, sum, and, or, xor). If the resulting file is non-zero and different from the original, I save it.

Then, for each of those >1300 binaries, I did basic 1bpp and byte-wise color visualizations.

Finally, each of those files ALSO has been searched for any repeating sequences of bytes (which don't start or end with 0x00) of lengths 3-12 bytes (searched up to 16, nothing found past 12 in any of them).

I also included the code for all of this.
