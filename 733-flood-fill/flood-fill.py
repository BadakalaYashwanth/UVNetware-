class Solution:
    def floodFill(self, image: List[List[int]], sr: int, sc: int, color: int) -> List[List[int]]:
        
        # Store the original color of the starting pixel
        Original_Color = image[sr][sc]

        # If the original color is already the new color,
        # there is nothing to change
        if Original_Color == color:
            return image 
        
        # DFS function to visit connected pixels
        def dfs(row, column):

            # Stop if:
            # 1. row goes outside the image
            # 2. column goes outside the image
            # 3. current pixel does not have the original color
            if row < 0 or row >= len(image) or column < 0 or column >= len(image[0]) or image[row][column] != Original_Color:
                return 
            
            # Change the current pixel to the new color
            image[row][column] = color

            # Move DOWN
            dfs(row + 1, column)

            # Move UP
            dfs(row - 1, column)

            # Move RIGHT
            dfs(row, column + 1)

            # Move LEFT
            dfs(row, column - 1)
        
        # Start DFS from the given starting position
        dfs(sr, sc)

        # Return the modified image
        return image