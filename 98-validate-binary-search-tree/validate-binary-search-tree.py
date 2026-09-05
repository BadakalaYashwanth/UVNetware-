class Solution:
    def isValidBST(self, root: Optional[TreeNode]) -> bool:

        # 'prev' stores the value of the previous node
        # that we visited during inorder traversal.
        #
        # At the beginning, we have not visited any node,
        # so there is no previous value.
        prev = None

        def inorder(node):

            # 'nonlocal' allows this recursive function
            # to change the 'prev' variable created outside it.
            nonlocal prev

            # If there is no node, we reached the end
            # of this branch.
            #
            # Nothing is wrong here, so return True.
            if node is None:
                return True

            # INORDER = Left → Root → Right
            #
            # First, completely visit the left subtree.
            #
            # If the left subtree is invalid,
            # immediately return False.
            if not inorder(node.left):
                return False

            # Now we are visiting the CURRENT node.
            #
            # 'node.val' means:
            # "Give me the value stored inside this node."
            #
            # Example:
            # node = TreeNode(5)
            # node.val = 5
            #
            # We compare the current value with the
            # previous value visited in inorder.
            #
            # A valid BST must produce:
            #
            # 1 → 2 → 3 → 4 → 5
            #
            # The values must ALWAYS increase.
            if prev is not None and node.val <= prev:
                return False

            # The current node is valid.
            #
            # Now save its value as 'prev'.
            #
            # This value will be compared with the
            # NEXT node that we visit.
            prev = node.val

            # Finally, visit the right subtree.
            #
            # Again, if the right subtree is invalid,
            # return False.
            return inorder(node.right)

        # Start the inorder traversal from the root.
        #
        # The recursive function will check:
        #
        # Left → Root → Right
        #
        # If every value is strictly increasing,
        # the tree is a valid BST.
        return inorder(root)