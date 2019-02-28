from random import randint


class PriorityQueue:
    """Array-based priority queue implementation."""

    def __init__(self):
        """Initially empty priority queue."""
        self.queue = []
        self.min_index = None

    def __len__(self):
        # Number of elements in the queue.
        return len(self.queue)

    def append(self, key):
        """Inserts an element in the priority queue."""
        if key is None:
            raise ValueError('Cannot insert None in the queue')
        self.queue.append(key)
        self.min_index = None
        self._min_heapify_up(len(self.queue)-1)

    def _min_heapify_up(self, node):
        """
        Heapify upwards when new node is added
        """
        if(not node):
            return
        parent = (node-1)//2
        if((self.queue[node] < self.queue[parent])):
            (self.queue[node], self.queue[parent]) = (
                self.queue[parent], self.queue[node])
            self._min_heapify_up(parent)

    def _min_heapify_down(self, node):
        if(node > (len(self.queue)-1)//2):
            return
        smallest = node
        left = (node*2) + 1
        right = (node*2) + 2
        if ((left < len(self.queue)) and (self.queue[left] < self.queue[node])):
            smallest = left
        if ((right < len(self.queue)) and (self.queue[right] < self.queue[smallest])):
            smallest = right
        if smallest != node:
            (self.queue[smallest], self.queue[node]) = (
                self.queue[node], self.queue[smallest])
            self._min_heapify_down(smallest)

    def min(self):
        """The smallest element in the queue."""
        if len(self.queue) == 0:
            return None
        self._find_min()
        return self.queue[self.min_index]

    def pop(self):
        """Removes the minimum element in the queue.

        Returns:
            The value of the removed element.
        """
        if len(self.queue) == 0:
            return None
        self._find_min()
        (self.queue[0], self.queue[len(self.queue)-1]) = (
            self.queue[len(self.queue) - 1], self.queue[0])
        popped_key = self.queue.pop()
        self._min_heapify_down(0)
        #for i in range((len(self.queue)-1)//2, -1, -1):
        #    self._min_heapify_down(i)
        self.min_index = None
        return popped_key

    def _find_min(self):
        # Computes the index of the minimum element in the queue.
        #
        # This method may crash if called when the queue is empty.
        if self.min_index is not None:
            return
        self.min_index = self.queue[0]


if __name__ == '__main__':
    p = PriorityQueue()
    for i in range(10):
        p.append(randint(0, 100))
    print(p.pop())
    print(p.pop())
    print('done')
