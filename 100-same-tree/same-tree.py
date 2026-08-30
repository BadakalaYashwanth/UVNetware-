# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class Solution:
    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        
        # Base Case
        # If both nodes [p and q] are empty, they are the same,
        # so return True.
        if p is None and q is None:
            return True
        
        # Base Case
        # If only one node is empty and the other node exists,
        # the structure of the trees is different, so return False.
        if p is None or q is None:
            return False
        
        # Check the values of the current nodes.
        # If p.val and q.val are different, the trees are not the same,
        # so return False.
        if p.val != q.val:
            return False
        
        # Recursive Call
        # Compare the LEFT child of p with the LEFT child of q.
        # If they are the same, this comparison returns True.
        #
        # Compare the RIGHT child of p with the RIGHT child of q.
        # If they are the same, this comparison returns True.
        #
        # The "and" means BOTH the left and right comparisons
        # must return True for the complete trees to be the same.
        return self.isSameTree(p.left, q.left) and self.isSameTree(p.right, q.right)