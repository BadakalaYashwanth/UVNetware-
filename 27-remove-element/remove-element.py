class Solution:
    def removeElement(self, nums: List[int], val: int) -> int:

        # slow points to the position where the next valid element should be placed
        slow = 0

        # fast scans every element in the array
        for fast in range(len(nums)):

            # Keep the element if it is not equal to val
            if nums[fast] != val:

                # Copy the valid element to the slow position
                nums[slow] = nums[fast]

                # Move slow to the next position
                slow += 1

        # Return the number of valid elements
        return slow