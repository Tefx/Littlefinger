from bitarray import bitarray
from numpy.random import random_integers

class BloomFilter(object):
    def __init__(self, length=1000000, k=10):
        self.array = bitarray(length)
        self.length = length
        self.k = k

    def add(self, item):
        ks = random_integers(0, self.length-1, self.k)
        for k in ks:
            self.array[k] = True
        return ks

    def update(self, b1):
        self.array &= b1.array

    def __contains__(self, b):
        return not ((b.array & self.array) ^ self.array).any()


if __name__ == '__main__':
    bf = BloomFilter(50000, 7)
    b1 = BloomFilter(50000, 1)
    for i in xrange(10):
        for j in xrange(10):
            bf.update(b1)
        for k in xrange(5000):
            a = b1 in bf
