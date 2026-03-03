class MaxHeap:
    def __init__(self):
        self.heap = []

    def push(self, val):
        self.heap.append(val)
        self._sift_up(len(self.heap) - 1)

    def _sift_up(self, idx):
        parent = (idx - 1) // 2
        if idx > 0 and self.heap[idx][2] > self.heap[parent][2]: # 以兴趣数排序
            self.heap[idx], self.heap[parent] = self.heap[parent], self.heap[idx]
            self._sift_up(parent)

    def pop(self):
        if len(self.heap) == 0: return None
        res = self.heap[0]
        self.heap[0] = self.heap[-1]
        self.heap.pop()
        if self.heap: self._sift_down(0)
        return res

    def _sift_down(self, idx):
        largest = idx
        left = 2 * idx + 1
        right = 2 * idx + 2
        if left < len(self.heap) and self.heap[left][2] > self.heap[largest][2]:
            largest = left
        if right < len(self.heap) and self.heap[right][2] > self.heap[largest][2]:
            largest = right
        if largest != idx:
            self.heap[idx], self.heap[largest] = self.heap[largest], self.heap[idx]
            self._sift_down(largest)