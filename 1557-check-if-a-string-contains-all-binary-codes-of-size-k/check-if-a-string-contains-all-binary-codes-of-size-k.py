class Solution:
    def hasAllCodes(self, s: str, k: int) -> bool:

        seen = set()
        window = s[:k]
        seen.add(window)

        for right in range(k, len(s)):
            window += s[right]
            window = window[1:]

            seen.add(window)

            if len(seen) == (2**k):
                return True
        return False 