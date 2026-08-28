class Solution:
    def sortedSquares(self, nums: List[int]) -> List[int]:
        left = 0 
        right = len(nums) - 1

        #Create a Empty List that are filled with zeros 
        result = [0] * len(nums)

        #To Fill the position from left to right
        position = len(nums) - 1

        while left <= right:

            left_squ = nums[left] ** 2
            right_squ = nums[right] ** 2

            if left_squ > right_squ:
                result[position] = left_squ 
                left += 1
            else:
                result[position] = right_squ
                right -= 1
            
            position -= 1
        
        return result