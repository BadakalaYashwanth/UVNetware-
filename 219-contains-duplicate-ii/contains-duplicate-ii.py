class Solution:
    def containsNearbyDuplicate(self, nums: List[int], k: int) -> bool:
        # Store each number with its latest index
        seen = {}

        for right in range(len(nums)):

            # If the number was seen before
            if nums[right] in seen:

                # Check the distance between the two indices
                if right - seen[nums[right]] <= k:
                    return True

            # Update the number's latest index
            seen[nums[right]] = right

        # No nearby duplicate was found
        return False