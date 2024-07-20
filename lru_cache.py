class ListNode:
    def __init__(self, key=0, val=0, left=None, right=None) -> None:
        self.key = key
        self.val = val
        self.left = left
        self.right = right

class LRUCache:
    def __init__(self, capacity) -> None:
        self.capacity = capacity
        self.head = ListNode()
        self.tail = ListNode()
        self.head.right = self.tail
        self.tail.left = self.head
        self.cache = {}  # key : value(ListNode)

    # delete node from doubly linked list
    def delete(self, node: ListNode):
        node.left.right = node.right
        node.right.left = node.left
    
    # add node at tail
    def add(self, node: ListNode):
        self.tail.left.right = node
        node.left = self.tail.left
        self.tail.left = node
        node.right = self.tail

    def get(self, key):
        if key in self.cache:
            node = self.cache[key]
            self.delete(node)
            self.add(node)
            return node.val
        else:
            # Incorrect: print(f'no \'{key}\' present in cache')
            # Correct: Return -1 if the key is not present
            return -1  

    def put(self, key, value):
        if key in self.cache:
            self.delete(self.cache[key])
        
        self.cache[key] = ListNode(key, value)
        self.add(self.cache[key])

        if len(self.cache) > self.capacity:
            del_key = self.head.right.key
            self.delete(self.head.right)
            del self.cache[del_key]
        
# Example usage:
cache = LRUCache(2)
cache.put(1, 1)
cache.put(2, 2)
print(cache.get(1))    # returns 1
cache.put(3, 3)        # evicts key 2
print(cache.get(2))    # returns -1 (not found)
cache.put(4, 4)        # evicts key 1
print(cache.get(1))    # returns -1 (not found)
print(cache.get(3))    # returns 3
print(cache.get(4))    # returns 4
