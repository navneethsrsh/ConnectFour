import os
import termcolor
import game_play

# Functions related to pre-game setup and playing the game
# All functions take either all or a subset of these parameters:
#   mapping       - 2D list which emulates the printed board on screen
#   player        - Name of the current player
#   player_index  - 1 or 2 for player 1 or player 2 respectively
#   player_names  - List with both the player names
#   board_size    - Width of the board as entered by the user at the start of the game
#   move_count    - Count of moves played up until this point


def get_board_size():
    attempts = 3
    board_size = 0
    while True:
        try:
            board_size = int(input("Enter the board size [5 - 10]: \n"))
            if board_size < 5 or board_size > 10:
                print("The input value is invalid! The allowed values are: {0}".format(str([5, 6, 7, 8, 9, 10])))
                continue
        except ValueError:
            attempts -= 1
            if attempts >= 0:
                print("The input value is invalid! The allowed values are: {0}".format(str([5, 6, 7, 8, 9, 10])))
                print("You have {} tries left. Failing which board size is defaulted to 7".format(attempts))
                continue
            else:
                print("Too many wrong entries. board size defaulted to 7!")
                board_size = 7
                break
        break
    return board_size


def build_mapping(board_size):
    mapping = []
    for i in range(board_size):
        mapping.append([])
        for j in range(board_size):
            mapping[i].append(0)
    return mapping


def get_player_names():
    player_names = []
    for i in range(2):
        player_names.append(input("Player {} - Enter your name: \n".format(i+1)).strip())
    player = player_names[0]
    player_index = 1
    return player_names, player, player_index


def play_game(mapping, player_names, player_index, player, board_size):
    move_count = 0
    game = game_play.state_of_game(mapping, 0, player_index, board_size, move_count)
    while game == "ON":
        os.system("clear")
        game_play.print_board(mapping, board_size)
        column, mapping, move_count = game_play.make_move(mapping, player, board_size, move_count, player_index)
        if 0 <= column < board_size:
            game = game_play.state_of_game(mapping, column, player_index, board_size, move_count)
            if game not in ["OVER", "DRAW"]:
                player, player_index = game_play.toggle(player, player_names)
        else:
            player, player_index = game_play.toggle(player, player_names)
    if game == "OVER":
        os.system("clear")
        game_play.print_board(mapping, board_size)
        termcolor.cprint("Congrats {}!!!".format(player), "blue", end=" ")
        termcolor.cprint(" You've won the game!!", "green")
    else:
        os.system("clear")
        game_play.print_board(mapping, board_size)
        termcolor.cprint("It's a tie!", "magenta")
