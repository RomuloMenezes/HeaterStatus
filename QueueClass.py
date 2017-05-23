class Queue:
    limitSize = 0

    def __init__(self, limit_size = -1):
        self.items = list()
        self.limitSize = limit_size

    @property
    def is_empty(self):
        return self.items == []

    @property
    def size(self):
        return len(self.items)

    def enqueue(self, item):
        if self.limitSize == -1:
            self.items.insert(0, item)
        else:
            if self.size < self.limitSize:
                self.items.insert(0, item)
            else:
                for i in range(self.limitSize - 1, 0, -1):
                    self.items[i] = self.items[i - 1]
                self.items[0] = item

    def dequeue(self):
        return self.items.pop()

    def reset_queue(self):
        self.items = []
