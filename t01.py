class HashTable:
    def __init__(self):
        self.size = 29
        self.table = [None] * self.size

    def hash(self, s):
        mult = 1
        hash_value = 0
        for c in s:
            hash_value += mult * ord(c)
            mult += 1
        return hash_value % self.size