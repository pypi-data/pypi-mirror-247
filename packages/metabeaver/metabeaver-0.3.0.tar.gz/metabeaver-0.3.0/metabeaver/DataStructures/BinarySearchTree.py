# Create a class to encapsulate our Binary Search Tree
class BinarySearchTree:

    def __init__(self):
        self.root = None

    def insert(self, value):
        new_node = Node(value)

        if self.root is None:
            self.root = new_node
        else:
            current_node = self.root

            while True:
                if value < current_node.value:
                    if current_node.left is None:
                        current_node.left = new_node
                        break
                    else:
                        current_node = current_node.left
                else:
                    if current_node.right is None:
                        current_node.right = new_node
                        break
                    else:
                        current_node = current_node.right

    def traverse(self):
        sorted_array = []

        def in_order(node):
            if node is not None:
                in_order(node.left)
                sorted_array.append(node.value)
                in_order(node.right)

        in_order(self.root)

        return sorted_array

    def median(self):
        sorted_array = self.traverse()

        # If the number of elements in the array is even, then the median is the average of the two middle elements.
        if len(sorted_array) % 2 == 0:
            median = (sorted_array[len(sorted_array) // 2] + sorted_array[len(sorted_array) // 2 - 1]) / 2
        else:
            # Otherwise, the median is the middle element. Uses floor to round down, and then index pos to reach middle.
            median = sorted_array[len(sorted_array) // 2]

        return median


# Define a node to be used in our binary structure.
class Node:

    # Hold the value the node was initiated with and instantiate None to the left AND right where future nodes may be.
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None