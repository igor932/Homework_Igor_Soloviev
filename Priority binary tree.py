class Node:
    def __init__(self, value: int, priority: int):
        self.value = value
        self.priority = priority
        self.left = None
        self.right = None

class Treap:
    def __init__(self):
        self.root = None

    def _rotate_right(self, node: Node) -> Node:
        left_child = node.left
        node.left = left_child.right
        left_child.right = node
        return left_child

    def _rotate_left(self, node: Node) -> Node:
        right_child = node.right
        node.right = right_child.left
        right_child.left = node
        return right_child

    def _insert(self, node: Node, value: int, priority: int) -> Node:
        if not node:
            return Node(value, priority)

        if value < node.value:
            node.left = self._insert(node.left, value, priority)
            if node.left and node.left.priority > node.priority:
                node = self._rotate_right(node)
        else:
            node.right = self._insert(node.right, value, priority)
            if node.right and node.right.priority > node.priority:
                node = self._rotate_left(node)

        return node

    def insert(self, value: int, priority: int):
        self.root = self._insert(self.root, value, priority)

    def _delete(self, node: Node, value: int) -> Node:
        if not node:
            return None

        if value < node.value:
            node.left = self._delete(node.left, value)
        elif value > node.value:
            node.right = self._delete(node.right, value)
        else:
            if not node.left:
                return node.right
            elif not node.right:
                return node.left
            else:
                if node.left.priority > node.right.priority:
                    node = self._rotate_right(node)
                    node.right = self._delete(node.right, value)
                else:
                    node = self._rotate_left(node)
                    node.left = self._delete(node.left, value)

        return node

    def delete(self, value: int):
        self.root = self._delete(self.root, value)

    def _inorder(self, node: Node):
        if node:
            self._inorder(node.left)
            print(f"Value: {node.value}, Priority: {node.priority}")
            self._inorder(node.right)

    def display(self):
        self._inorder(self.root)


if __name__ == "__main__":
    treap = Treap()


    treap.insert(10, 15)
    treap.insert(20, 10)
    treap.insert(5, 20)
    treap.insert(15, 5)
    treap.insert(25, 30)

    print("Дерево после вставки:")
    treap.display()


    treap.delete(10)

    print("\nДерево после удаления 10:")
    treap.display()
