# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class Solution:
    def inorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        
        # Base Case:
        # If the current node is empty, return an empty list
        if root is None:
            return []
        
        # Create an empty list to store the inorder traversal
        result = []

        # First, recursively visit the LEFT subtree
        # Inorder follows: LEFT → ROOT → RIGHT
        result += self.inorderTraversal(root.left)

        # Second, process the ROOT node
        # Add the current node's value to the result
        result.append(root.val)

        # Third, recursively visit the RIGHT subtree
        result += self.inorderTraversal(root.right)

        # Return the complete inorder traversal
        return result