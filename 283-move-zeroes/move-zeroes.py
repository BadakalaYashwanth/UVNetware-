class Solution:
    def moveZeroes(self, nums: List[int]) -> None:
        # slow points to where the next non-zero value should go
        slow = 0

        # fast scans the entire array
        for fast in range(len(nums)):

            # If the current value is not zero, keep it
            if nums[fast] != 0:

                # Copy the non-zero value to the slow position
                nums[slow] = nums[fast]

                # Move slow to the next position
                slow += 1

        # After scanning the whole array, fill the remaining positions with 0
        while slow < len(nums):
            nums[slow] = 0
            slow += 1