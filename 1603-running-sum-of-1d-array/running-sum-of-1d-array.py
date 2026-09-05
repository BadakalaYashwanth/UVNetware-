class Solution:
    def runningSum(self, nums: List[int]) -> List[int]:

        # Store all the running sums
        result = []

        # Keep track of the sum calculated so far
        current_sum = 0

        # Go through every element in the array
        for i in range(len(nums)):

            # Add the current number to the running total
            current_sum += nums[i]

            # Store the current running sum in the result list
            result.append(current_sum)

        # Return all the running sums
        return result