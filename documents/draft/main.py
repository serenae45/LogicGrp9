
board = [[1,2,3],[4,5,6],[7,8,"empty_box"]]
direction = "right"

def swap(board, row, column, direction):
    if direction == "down":
        if (row+1) >= 0 & (row+1)<= 3:
            initial_pos = board[row][column] # holds the initial position number into a temporary variable
            board[row][column] = board[row+1][column] # assign number in target position to initial position
            board[row+1][column] = initial_pos # assign number in initial position to target position
            return board
        return "Error: The current number is in the top row, and there is no row above to swap."
    if direction == "up":
        if (row-1)>=0 & (row-1)<=3:
            initial_pos = board[row][column] # holds the initial position number into a temporary variable
            board[row][column] = board[row+1][column] # assign number in target position to initial position
            board[row+1][column] = initial_pos # assign number in initial position to target position
            return board
        return "Error: The current number is in the bottom row, and there is no row below to swap."
    if direction == "right":
        if (column+1)>=0 & (column+1)<=3:
            initial_pos = board[row][column] # holds the initial position number into a temporary variable
            board[row][column] = board[row][column+1] # assign number in target position to initial position
            board[row][column+1] = initial_pos # assign number in initial position to target position
            return board
        return "Error: The current number is in the most right column, and there is no column to the right to swap."
    if direction == "left":
        if (column-1)>=0 & (column-1)<=3:
            initial_pos = board[row][column] # holds the initial position number into a temporary variable
            board[row][column] = board[row][column-1] # assign number in target position to initial position
            board[row][column-1] = initial_pos # assign number in initial position to target position
            return board
        return "Error: The current number is in the most left column, and there is no column to the left to swap."
    return "Error: the direction entered is not an acceptible move."

print(swap(board, 1, 2, direction))