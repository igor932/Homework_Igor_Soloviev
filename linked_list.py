class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        last = self.head
        while last.next:
            last = last.next
        last.next = new_node
    
    def remove_value(self, value):
        while self.head and self.head.data == value:
            self.head = self.head.next
        current = self.head
        while current and current.next:
            if current.next.data == value:
                current.next = current.next.next
            else:
                current = current.next
    
    def remove_duplicate(self):
        new_list = LinkedList()
        if not self.head:
            return new_list
        seen = set()
        current = self.head
        while current:
            if current.data not in seen:
                new_list.append(current.data)
                seen.add(current.data)
            current = current.next
        return new_list
    
    def __iter__(self):
        return LinkedListIterator(self.head)

    @staticmethod
    def merge(linked_list_1, linked_list_2):
        merged_list = LinkedList()
        dummy = Node(0)
        current = dummy
        l1, l2 = linked_list_1.head, linked_list_2.head
        while l1 and l2:
            if l1.data < l2.data:
                current.next = l1
                l1 = l1.next
            else:
                current.next = l2
                l2 = l2.next
            current = current.next
        current.next = l1 if l1 else l2
        merged_list.head = dummy.next
        return merged_list
    
    @staticmethod
    def compression(linked_list):
        if not linked_list.head:
            return linked_list
        compressed_list = LinkedList()
        compressed_list.append(linked_list.head.data)
        current = linked_list.head.next
        while current:
            if current.data != compressed_list.head.data:
                compressed_list.append(current.data)
            current = current.next
        return compressed_list

class LinkedListIterator:
    def __init__(self, head):
        self.head = head
        self.current = head

    def __iter__(self):
        return self

    def __next__(self):
        if not self.current:
            raise StopIteration
        data = self.current.data
        self.current = self.current.next
        return data
