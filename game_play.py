import termcolor
import game_state as gs

# Functions related to game play steps
# All functions take either all or a subset of these parameters:
#   mapping       - 2D list which emulates the printed board on screen
#   player        - Name of the current player
#   player_index  - 1 or 2 for player 1 or player 2 respectively
#   player_names  - List with both the player names
#   board_size    - Width of the board as entered by the user at the start of the game
#   move_count    - Count of moves played up until this point


# Generate playing board with updated color coding for game progression
def print_board(mapping, board_size=7):
    text = "\u2B24"
    print("\n\n")
    for i in range(board_size):
        print(' ' * 5, end='')
        for j in range(board_size):
            if mapping[i][j] == 1:
                termcolor.cprint(text, "red", end='  ')
            elif mapping[i][j] == 2:
                termcolor.cprint(text, "yellow", end='  ')
            else:
                termcolor.cprint(text, "grey", end='  ')
        print()
    print(' '*5, end='')
    for i in range(board_size):
        print(i + 1, end='  ')
    print()


# Get the column where the user wants to drop their coin
def get_move(player, board_size):
    print("{}'s move: ".format(player))
    accepted_values = [x for x in range(board_size)]
    column = 0
    chances = 3
    while True:
        try:
            column = int(input())
        except ValueError:
            chances -= 1
            if chances >= 0:
                print("Invalid value entered! Try again.Acceptable values are {}".format(accepted_values))
                print("You have {} chances left".format(chances))
                continue
            else:
                column = -1
                break
        break
    return column


# Based on the column chosen by current player, the mapping table is updated and move count incremented
def make_move(mapping, player, board_size, move_count, player_index):
    column = get_move(player, board_size)
    if column < 0 or column > board_size:
        return column, mapping, move_count
    else:
        for i in reversed(range(0, board_size)):
            if mapping[i][column - 1] == 0:
                mapping[i][column - 1] = player_index
                break
        move_count += 1
    return column, mapping,  move_count


# Checks and updates (if needed) the state of the game --> "ON", "DRAW", "OVER"
def state_of_game(mapping, column, player_index, board_size, move_count):
    if move_count <= 6:  # Minimum number of total moves == 7 for a chance at winning
        return "ON"
    else:
        pos = (-1, -1)  # Tuple holding the (row, column) of current input
        for i in range(board_size):  # column = 3 | mapping_T[?][2] --> first occurrence of index
            if mapping[i][column-1] == player_index:
                pos = (i, column-1)
                break
        count = 0
        count += gs.look_left_right(mapping, pos, player_index, board_size) +\
                 gs.look_up_down(mapping, pos, player_index, board_size) + \
                 gs.look_left_diagonal(mapping, pos, player_index, board_size) + \
                 gs.look_right_diagonal(mapping, pos, player_index, board_size)
    return "DRAW" if move_count == board_size ** 2 and count == 0 else "OVER" if count >= 3 else "ON"


# Switch between player 1 and player 2
def toggle(player, player_names):
    return (player_names[1], 2) if player == player_names[0] else (player_names[0], 1)
