class Solution:
    def numOfSubarrays(self, arr: List[int], k: int, threshold: int) -> int:
        count = 0
        n = len(arr)

        if k > n:
            return 0

        window_sum = sum(arr[:k])
        avg = window_sum / k

        if avg >= threshold:
            count += 1

        for i in range(k, n):
            window_sum += arr[i]
            window_sum -= arr[i - k]
            avg = window_sum / k

            if avg >= threshold:
                count += 1

        return count