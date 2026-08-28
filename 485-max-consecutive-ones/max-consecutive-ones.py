class Solution:
    def findMaxConsecutiveOnes(self, nums: List[int]) -> int:
        
        # count keeps track of the current continuous sequence of 1s
        count = 0
        
        # maxi stores the maximum number of consecutive 1s found so far
        maxi = 0 
        
        # iterate through the array using index i
        for i in range(len(nums)):
            
            # if the current element is 1, we are inside a streak of 1s
            if nums[i] == 1:
                
                # extend the current streak
                count += 1
                
                # update the maximum streak if current is larger
                maxi = max(maxi, count)
            
            # if the current element is 0, the streak breaks
            else:
                # reset the current streak counter
                count = 0
        
        # return the longest streak of consecutive 1s found
        return maxi
