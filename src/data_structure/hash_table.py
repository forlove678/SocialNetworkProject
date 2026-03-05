"""
哈希表实现 - 用于缓存用户信息
使用链地址法处理冲突
"""

class UserInfo:
    """用户信息类"""

    def __init__(self, user_id, name, interests=""):
        self.user_id = int(user_id)
        self.name = name
        self.interests = interests if interests else ""

    def __str__(self):
        return f"ID:{self.user_id} | {self.name} | 兴趣:{self.interests}"


class HashTable:
    """哈希表类 - 用于缓存用户信息"""

    def __init__(self, capacity=100):
        """
        初始化哈希表
        使用链地址法处理冲突
        """
        self.capacity = capacity
        self.size = 0
        self.buckets = [[] for _ in range(capacity)]

    def _hash(self, key):
        """哈希函数"""
        try:
            key = int(key)
            return hash(key) % self.capacity
        except:
            return hash(str(key)) % self.capacity

    def insert(self, key, value):
        """
        插入键值对
        时间复杂度：平均O(1)，最坏O(n)
        """
        try:
            key = int(key)
        except:
            return False, "键必须是数字"

        index = self._hash(key)
        bucket = self.buckets[index]

        # 检查key是否已存在
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)  # 更新
                return True, "用户信息更新成功"

        # 插入新键值对
        bucket.append((key, value))
        self.size += 1
        return True, "用户信息添加成功"

    def get(self, key):
        """
        根据key获取value
        时间复杂度：平均O(1)，最坏O(n)
        """
        try:
            key = int(key)
        except:
            return None

        index = self._hash(key)
        bucket = self.buckets[index]

        for k, v in bucket:
            if k == key:
                return v
        return None

    def delete(self, key):
        """
        删除键值对
        时间复杂度：平均O(1)，最坏O(n)
        """
        try:
            key = int(key)
        except:
            return False, "键必须是数字"

        index = self._hash(key)
        bucket = self.buckets[index]

        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket.pop(i)
                self.size -= 1
                return True, "用户信息删除成功"

        return False, "用户不存在"

    def contains(self, key):
        """检查key是否存在"""
        return self.get(key) is not None

    def get_all(self):
        """获取所有用户信息"""
        result = []
        for bucket in self.buckets:
            for k, v in bucket:
                result.append(v)
        return result

    def get_size(self):
        """获取元素数量"""
        return self.size