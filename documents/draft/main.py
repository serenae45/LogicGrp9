
from operator import index
from sre_compile import isstring


board = [[1,2,3],[4,5,6],[7,8,"empty_box"]]
winning_board = board = [[1,2,3],[4,5,6],[7,8,"empty_box"]]
direction = "down"
current_position = index("empty_box")

def swap(board, row, column, direction):
    if direction == "down":
        if (row+1) >= 0 & (row+1)<= 3 & isstring(board[row][column]):
            initial_pos = board[row][column] # holds the initial position number into a temporary variable
            board[row][column] = board[row+1][column] # assign number in target position to initial position
            board[row+1][column] = initial_pos # assign number in initial position to target position
            return board
        return "Error: The current number is either in the bottom row and cannot swap, or the target position is not an empty box."
    if direction == "up":
        if (row-1)>=0 & (row-1)<=3 & isstring(board[row][column]):
            initial_pos = board[row][column] # holds the initial position number into a temporary variable
            board[row][column] = board[row+1][column] # assign number in target position to initial position
            board[row+1][column] = initial_pos # assign number in initial position to target position
            return board
        return "Error: The current number is either at the top row and cannot swap up, or the target position is not an empty box."
    if direction == "right":
        if (column+1)>=0 & (column+1)<=3 & isstring(board[row][column+1]):
            initial_pos = board[row][column] # holds the initial position number into a temporary variable
            board[row][column] = board[row][column+1] # assign number in target position to initial position
            board[row][column+1] = initial_pos # assign number in initial position to target position
            return board
        return "Error: The current number is either in the right most position and cannot swap, or the target position is not an empty box."
    if direction == "left":
        if (column-1)>=0 & (column-1)<=3 & isstring(board[row][column-1]):
            initial_pos = board[row][column] # holds the initial position number into a temporary variable
            board[row][column] = board[row][column-1] # assign number in target position to initial position
            board[row][column-1] = initial_pos # assign number in initial position to target position
            return board
        return "Error: The current number is either in the left most position and cannot swap, or the target position is not an empty box"
    return "Error: the direction entered is not an acceptible move."

print(swap(board, 1, 2, direction))