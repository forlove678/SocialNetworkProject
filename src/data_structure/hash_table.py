class HashTable:
    def __init__(self, capacity=100):
        self.capacity = capacity
        self.table = [[] for _ in range(self.capacity)]

    def _hash(self, key):
        return hash(key) % self.capacity

    def insert(self, user_id, info):
        index = self._hash(user_id)
        for item in self.table[index]:
            if item[0] == user_id:
                item[1] = info
                return
        self.table[index].append([user_id, info])

    def get(self, user_id):
        index = self._hash(user_id)
        for item in self.table[index]:
            if item[0] == user_id:
                return item[1]
        return None