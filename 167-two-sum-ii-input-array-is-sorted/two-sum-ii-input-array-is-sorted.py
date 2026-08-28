class Solution:
    def twoSum(self, numbers: List[int], target: int) -> List[int]:
        left = 0
        right = len(numbers) - 1

        while left < right:
            Addition = numbers[left] + numbers[right]
            if Addition < target:
                left += 1
            elif Addition > target:
                right -= 1
            else:
                return [left + 1, right + 1]