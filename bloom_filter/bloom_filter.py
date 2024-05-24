from bitarray import bitarray
import mmh3

class BloomFilter:
    def __init__(self, size, hash_count):
        self.size = size 
        self.hash_count = hash_count
        self.ba = bitarray(size) 
        self.ba.setall(0)

    def add(self, item):
        for i in range(self.hash_count):
            idx = mmh3.hash(item, i) % self.size 
            self.ba[idx] = 1 

    def check(self, item):
        for i in range(self.hash_count):
            idx = mmh3.hash(item, i) % self.size 
            if self.ba[idx] == 0 :
                 return False 
        return True  

class SpellChecker:
    def __init__(self, d):
        self.bf = BloomFilter(5000, 7)
        for w in d:
            self.bf.add(w)

    def check(self, w):
        return self.bf.check(w)

d = ["apple", "banana", "orange", "grape", "watermelon"]

sp = SpellChecker(d)

print(sp.check("apple"))
print(sp.check("app"))

