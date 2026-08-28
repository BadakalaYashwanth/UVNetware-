class Solution:
    def captureForts(self, forts: List[int]) -> int:
        left = 0
        max_count = 0

        for right in range(len(forts)):

            if forts[right] == 0:
                continue

            if (forts[left] == 1 and forts[right] == -1) or \
               (forts[left] == -1 and forts[right] == 1):

                max_count = max(max_count, right - left - 1)

            left = right

        return max_count