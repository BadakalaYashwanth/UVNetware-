class Solution:
    def maximumSubarraySum(self, nums: List[int], k: int) -> int:
        n = len(nums)

        if k > n:
            return 0

        window_sum = sum(nums[:k])
        max_value = 0

        # Store the frequency of elements in the first window
        frequency = {}

        for i in range(k):
            frequency[nums[i]] = frequency.get(nums[i], 0) + 1

        # If all elements are distinct, first window is valid
        if len(frequency) == k:
            max_value = window_sum

        # Slide the window
        for i in range(k, n):

            # Add new element
            window_sum += nums[i]
            frequency[nums[i]] = frequency.get(nums[i], 0) + 1

            # Remove old element
            window_sum -= nums[i - k]

            frequency[nums[i - k]] -= 1

            # Remove from dictionary if its frequency becomes 0
            if frequency[nums[i - k]] == 0:
                del frequency[nums[i - k]]

            # Update maximum only when all k elements are distinct
            if len(frequency) == k:
                max_value = max(max_value, window_sum)

        return max_value