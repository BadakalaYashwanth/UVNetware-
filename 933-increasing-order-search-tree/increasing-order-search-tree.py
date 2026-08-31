# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class Solution:
    def increasingBST(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        
        # If the tree is empty, return None
        if root is None:
            return None
        
        # Store the values in inorder
        result = []

        def dfs(node):

            # Base Case
            # Stop when there is no node
            if node is None:
                return

            # Inorder: LEFT
            dfs(node.left)

            # Inorder: ROOT
            # Store the current node's value
            result.append(node.val)

            # Inorder: RIGHT
            dfs(node.right)

        # Start inorder traversal from the root
        dfs(root)

        # Create a dummy node to help build the new tree
        dummy = TreeNode(0)

        # Current points to the node where we will attach
        # the next value
        current = dummy

        # Create the new tree using the sorted values
        for value in result:

            # Create a new node
            current.right = TreeNode(value)

            # Move current to the newly created node
            current = current.right

        # The dummy node is not part of the answer
        # Return the actual first node
        return dummy.right