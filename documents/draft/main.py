

board = [[4,5,6],
         [7,8,1],
         [2,3,"empty_box"]]

winning_board = [[1,2,3],
                 [4,5,6],
                 [7,8,"empty_box"]]
current_pos = [2, 2] # holds the row and column index's of the empty box in the board list.
moves = []

def swap(board, current_pos, direction):
    if direction == "down":
        if (current_pos[0]+1) >= 0 & (current_pos[0]+1)<= 3:
            initial_pos = board[current_pos[0]][current_pos[1]] # holds the initial position number into a temporary variable
            board[current_pos[0]][current_pos[1]] = board[current_pos[0]+1][current_pos[1]] # assign number in target position to initial position
            board[current_pos[0]+1][current_pos[1]] = initial_pos # assign number in initial position to target position
            current_pos = [current_pos[0]+1,current_pos[1]] # update the current position to keep track of the empty box position
            moves.append("down")
            return board, current_pos
        return "Error: The current number is either in the bottom row and cannot swap, or the target position is not an empty box."
    if direction == "up":
        if (current_pos[0]-1)>=0 & (current_pos[0]-1)<=3:
            initial_pos = board[current_pos[0]][current_pos[1]] # holds the initial position number into a temporary variable
            board[current_pos[0]][current_pos[1]] = board[current_pos[0]-1][current_pos[1]] # assign number in target position to initial position
            board[current_pos[0]-1][current_pos[1]] = initial_pos # assign number in initial position to target position
            moves.append("up")
            current_pos = [current_pos[0]-1,current_pos[1]] # update the current position to keep track of the empty box position
            return board, current_pos
        return "Error: The current number is either at the top row and cannot swap up, or the target position is not an empty box."
    if direction == "right":
        if (current_pos[1]+1)>=0 & (current_pos[1]+1)<=3:
            initial_pos = board[current_pos[0]][current_pos[1]] # holds the initial position number into a temporary variable
            board[current_pos[0]][current_pos[1]] = board[current_pos[0]][current_pos[1]+1] # assign number in target position to initial position
            board[current_pos[0]][current_pos[1]+1] = initial_pos # assign number in initial position to target position
            current_pos = [current_pos[0],current_pos[1]+1] # update the current position to keep track of the empty box position
            moves.append("right")
            return board, current_pos
        return "Error: The current number is either in the right most position and cannot swap, or the target position is not an empty box."
    if direction == "left":
        if (current_pos[1]-1)>=0 & (current_pos[1]-1)<=3:
            initial_pos = board[current_pos[0]][current_pos[1]] # holds the initial position number into a temporary variable
            board[current_pos[0]][current_pos[1]] = board[current_pos[0]][current_pos[1]-1] # assign number in target position to initial position
            board[current_pos[0]][current_pos[1]-1] = initial_pos # assign number in initial position to target position
            current_pos = [current_pos[0],current_pos[1]-1] # update the current position to keep track of the empty box position
            moves.append("left")
            return board, current_pos
        return "Error: The current number is either in the left most position and cannot swap, or the target position is not an empty box"
    # we may want to move this to another function that checks all of the propositions, but I put it here for now.
    if board == winning_board:
        print("The slide puzzle has now been solved") 
    return "Error: the direction entered is not an acceptible move."

board, current_pos = swap(board, current_pos, "up")
print("board:", board)
print("moves:", moves)
