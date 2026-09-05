class Solution:
    def maxScore(self, cardPoints: List[int], k: int) -> int:

        # Total number of cards
        n = len(cardPoints)

        # Sum of points from all cards
        total = sum(cardPoints)

        # We take k cards, so n-k cards must remain
        # These remaining cards form one continuous window
        window_size = n - k

        # If we take every card, nothing remains
        if window_size == 0:
            return total

        # Create the first window of cards that we leave behind
        window_sum = sum(cardPoints[:window_size])

        # Store the smallest window sum found so far
        min_window = window_sum

        # Slide the fixed-size window through the array
        for right in range(window_size, n):

            # Find the index of the card leaving the window
            left = right - window_size

            # Remove the card that is leaving the window
            window_sum -= cardPoints[left]

            # Add the new card entering the window
            window_sum += cardPoints[right]

            # Keep the smallest window sum
            min_window = min(min_window, window_sum)

        # Maximum points =
        # total points - minimum points left behind
        return total - min_window