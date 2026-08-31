# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class Solution:
    def getMinimumDifference(self, root: Optional[TreeNode]) -> int:

        # Store the previous value visited during inorder traversal
        self.previous = None

        # Start with a very large minimum difference
        self.minimum = float('inf')

        def dfs(node):

            # Base Case
            if node is None:
                return

            # Inorder: LEFT
            dfs(node.left)

            # ROOT
            # Compare current value with the previous value
            if self.previous is not None:
                difference = node.val - self.previous

                # Update minimum difference if this is smaller
                self.minimum = min(self.minimum, difference)

            # Current node becomes the previous node
            self.previous = node.val

            # Inorder: RIGHT
            dfs(node.right)

        # Start DFS from the root
        dfs(root)

        # Return the smallest difference found
        return self.minimum