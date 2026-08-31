# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class Solution:
    def postorderTraversal(self, root: Optional[TreeNode]) -> List[int]:

        # Base Case:
        # If the current node is empty, stop the recursion
        # and return an empty list
        if root is None:
            return []
        
        # Create an empty list to store the postorder values
        result = []

        # First, recursively visit the LEFT subtree
        # Postorder follows: LEFT → RIGHT → ROOT
        result += self.postorderTraversal(root.left)

        # Second, recursively visit the RIGHT subtree
        result += self.postorderTraversal(root.right)

        # Third, process the ROOT node
        # Add the current node's value after both children are processed
        result.append(root.val)

        # Return the complete postorder traversal
        return result