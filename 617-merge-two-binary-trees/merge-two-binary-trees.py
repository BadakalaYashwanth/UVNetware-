# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class Solution:
    def mergeTrees(self, root1: Optional[TreeNode], root2: Optional[TreeNode]) -> Optional[TreeNode]:

        # Base Case:
        # If root1 is empty, there is no node from the first tree
        # to merge with root2.
        # So, return root2 directly.
        if root1 is None:
            return root2
        
        # Base Case:
        # If root2 is empty, there is no node from the second tree
        # to merge with root1.
        # So, return root1 directly.
        if root2 is None:
            return root1

        # Create a new node for the merged tree.
        # Add the values of the current nodes from both trees.
        #
        # Example:
        # root1.val = 1
        # root2.val = 2
        # 1 + 2 = 3
        #
        # So, the new merged node will contain 3.
        merged = TreeNode(root1.val + root2.val)

        # Recursive Call for the LEFT side:
        # Take the left child of root1 and the left child of root2.
        # Merge these two left subtrees using the same function.
        #
        # The returned merged node/subtree is attached
        # as the LEFT child of the current merged node.
        merged.left = self.mergeTrees(root1.left, root2.left)

        # Recursive Call for the RIGHT side:
        # Take the right child of root1 and the right child of root2.
        # Merge these two right subtrees using the same function.
        #
        # The returned merged node/subtree is attached
        # as the RIGHT child of the current merged node.
        merged.right = self.mergeTrees(root1.right, root2.right)

        # Return the current merged node.
        # At this point, the node contains the sum of the current values
        # and its LEFT and RIGHT subtrees have also been merged.
        return merged