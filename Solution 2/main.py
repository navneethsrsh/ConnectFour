import board
import sys

if len(sys.argv) > 1 and (sys.argv[1] == '-h' or sys.argv[1] == '--help'):
    help(board.Board)
else:
    board.Board()
