class Solution:
    def findMaxAverage(self, nums: List[int], k: int) -> float:
        n = len(nums)
        if k > n:
            return -1 

        left = 0
        window_slide= 0

        window_slide = sum(nums[:k])
        max_value = window_slide/k 

        for right in range(k, n):
            window_slide += nums[right]
            window_slide -= nums[right - k]

            max_value = max(max_value, window_slide/k)
        
        return max_value
            