class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        # slow points to where the next unique value should go
        slow = 1

        # fast checks every element
        for fast in range(1, len(nums)):

            # Check if current value is different from the last unique value
            if nums[fast] != nums[slow - 1]:

                # Put the new unique value at slow
                nums[slow] = nums[fast]

                # Move slow to the next position
                slow += 1

        # slow represents the number of unique elements
        return slow