import termcolor
import connectFour as conn4

# Get board size from user
board_size = conn4.get_board_size()

# Print warning message regarding penalty for more than 3 incorrect move inputs
acceptable_values = [x for x in range(1,board_size+1)]
termcolor.cprint("\nATTENTION!!!", "yellow", attrs=["bold"])
print("While making a move be careful to enter only valid values!\n" +
      "Providing an incorrect value more than 3 times serves as a penalty and your turn ", end='')
termcolor.cprint("WILL BE SKIPPED!", "red", attrs=["bold"])
print("In this instance your board size is {0} and so the acceptable values are ONLY {1}\n"\
      .format(board_size, acceptable_values))

# Build mapping table (a 2D list) which maintains the position each player has played
mapping = conn4.build_mapping(board_size)

# Get the player names, set the current player as Player1 and corresponding player index to 1
player_names, player, player_index = conn4.get_player_names()

# Begin playing the game
conn4.play_game(mapping, player_names, player_index, player, board_size)