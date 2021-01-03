import os
import termcolor
from collections import namedtuple


class Player:
    """
    Class to handle player information

    Class Variables:
    ----------------
    index --> Number denoting the player e.g. 1 for Player 1
    color --> Unused (at this point)

    Attributes:
    -----------
    name --> name of the player
    """
    index = 0
    color = ''

    def __new__(cls):
        """
        Update index and create a new instance
        """
        cls.index += 1
        return object.__new__(cls)

    def __init__(self):
        """
        Retrieve the name of the player as user input
        """
        self.name = input(f"Player {self.index} Name: ")

    def __str__(self):
        """
        Only the name attribute is printed

        :return: Name of the player
        """
        return self.name


class Board(object):
    """
    Class to play Connect Four

    Class Variables:
    ----------------
    size --> Size of the game board. Valid values are 5-10
    attempts --> Chances the user has to input a valid board size
    is_player --> Definition of namedtuple for player information
    is_playing --> Definition of namedtuple for current/next player

    Attributes:
    -----------
    mapping --> 2-dimensional list recording the current state of
                the game board >> type = list
    p1 --> Player 1 info >> type = is_player
    p2 --> Player 2 info >> type = is_player
    plyr --> Current/next Player >> type = is_playing
    replay --> List maintaining history of mapping matrix for each move

    The class and it's functions are defined in such way that simply
    calling the class will start and run the game.
    """
    # Class Variables -----------------------------------

    size = 0
    attempts = 4
    is_player = namedtuple("is_player", ["name", "index"])
    is_playing = namedtuple("is_playing", ["now", "next"])

    # Built-in Methods -------------------------------------

    def __new__(cls):
        """
        Create a new instance of the class and build board

        This method is not required technically but exists conceptually.
        The concept being the board must exist in order for the game to
        be played. Keeping in line with that concept this method creates
        a new instance of this class and also accepts and validates the
        board size as user input by calling the classmethod - build_board
        """

        print("Building your board!")
        instance = object.__new__(cls)
        while instance.attempts:
            cls.build_board(instance)
        return instance

    def __init__(self):
        """
        Initiate gameplay

        1. Initialization of the mapping matrix
        2. Setting up Player 1 and 2
        3. Setting up current player
        4. Display initial empty board onto terminal screen
        5. Call self as a function to run gameplay

        Additional Info:
        ----------------
        The mapping matrix is a 2-dimensional list (a list within
        a list) which maintains the current state of the board
        displayed on screen

        """

        self.mapping = []
        for row in range(self.size):
            self.mapping.append([])
            for col in range(self.size):
                self.mapping[row].append(0)
        self.p1 = self.is_player(Player().name, Player.index)
        self.p2 = self.is_player(Player().name, Player.index)
        self.plyr = self.is_playing(self.p1, self.p2)
        self.replay = []
        self.replay.append(self.mapping)
        print(self)
        self()

    def __call__(self):
        """
        Calling self as function runs gameplay

            When an instance is called:
            1. Appropriate player (1 or 2) makes a move
            2. The mapping matrix is updated with the latest move
            3. Board is updated and printed to screen
            4. Check to see if the player has won - if, yes mention the winner and the game is over
            5. If not, toggle the player and repeat

        Additional Info:
        ----------------
            Any move made by a player is recognized as an
            intersection in the mapping matrix which is represented
            by the tuple (row, col). This tuple representation
            is used in the function- solution_map to validate
            if a player has won

        """

        while True:
            print(f"{self.plyr.now.name}, it's your move")
            _col = int(input("Place your coin by entering the column: ")) - 1
            _row = -1
            for i in reversed(range(self.size)):
                if self.mapping[i][_col] == 0:
                    _row = i
                    break
            self.mapping[_row][_col] = self.plyr.now.index
            print(self)
            state = self.solution_map(_row, _col)
            if state == 1:
                print(f'{self.plyr.now.name} has won the game!')
                break
            else:
                reversed(self)

    def __reversed__(self):
        """
        Used to toggle between player 1 and 2

        """

        _p1 = self.plyr.next
        _p2 = self.plyr.now
        self.plyr = self.plyr._replace(now=_p1, next=_p2)

    def __repr__(self):
        """
        Used to display the mapping matrix
        """

        text = ''
        for row in range(self.size):
            for col in range(self.size):
                text += str(self.mapping[row][col])
            text += '\n'
        return text

    def __str__(self):
        """
        Print the game-board in current state
        """

        color_table = {
            0: 'grey',
            1: 'red',
            2: 'yellow'
        }
        os.system('clear')
        text = ''
        for row in range(self.size):
            for col in range(self.size):
                text += termcolor.colored('\u2b24  ', color_table[self.mapping[row][col]])
            text += '\n'
        for row in range(self.size):
            text += str(row+1) + '  '
        text += '\n'
        return text

    def __enter__(self):
        """
        Context Manager Entry - Only used to push-back the board size
        as input by the user

        :return: Size of the board entered

        """

        return self.size

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Context Manager method used to handle ValueError exception
        when user inputs size of the board in classmethod - build_board()

        :param exc_type: The type of exception (at this point only ValueError)
        :param exc_val: The message related to the exception
        :param exc_tb: Traceback (unused)
        :return: boolean(True) if exception is handled correctly

        The user has three(3) attempts after the first incorrect input.
        Inputting an invalid value beyond the allowed attempts results in
        defaulting the board size to seven(7).

        """
        if exc_type is ValueError:
            self.attempts -= 1
            if self.attempts:
                print(exc_val, f'\nYou have {self.attempts} attempts left. '
                               f'After which board size will be defaulted to 7')
            else:
                self.size = 7
                print(f'Board size has been defaulted to {self.size}')
            return True

    # User-defined Methods -------------------------------

    def map_value(self, row: int, col: int) -> int:
        """
        Used to return the value in the mapping matrix if valid,
        else returns 0

        :param row: The row index of the mapping matrix where the current user
                    made the latest move
        :param col: The column index of the mapping matrix where the current user
                    made the latest move
        :return: Value: 1 if the current player has won else Value: 0

        """

        return self.mapping[row][col] if [0 <= x <= (self.size - 1) for x in [row, col]].count(True) == 2 else 0

    def solution_map(self, row: int, col: int) -> bool:
        """
        Identifies if a player has won

        :param row: The row index of the mapping matrix where the current user
                    made the latest move
        :param col: The column index of the mapping matrix where the current user
                    made the latest move
        :return: Value: 1 if the current player has won else Value: 0

        Dispatch Table --> path_table:
        ------------------------------
        The function uses a dispatch table to generate dictionaries which
        hold the possible paths to look for a win situation

        Keys:
            1 --> Looking left - right
            2 --> Looking up - down
            3 --> Looking bottom-left to top-right
            4 --> Looking bottom-right to top-left

        For each key in path_table the corresponding value is a dictionary
        which looks like {(r1, c1): 0, (r2, c2): 1 ... (rn, cn): 0}
        where r1, r2 ... rn are all valid row indexes for the mapping
        matrix and c1, c2...cn are all valid column indexes for the mapping
        matrix.
        The value for each pair (rn, cn) can either be 0 or 1 or 2 depending
        on which player has occupied that intersection in the mapping matrix.

        The return Statement:
        ---------------------
        The return statement is a one-liner which does -
            1. Builds a list of all the solution path dictionaries obtained
               from the dispatch table path_table e.g. [{(4,3): 1, (3,2): 0}]
            2. Builds a list of the values of each key for each dictionary
               obtained in (1.) e.g. [1,0]
            3. Converts it into a list of string values rather than int.
               e.g. '1,0'
               Note:: While converting to string all ascii-whitespaces are
                      removed
            4. Checks if the "win-string" is a substring of the one obtained
               in (3.) e.g. '1,0' in '1,0' --> True
               At this point a list of True/False values is available indicating
               if at least one path is a win solution.
            5. The sum of the True/False list is checked against 0 to create the
               final return value.
        """

        path_table = {
            1: {(row, c): self.map_value(row, c) for c in range(max(0, col - 3), min(self.size, col + 4))},
            2: {(r, col): self.map_value(r, col) for r in range(max(0, row - 3), min(self.size, row + 4))},
            3: {**{(r, c): self.map_value(r, c) for (r, c) in [(row + i, col - i)
                                                               for i in range(min(self.size - row, col))]},
                **{(r, c): self.map_value(r, c) for (r, c) in [(row - i, col + i)
                                                               for i in range(min(row, self.size - col))]}},
            4: {**{(r, c): self.map_value(r, c) for (r, c) in [(row - i, col - i)
                                                               for i in range(min(row, col) + 1)]},
                **{(r, c): self.map_value(r, c) for (r, c) in [(row + i, col + i)
                                                               for i in range(min(self.size - row, self.size - col))]}}
        }
        return sum(list(map(lambda z: ((str(self.plyr.now.index) + ',')*4)[:-1] in z,
                            list(map(lambda s: str(s).replace(' ', ''),
                                     list(map(lambda x: [y for y in x.values()],
                                              [val for val in path_table.values()]))))))) >= 1

    def playback(self):
        """
        IN PROGRESS
        :return: None
        """
        pass

    # Class Method --------------------------------

    @classmethod
    def build_board(cls, self) -> int:
        """
        Used to accept user input for board size and validate
        the input

        :param self: Instance of this class
        :return: Value: 1 if validation is passed
        """
        cls.size = int(input("Enter the size of the board [5...10]: "))
        with self as size:
            if not 5 <= size <= 10:
                raise ValueError(f"Oops! The value {size} is out of range!!")
            else:
                self.attempts = 0
        return 1
