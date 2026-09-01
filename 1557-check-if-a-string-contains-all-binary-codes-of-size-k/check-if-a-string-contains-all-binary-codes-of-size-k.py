class Solution:
    def hasAllCodes(self, s: str, k: int) -> bool:

        # Store all unique substrings of length k
        seen = set()

        # Create the first window of size k
        window = s[:k]

        # Add the first window to the set
        seen.add(window)

        # Slide the window through the string
        for right in range(k, len(s)):

            # Add the new character entering the window
            window += s[right]

            # Remove the first character to keep window size k
            window = window[1:]

            # Store the current window if it is unique
            seen.add(window)

            # There are 2^k possible binary strings of length k
            # If we found all of them, return True
            if len(seen) == 2 ** k:
                return True

        # Not all possible binary codes were found
        return False