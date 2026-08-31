class Solution:
    def preorderTraversal(self, root: Optional[TreeNode]) -> List[int]:

        # Base Case
        # If there is no node, return an empty list
        if root is None:
            return []

        # Process ROOT first
        result = [root.val]

        # Recursively get the LEFT subtree
        result += self.preorderTraversal(root.left)

        # Recursively get the RIGHT subtree
        result += self.preorderTraversal(root.right)

        # Return ROOT + LEFT + RIGHT
        return result