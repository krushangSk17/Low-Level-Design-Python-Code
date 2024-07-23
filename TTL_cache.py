import time

class Node:
    def __init__(self, key, value, expire_time):
        self.key = key
        self.value = value
        self.expire_time = expire_time
        self.prev = None
        self.next = None

class TTLCache:
    def __init__(self, capacity, ttl):
        self.capacity = capacity
        self.ttl = ttl
        self.cache = {}  # maps key to node
        self.head = Node(0, 0, 0)  # Dummy head
        self.tail = Node(0, 0, 0)  # Dummy tail
        self.head.next = self.tail
        self.tail.prev = self.head

    def _add_node(self, node):
        # Always add the new node right after head.
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def _remove_node(self, node):
        # Remove an existing node from the linked list.
        prev = node.prev
        next = node.next
        prev.next = next
        next.prev = prev

    def _move_to_head(self, node):
        # Move certain node in between to the head.
        self._remove_node(node)
        self._add_node(node)

    def _pop_tail(self):
        # Pop the current tail.
        res = self.tail.prev
        self._remove_node(res)
        return res

    def get(self, key):
        node = self.cache.get(key, None)
        if not node:
            return -1
        # Check if node has expired
        if node.expire_time < time.time():
            self._remove_node(node)
            del self.cache[key]
            return -1
        # Move the accessed node to the head.
        self._move_to_head(node)
        return node.value

    def put(self, key, value):
        node = self.cache.get(key)
        if not node:
            newNode = Node(key, value, time.time() + self.ttl)
            self.cache[key] = newNode
            self._add_node(newNode)
            if len(self.cache) > self.capacity:
                # Pop the tail
                tail = self._pop_tail()
                del self.cache[tail.key]
        else:
            # Update the value and the expiration time
            node.value = value
            node.expire_time = time.time() + self.ttl
            self._move_to_head(node)

# Usage Example
cache = TTLCache(2, 5)  # capacity 2, TTL 5 seconds
cache.put(1, 1)
print(cache.get(1))      # returns 1
time.sleep(6)
print(cache.get(1))      # returns -1, because it has expired
cache.put(2, 2)
print(cache.get(2))      # returns 2
cache.put(3, 3)          # evicts key 2
print(cache.get(2))      # returns -1, because 2 has been evicted
print(cache.get(3))      # returns 3
