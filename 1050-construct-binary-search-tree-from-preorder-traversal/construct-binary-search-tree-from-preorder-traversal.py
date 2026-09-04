# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class Solution:
    def bstFromPreorder(self, preorder: List[int]) -> Optional[TreeNode]:

        # The first element in preorder is always the root
        # because preorder traversal follows:
        # Root → Left → Right
        root = TreeNode(preorder[0])

        # Process every value after the root
        # Example: [8, 5, 1, 7, 10, 12]
        #          ↑
        #        root
        # Remaining values: 5, 1, 7, 10, 12
        for value in preorder[1:]:

            # Start searching for the correct position
            # from the root for every new value
            current = root

            # Keep moving through the tree until
            # we find an empty position
            while True:

                # If the new value is smaller than
                # the current node's value,
                # it belongs somewhere in the LEFT subtree
                if value < current.val:

                    # Check whether the left position is empty
                    if current.left is None:

                        # Create a new node with the current value
                        # and attach it as the left child
                        current.left = TreeNode(value)

                        # The value has been inserted,
                        # so stop searching for its position
                        break

                    # The left position is already occupied
                    # so move current to the left child
                    # and continue comparing
                    current = current.left

                # If the value is greater than the current node,
                # it belongs somewhere in the RIGHT subtree
                else:

                    # Check whether the right position is empty
                    if current.right is None:

                        # Create a new node with the current value
                        # and attach it as the right child
                        current.right = TreeNode(value)

                        # The value has been inserted,
                        # so stop searching for its position
                        break

                    # The right position is already occupied
                    # so move current to the right child
                    # and continue comparing
                    current = current.right

        # Return the root node.
        # Since all nodes are connected to root,
        # returning root returns the complete BST.
        return root