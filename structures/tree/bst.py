class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None


def checkBST(root):
    def in_order_traversal(node, last_node_val):
        # Base case: if the node is None, return True
        if not node:
            return True

        # Check the left subtree
        if not in_order_traversal(node.left, last_node_val):
            return False

        # Check current node's value with the last node's value
        if last_node_val[0] is not None and node.data <= last_node_val[0]:
            return False

        # Update the last node's value to the current node's value
        last_node_val[0] = node.data

        # Check the right subtree
        return in_order_traversal(node.right, last_node_val)

    # Start the traversal with the initial last node value as None
    return in_order_traversal(root, [None])

# Example usage:
# Constructing the tree:
#       4
#      / \
#     2   6
#    / \ / \
#   1  3 5  7


root = Node(4)
root.left = Node(2)
root.right = Node(6)
root.left.left = Node(1)
root.left.right = Node(3)
root.right.left = Node(5)
root.right.right = Node(7)

# Check if the tree is a BST
print(checkBST(root))  # Output: True
