"""
# Definition for a Node.
class Node:
    def __init__(self, val: Optional[int] = None, children: Optional[List['Node']] = None):
        self.val = val
        self.children = children
"""

class Solution:
    def postorder(self, root: 'Node') -> List[int]:
        
        # Base Case
        # If the tree is empty, return an empty list
        if root is None:
            return []
        
        # Store the postorder traversal
        result = []

        def dfs(node):

            # Base Case
            # If there is no current node, stop
            if node is None:
                return
            
            # First, visit all children
            for child in node.children:
                dfs(child)

            # After all children are processed,
            # process the current node
            result.append(node.val)
        
        # Start DFS from the root
        dfs(root)
        
        # Return the complete postorder traversal
        return result