class Solution:
    def numIdenticalPairs(self, nums: List[int]) -> int:

        count = 0

        # Choose the first index
        for i in range(len(nums)):

            # Compare it with every element after it
            # j starts at i + 1, so i is always less than j
            for j in range(i + 1, len(nums)):

                # Check if the two values are equal
                if nums[i] == nums[j]:
                    count += 1

        return count