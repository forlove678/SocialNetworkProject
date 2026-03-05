"""
堆数据结构实现
用于Top-K推荐等场景
"""


class MaxHeap:
    """最大堆实现"""

    def __init__(self, capacity=None):
        """
        初始化最大堆
        :param capacity: 堆的最大容量（可选）
        """
        self.heap = []
        self.capacity = capacity

    def push(self, item):
        """
        插入元素
        时间复杂度：O(log n)
        """
        if self.capacity and len(self.heap) >= self.capacity:
            # 如果堆已满，比较堆顶
            if item[0] < self.heap[0][0]:
                return  # 新元素小于堆顶，不插入

        self.heap.append(item)
        self._sift_up(len(self.heap) - 1)

        # 如果超过容量，弹出最小的
        if self.capacity and len(self.heap) > self.capacity:
            self._pop_min()

    def pop(self):
        """
        弹出堆顶元素
        时间复杂度：O(log n)
        """
        if not self.heap:
            return None

        if len(self.heap) == 1:
            return self.heap.pop()

        top = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._sift_down(0)
        return top

    def _sift_up(self, index):
        """上浮操作"""
        parent = (index - 1) // 2
        while index > 0 and self.heap[index][0] > self.heap[parent][0]:
            self.heap[index], self.heap[parent] = self.heap[parent], self.heap[index]
            index = parent
            parent = (index - 1) // 2

    def _sift_down(self, index):
        """下沉操作"""
        n = len(self.heap)
        while True:
            largest = index
            left = 2 * index + 1
            right = 2 * index + 2

            if left < n and self.heap[left][0] > self.heap[largest][0]:
                largest = left
            if right < n and self.heap[right][0] > self.heap[largest][0]:
                largest = right

            if largest == index:
                break

            self.heap[index], self.heap[largest] = self.heap[largest], self.heap[index]
            index = largest

    def _pop_min(self):
        """弹出最小的元素（用于容量控制）"""
        if not self.heap:
            return None

        # 找到最小元素索引
        min_index = 0
        for i in range(1, len(self.heap)):
            if self.heap[i][0] < self.heap[min_index][0]:
                min_index = i

        # 交换到末尾并弹出
        if min_index != len(self.heap) - 1:
            self.heap[min_index], self.heap[-1] = self.heap[-1], self.heap[min_index]

        return self.heap.pop()

    def peek(self):
        """查看堆顶元素"""
        return self.heap[0] if self.heap else None

    def is_empty(self):
        """检查堆是否为空"""
        return len(self.heap) == 0

    def size(self):
        """获取堆大小"""
        return len(self.heap)


class MinHeap:
    """最小堆实现"""

    def __init__(self, capacity=None):
        self.heap = []
        self.capacity = capacity

    def push(self, item):
        if self.capacity and len(self.heap) >= self.capacity:
            if item[0] > self.heap[0][0]:
                return

        self.heap.append(item)
        self._sift_up(len(self.heap) - 1)

        if self.capacity and len(self.heap) > self.capacity:
            self._pop_max()

    def pop(self):
        if not self.heap:
            return None

        if len(self.heap) == 1:
            return self.heap.pop()

        top = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._sift_down(0)
        return top

    def _sift_up(self, index):
        parent = (index - 1) // 2
        while index > 0 and self.heap[index][0] < self.heap[parent][0]:
            self.heap[index], self.heap[parent] = self.heap[parent], self.heap[index]
            index = parent
            parent = (index - 1) // 2

    def _sift_down(self, index):
        n = len(self.heap)
        while True:
            smallest = index
            left = 2 * index + 1
            right = 2 * index + 2

            if left < n and self.heap[left][0] < self.heap[smallest][0]:
                smallest = left
            if right < n and self.heap[right][0] < self.heap[smallest][0]:
                smallest = right

            if smallest == index:
                break

            self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
            index = smallest

    def _pop_max(self):
        if not self.heap:
            return None

        max_index = 0
        for i in range(1, len(self.heap)):
            if self.heap[i][0] > self.heap[max_index][0]:
                max_index = i

        if max_index != len(self.heap) - 1:
            self.heap[max_index], self.heap[-1] = self.heap[-1], self.heap[max_index]

        return self.heap.pop()