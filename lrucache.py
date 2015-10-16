class LRUCache:

    class Node:
        # initialization of one node
        def __init__(self, key, value):
            self.prev = None
            self.key = key
            self.value = value
            self.next = None

    def __init__(self, capacity):
        self.capacity = capacity
        self.dict = {}
        self.head = self.Node('head', 'head')
        self.tail = self.Node('tail', 'tail')
        self.head.next = self.tail
        self.tail.prev = self.head

    def insert_at_head(self, node):
        # update the next of this node
        node.next = self.head.next
        # update the prev of this node
        node.prev = self.head
        # update the prev of next to head node to this node
        self.head.next.prev = node
        # update the next of head node to this node
        self.head.next = node

    def delete_node(self, node):
        # update next of previous node
        node.prev.next = node.next
        # update prev of next node
        node.next.prev = node.prev
        node.prev = None
        node.next = None
        return node

    def get(self, key):
        if key in self.dict:
            # delete the node from list
            node_ptr = self.delete_node(self.dict[key])
            # and insert at head to mark it as the most recent one
            self.insert_at_head(node_ptr)
            return self.dict[key].value
        return -1

    def set(self, key, value):
        if key in self.dict:
            # delete the node from list
            node_ptr = self.delete_node(self.dict[key])
            # and insert at head to mark it as the most recent one
            self.insert_at_head(node_ptr)
            # update the value of the node
            self.dict[key].value = value
        else:
            if len(self.dict) >= self.capacity:
                # delete the last node
                del self.dict[self.delete_node(self.tail.prev).key]
            self.dict[key] = self.Node(key, value)
            self.insert_at_head(self.dict[key])
