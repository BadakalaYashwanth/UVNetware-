# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution:
    def detectCycle(self, head: Optional[ListNode]) -> Optional[ListNode]:

        # If the linked list is empty, there is no cycle
        if head is None:
            return None

        # Both pointers start at the first node
        slow = head
        fast = head

        # Phase 1, check whether a cycle exists
        # slow moves 1 node, fast moves 2 nodes
        while fast is not None and fast.next is not None:

            # Move slow one node forward
            slow = slow.next

            # Move fast two nodes forward
            fast = fast.next.next

            # If both pointers meet, a cycle exists
            if slow == fast:
                break

        # If fast reaches the end, there is no cycle
        else:
            return None

        # Phase 2, move slow back to the first node
        slow = head

        # Move both pointers one node at a time
        # They will meet at the node where the cycle starts
        while slow != fast:
            slow = slow.next
            fast = fast.next

        # Return the node where the cycle begins
        return slow