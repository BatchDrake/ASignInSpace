#!/usr/bin/env python

from bitarray import bitarray, decodetree
import matplotlib.pyplot as plot

def group_acc(x, size):
    res = [0] * size
    for i, s in enumerate(x):
        res[i % size] += s
    return res

def graph_group_acc(x, size):
    res = group_acc(x, size)
    plot.bar(range(size), res)
    plot.show()

def main():
    with open("data17.bin", "rb") as f:
        # Load bits from file...
        bits = bitarray()
        bits.fromfile(f)
        t = decodetree({0x00: bitarray('0'), 0x01: bitarray('1')})
        r = bits.decode(t)
        # Discard first and last 10 bytes
        r = r[10*8:-10*8]
        for s in range(2, 60, 2):
            graph_group_acc(r, s)

if __name__ == "__main__":
    main()
