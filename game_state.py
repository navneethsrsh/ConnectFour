# Set of functions to check in different directions and identify if a player has won
# All functions take the same parameters:
#   mapping      - 2D list which emulates the printed board on screen
#   position     - Tuple with the column entered by the user and the generated row as (row, column)
#   player_index - 1 or 2 for player 1 or player 2 respectively
#   board_size   - Width of the board as entered by the user at the start of the game


# Look left_right
def look_left_right(mapping, position, player_index, board_size):
    count = 0
    for i in range(1, 4):
        if position[1] + i < board_size:  # Looking right
            if mapping[position[0]][position[1] + i] == player_index:
                count += 1
        if position[1] - i >= 0:  # Looking left
            if mapping[position[0]][position[1] - i] == player_index:
                count += 1
    print("Right: ", count)
    return 0 if count != 3 else count


# Look up_down
def look_up_down(mapping, position, player_index, board_size):
    count = 0
    for i in range(1, 4):
        if position[0] + i < board_size:  # Looking up
            if mapping[position[0] + i][position[1]] == player_index:
                count += 1
        if position[0] - i >= 0:  # Looking down
            if mapping[position[0] - i][position[1]] == player_index:
                count += 1
    print("left: ", count)
    return 0 if count != 3 else count


# Look diagonal bottom-left --> top-right
def look_left_diagonal(mapping, position, player_index, board_size):
    count = 0
    for i in range(1, 4):
        if position[0] - i >= 0 and position[1] + i < board_size:  # Looking diagonally up-right
            if mapping[position[0] - i][position[1] + i] == player_index:
                count += 1
        if position[0] + i < board_size and position[1] - i >= 0:  # Looking diagonally down-left
            if mapping[position[0] + i][position[1] - i] == player_index:
                count += 1
    return 0 if count != 3 else count


# Look diagonal bottom-right --> top-left
def look_right_diagonal(mapping, position, player_index, board_size):
    count = 0
    for i in range(1,4):
        if position[0] + i < board_size and position[1] + i < board_size:  # Looking diagonally down-right
            if mapping[position[0] + i][position[1] + i] == player_index:
                count += 1
        if position[0] - i >= 0 and position[1] - i >= 0:  # Looking diagonally up-left
            if mapping[position[0] - i][position[1] - i] == player_index:
                count += 1
    return 0 if count != 3 else count
