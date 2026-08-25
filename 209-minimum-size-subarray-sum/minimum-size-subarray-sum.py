class Solution:
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        left = 0
        window_sum = 0
        result = float('inf')

        for right in range(len(nums)):
            window_sum += nums[right]

            while window_sum >= target:
                result = min(result, right - left + 1)
                window_sum -= nums[left]
                left += 1

        if result == float('inf'):
            return 0

        return result