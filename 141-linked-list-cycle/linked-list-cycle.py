# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution:
    def hasCycle(self, head: Optional[ListNode]) -> bool:

        # left is the slow pointer, it moves one step at a time
        left = head

        # right is the fast pointer, it moves two steps at a time
        right = head

        # Continue while the fast pointer can safely move two steps
        while right is not None and right.next is not None:

            # Move slow pointer one node forward
            left = left.next

            # Move fast pointer two nodes forward
            right = right.next.next

            # If both pointers meet, a cycle exists
            if left == right:
                return True

        # Fast pointer reached the end, so there is no cycle
        return False