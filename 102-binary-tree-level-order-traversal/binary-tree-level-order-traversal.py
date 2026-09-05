from collections import deque

class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:

        # If the tree is empty, return an empty list.
        if root is None:
            return []

        # Create a queue and put the root node into it.
        queue = deque([root])

        # Store the final answer here.
        result = []

        # Continue while there are nodes waiting in the queue.
        while queue:

            # Store the nodes of the current level.
            level = []

            # Process only the nodes currently in the queue.
            # len(queue) = number of nodes in the current level.
            for _ in range(len(queue)):

                # Remove the first node from the queue.
                node = queue.popleft()

                # Add the current node's value to this level.
                level.append(node.val)

                # Add the left child to the queue for the next level.
                if node.left:
                    queue.append(node.left)

                # Add the right child to the queue for the next level.
                if node.right:
                    queue.append(node.right)

            # Current level is complete, so add it to the result.
            result.append(level)

        # Return all levels.
        return result