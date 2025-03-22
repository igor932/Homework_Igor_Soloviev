class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
        self.previous = None

class DoubleLinkedList:
    def __init__(self, cycle=False):
        self.head = None
        self.tail = None
        self.length = 0
        self.cycle = cycle

    def __str__(self):
        if self.length == 0:
            return "Empty list"
        current = self.head
        result = []
        while current:
            result.append(str(current.value))
            current = current.next
            if current == self.head:
                break
        return " <-> ".join(result)

    def add_to_head(self, value):
        new_node = Node(value)
        if self.length == 0:
            self.head = self.tail = new_node
            if self.cycle:
                self.head.next = self.tail
                self.tail.previous = self.head
        else:
            new_node.next = self.head
            self.head.previous = new_node
            self.head = new_node
            if self.cycle:
                self.tail.next = self.head
                self.head.previous = self.tail
        self.length += 1

    def add_to_tail(self, value):
        new_node = Node(value)
        if self.length == 0:
            self.head = self.tail = new_node
            if self.cycle:
                self.head.next = self.tail
                self.tail.previous = self.head
        else:
            new_node.previous = self.tail
            self.tail.next = new_node
            self.tail = new_node
            if self.cycle:
                self.tail.next = self.head
                self.head.previous = self.tail
        self.length += 1

    def remove_all_occurrences(self, value):
        if self.length == 0:
            return
        
        current = self.head
        count = 0 
        while count < self.length:
            if current.value == value:
                if current == self.head:
                    self.remove_from_head()
                    current = self.head
                elif current == self.tail:
                    self.remove_from_tail()
                    current = None
                else:
                    next_node = current.next
                    current.previous.next = current.next
                    current.next.previous = current.previous
                    self.length -= 1
                    current = next_node
            else:
                current = current.next
            count += 1

    def __iter__(self):
        self._iter_node = self.head
        self._iter_count = 0
        return self

    def __next__(self):
        if self._iter_node is None or self._iter_count >= self.length:
            raise StopIteration
        value = self._iter_node.value
        self._iter_node = self._iter_node.next
        self._iter_count += 1
        return value

    def remove_from_head(self):
        if self.length == 0:
            raise IndexError("List is empty")
        value = self.head.value
        if self.length == 1:
            self.head = self.tail = None
        else:
            self.head = self.head.next
            self.head.previous = None
            if self.cycle:
                self.tail.next = self.head
                self.head.previous = self.tail
        self.length -= 1
        return value

    def remove_from_tail(self):
        if self.length == 0:
            raise IndexError("List is empty")
        value = self.tail.value
        if self.length == 1:
            self.head = self.tail = None
        else:
            self.tail = self.tail.previous
            self.tail.next = None
            if self.cycle:
                self.tail.next = self.head
                self.head.previous = self.tail
        self.length -= 1
        return value

    def remove_at_index(self, index):
        if index < 0 or index >= self.length:
            raise IndexError("Index out of range")
        if index == 0:
            return self.remove_from_head()
        elif index == self.length - 1:
            return self.remove_from_tail()
        else:
            current = self.head
            for _ in range(index):
                current = current.next
            value = current.value
            current.previous.next = current.next
            current.next.previous = current.previous
            self.length -= 1
            return value

    def reverse(self):
        new_list = DoubleLinkedList(self.cycle)
        current = self.tail
        while current:
            new_list.add_to_tail(current.value)
            current = current.previous
            if current == self.tail:
                break
        return new_list

dll = DoubleLinkedList(cycle=True)
dll.add_to_tail(1)
dll.add_to_tail(2)
dll.add_to_tail(3)
dll.add_to_tail(4)
print(dll)  

dll.add_to_head(0)
print(dll) 

dll.insert_at_index(2, 1.5)
print(dll)  

dll.remove_at_index(2)
print(dll)  

dll.remove_all_occurrences(1)
print(dll)  

reversed_dll = dll.reverse()
print(reversed_dll)  

for item in dll:
    print(item, end=" ")
