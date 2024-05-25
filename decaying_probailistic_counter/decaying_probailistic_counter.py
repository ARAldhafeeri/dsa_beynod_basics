import time 
import math
import hashlib

class DecayingProbailsticCounter:
    def __init__(self, size, hash_count, decay_rate):
        self.size = size
        self.hash_count = hash_count
        self.decay_rate = decay_rate
        self.counters = [0] * size 
        self.last_decay_time = time.time() 


    def _hashes(self, item):
        res = []
        for i in range(self.hash_count):
            hash_res = hashlib.md5((str(item) + str(i)).encode()).hexdigest()
            res.append(int(hash_res, 16) % self.size)
        return res

    def add(self, item):
        self._apply_decay() 
        for i in self._hashes(item):
            self.counters[i] = self.counters[i] + 1

    def remove(self, item):
        self._apply_decay() 
        for i in self._hashes(item):
            self.counters[i] = self.counters[i] - 1 

    def count(self, item):
        self._apply_decay()
        return min(self.counters[i] for i in self._hashes(item)) 

    def _apply_decay(self):
        current_time = time.time() 
        elapsed_time = current_time - self.last_decay_time
        decay_factor = math.exp(-self.decay_rate * elapsed_time) # exponential something 

        if decay_factor < 1:
            for i in range(self.size):
                self.counters[i] = int(self.counters[i] * decay_factor)
        self.last_decay_time = current_time


class NetworkA:
    def __init__(self, network_buckets):
        self.network_buckets = network_buckets
        self.dpc = DecayingProbailsticCounter(50000, 7, 0.32)
        for i in nb:
            self.dpc.add(i)

    def check(self, item):
        return self.dpc.count(item)

nb = ["01010101", "01010101", "01010111", "01010101", "01010111", "01010011", "01010111"]

na = NetworkA(nb)

print(na.check("01010111"))

# 90000k search query per second 
# ****** mb / s