import mmh3
import math
from collections import defaultdict

class HyperLogLogPlusPlus:
    """Implements the HyperLogLog++ algorithm for cardinality estimation."""
    def __init__(self, p=14, p_prime=25):
        """Initialize with precision parameters."""
        self.p = p  
        self.p_prime = p_prime
        self.m = 2**p
        self.m_prime = 2**p_prime
        self.alpha_m = 0.7213 / (1 + 1.079 / self.m)
        self.format = 'SPARSE'
        self.tmp_set = set()
        self.sparse_list = set()
        self.M = defaultdict(int)

    def linear_counting(self, V):
        """ format linear counting"""
        return {"H": self.m_prime, "O": V}

    def threshold(self):
        """placeholder for actual threshold calculations"""
        return 10
    
    def encode_hash(self, x):
        """Encodes the hash code x as an integer"""
        hash_value = mmh3.hash64(x, signed=False)[0]
        x_bits = bin(hash_value)[2:].zfill(64)
        index = int(x_bits[:self.p], 2)
        remainder = x_bits[self.p:]
        w = int(remainder, 2)
        return index, w
    
    def decode(self, k):
        """Decode hash value"""
        r = (k >> (64 - self.p))
        return (r, (64 - self.p_prime + r))
    
    def to_normal(self):
        """Converts from sparse to normal formats"""
        self.M = defaultdict(int)
        for k in self.sparse_list:
            idx, r = self.decode_hash(k)
            self.M[idx] = max(self.M[idx], r)

    @staticmethod
    def merge(a,b):
        """ merge two sorted sets"""
        merged = []
        a_list = list(a)
        b_list = list(b)

        i= j = 0

        while i < len(a) and j < len(b):
            if a[i] == b[j]:
                merged.append(a_list[i])
                i +=1 
                j += 1
            elif a[i]  < b[j]:
                merged.append(a_list[i])
                i += 1
            else:
                merged.append(b_list[j])
                j += 1
        merged.extend(a_list[i:])
        merged.extend(b_list[j:])
        return merged 
    def estimate_cardinality(self, S):
        """ Estimates the cardinality of the set S"""
        for v in S:
            x = v.encode("utf-8") if isinstance(v, str) else bytes(v)
            if self.format == "NORMAL":
                idx, w = self.encode_hash(x)
                self.M[idx] = max(self.M[idx], w)
            else:
                k = self.encode_hash(x)
                self.tmp_set.add(k)
                if len(self.tmp_set) > self.threshold(): # constant 
                    self.format = "NORMAL"
                    self.sparse_list = self.merge(self.sparse_list, sorted(self.tmp_set))
                    self.tmp_set = set()
                    self.to_normal()

        if self.format == "SPARSE":
            self.sparse_list = self.merge(self.sparse_list, sorted(self.tmp_set))
            return self.linear_counting(len(self.sparse_list))["O"]
        
        E = self.alpha_m * self.m_prime**2 / sum(2**-v for v in self.M.values())
        bias = self.alpha_m * E
        return round(E - bias)

    

# Example usage
data = [
    "apple", "banana", "apple", "orange", "grape", 
    "banana", "mango", "apple", "grapefruit", "pear", "koko"
]

hllpp = HyperLogLogPlusPlus()
estimated_cardinality = hllpp.estimate_cardinality(data)

print("Estimated number of unique products:", estimated_cardinality)
