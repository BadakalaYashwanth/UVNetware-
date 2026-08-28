class Solution:
    def captureForts(self, forts: List[int]) -> int:
        left = 0
        max_count = 0

        for right in range(len(forts)):

            # If we find 0, it is an enemy fort.
            # Keep expanding the window.
            if forts[right] == 0:
                continue

            # We reached 1 or -1.
            # Check if the two ends are opposite:
            # 1 ... -1  OR  -1 ... 1
            if (forts[left] == 1 and forts[right] == -1) or \
               (forts[left] == -1 and forts[right] == 1):

                # Count the 0s between left and right.
                current_count = right - left - 1

                # Store the biggest group of 0s found so far.
                max_count = max(max_count, current_count)

            # Current 1 or -1 becomes the new left boundary.
            left = right

        # Return the maximum enemy forts that can be captured.
        return max_count