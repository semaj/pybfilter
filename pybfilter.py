import math
import mmh3

LN2SQUARED = math.pow(math.log(2), 2)
LN2 = math.log(2)

class BFilter:
    def __init__(self, elements, fprate, ntweak = 0):
        size = -1.0 / LN2SQUARED * elements * math.log(fprate)
        filter_size = int(math.floor(size / 8.0))
        self.vdata = bytearray(filter_size);
        self.nhashfuncs = int(math.floor(filter_size * 8.0 / elements * LN2))
        self.ntweak = ntweak

    def hash(self, hashnum, data):
        seed = hashnum #((hashnum * 0xFBA4C795) + self.ntweak) & 0xFFFFFFFF
        hsh = mmh3.hash(data, seed)
        if hsh < 0:
            hsh = (1 << 32) + hsh
        return hsh % (len(self.vdata) * 8)

    def insert(self, data):
        for i in range(0, self.nhashfuncs):
            index = self.hash(i, data)
            position = 1 << (7 & index)
            self.vdata[index >> 3] |= position
        return self

    def contains(self, data):
        if (len(self.vdata) == 0):
            return False
        for i in range(0, self.nhashfuncs):
            index = self.hash(i, data)
            if (self.vdata[index >> 3] & (1 << (7 & index)) == 0):
                return False
        return True

    def clear(self):
        self.vdata = bytearray(len(self.vdata))




