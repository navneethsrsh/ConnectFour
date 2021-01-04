import os
import time
import copy
import termcolor
from collections import namedtuple
# ToDO: Fix bug for directional lookup not searching till the end
# ToDo: Logging functionality


class Player:
    """
    Class to handle player information

    Class Variables:
    ----------------
    index --> Number denoting the player e.g. 1 for Player 1

    Attributes:
    -----------
    name --> name of the player
    """
    index = 0
    attempts = 4

    def __new__(cls):
        """
        Update index and create a new player
        """
        cls.index += 1
        return object.__new__(cls)

    def __init__(self):
        """
        Retrieve the name of the player as user input
        """
        while self.attempts:
            with self:
                self.name = input(f"Player {self.index} Name: ")
                self.attempts = self.raise_exceptions(self.name)

    def __str__(self):
        """
        Only the name attribute is printed

        :return: Name of the player
        """
        return self.name

    def __enter__(self):
        """
        Context manager entry

        :return: Current instance
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Context manager exit

        :param exc_type: Type of exception raised
        :param exc_val: The message of the exception
        :param exc_tb: Traceback
        :return: boolean(True) when exception is handled

        Additional Info:
        ----------------
        User has four(4) additional attempts after the first
        incorrect attempt to enter a valid name. Failing which
        the user name will be defaulted to:
            Player1 for player 1
            Player2 for player 2
        """

        if exc_type is ValueError:
            self.attempts -= 1
            if self.attempts:
                error = termcolor.colored(exc_val, 'red', 'on_yellow', attrs=['bold'])
                print(error, f'\nYou have {self.attempts} attempts left. '
                             f'After which board size will be defaulted to \"Player{self.index}\"')
            else:
                termcolor.cprint('\n\nToo many incorrect inputs', 'red', attrs=['bold'])
                time.sleep(1)
                self.name = f'Player{self.index}'
                print(f'Name has been defaulted to \"Player{self.index}\"')
            return True

    @staticmethod
    def raise_exceptions(name: str) -> int:
        if name == '':
            raise ValueError('Name cannot be blank')
        elif len(name) < 3:
            raise ValueError('Name is too short. Minimum length is three(3)')
        else:
            return 0


class Board:
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

    size = 0
    attempts = 4
    is_player = namedtuple("is_player", ["name", "index", "color"])
    is_playing = namedtuple("is_playing", ["now", "next"])

    def __new__(cls):
        """
        Create a new board and it's corresponding mapping matrix

        This method is technically unnecessary but, exists conceptually.
        The concept being the board must exist in order for the game to
        be played. Keeping in line with that concept this method
            1. Creates a new instance of this class
            2. Accepts and validates the board size as user input by calling
               the class-method - build_board
            3. Initializes and builds the mapping matrix
            4. Displays the empty board on screen

        Additional Info:
        ----------------
        The mapping matrix is a 2-dimensional list (a list within
        a list) which maintains the current state of the board
        displayed on screen
        The p1 and p2 attributes are dummy values here. This is
        needed to print the initial board
        """

        print("Building your board!")
        self = object.__new__(cls)
        while self.attempts:
            cls.build_board(self)
        self.mapping = []
        for row in range(self.size):
            self.mapping.append([])
            for col in range(self.size):
                self.mapping[row].append(0)
        print("Okay")
        print(self.mapping)
        cls.p1 = cls.is_player('name', 1, 'grey')  # Dummy player 1 for initial printing of board
        cls.p2 = cls.is_player('name', 2, 'grey')  # Dummy player 2 for initial printing of board

        print(self)
        return self

    def __init__(self):
        """
        Initiate gameplay

        1. Setting up Player 1 and 2
            1.1. Get name as user input
            1.2. Generate index for player (done in class Player)
            1.3. Get choice of color as user input
        2. Setting up current player
        3. Initialize and update replay[] list with blank mapping
           matrix
        4. Re-print the blank board -- to clear the player info
           from screen
        5. Call self as a function to run gameplay

        Additional Info:
        ----------------
        Player 2 will have one less option in comparison to Player 1
        when it comes to choosing colors. The set of colors available
        in color_set are limited to those provided by the module
        termcolor.
        The color 'grey' is the color used for an unoccupied position
        on the board and is therefore not a choice available to
        either player.
        """

        color_set = {'red', 'yellow', 'blue', 'magenta', 'green', 'cyan', 'white'}
        self.p1 = self.is_player(Player().name, Player.index, self.set_color(color_set))
        color_set -= {self.p1.color}
        self.p2 = self.is_player(Player().name, Player.index, self.set_color(color_set))
        self.plyr = self.is_playing(self.p1, self.p2)
        self.replay = []
        self.replay.append(copy.deepcopy(self.mapping))
        print(self)
        self()

    def __call__(self):
        """
        Calling self as a function runs gameplay

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
            self.replay.append(copy.deepcopy(self.mapping))
            print(self)
            state = self.solution_map(_row, _col)
            if state == 1:
                print(f'{self.plyr.now.name} has won the game!')
                self.playback(input("Would you like to watch a replay? (y/n): "))
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
            1: self.p1.color,
            2: self.p2.color
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
        Context Manager Entry

        :return: Current instance

        """

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Context Manager method used to handle ValueError exception
        when user inputs size of the board in class-method - build_board()

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
                error = termcolor.colored(exc_val, 'red', 'on_yellow', attrs=['bold'])
                print(error, f'\nYou have {self.attempts} attempts left. '
                             f'After which board size will be defaulted to 7')
            else:
                self.size = 7
                os.system('clear')
                termcolor.cprint('\n\nToo many incorrect inputs', 'red', attrs=['bold'])
                time.sleep(1)
                print(f'Board size has been defaulted to {self.size}')
                color = ['red', 'yellow', 'green']
                for u in range(3):
                    shape = termcolor.colored(' '*(u + 1) + '\u2b24', color[u])
                    print('Loading game ' + shape, end='\r')
                    time.sleep(1)
            return True

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

    def playback(self, watch: str):
        """
        Function to run a replay of the game

        :param watch: Value: y or Value: n representing if the players
                      want to watch a replay

        Additional Info:
        ----------------
        The replay[] list maintains a deepcopy of the mapping matrix for every
        move made on the board. This method simply loops over each matrix and
        prints the board.
        """

        if watch == 'y':
            for b_map in self.replay:
                self.mapping = b_map
                print(self)
                time.sleep(1)

    @classmethod
    def build_board(cls, self) -> int:
        """
        Used to accept user input for board size and validate
        the input

        :param self: Instance of this class
        :return: Value: 1 if validation is passed
        """
        with self:
            self.size = int(input("Enter the size of the board [5...10]: "))
            if not 5 <= self.size <= 10:
                raise ValueError(f"Oops! The value {self.size} is out of range!!")
            else:
                self.attempts = 0
        return 1

    @staticmethod
    def set_color(colors: set) -> str:
        print('Colors:', end='  ')
        for color in colors:
            termcolor.cprint('\u2b24  ', color, end='')
        print()
        print('Index:', end='   ')
        for index in range(len(colors)):
            print(str(index + 1) + '  ', end='')
        print()
        select = int(input('Choose your color [Enter the index of color]: ')) - 1
        return list(colors)[select]