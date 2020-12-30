from collections import ChainMap, deque, namedtuple


class Player:
    index = 'p0'
    number = 0

    def __new__(cls):
        cls.index = cls.increment_index()
        cls.number += 1
        return object.__new__(cls)

    def __init__(self):
        self.name = input(f"Player {self.number} Name: ")

    def __str__(self):
        return self.name

    @classmethod
    def increment_index(cls):
        return 'p' + str(int(cls.index[1])+1)


class SolutionTree:
    pass


class Board(object):
    size = 0
    attempts = 4
    is_player = namedtuple("is_player", ["name", "index"])
    p1 = is_player(Player().name, Player.index)  # name of Player 1 and 'p1''
    p2 = is_player(Player().name, Player.index)  # name of Player 2 and 'p2'
    # Solution Tree init and build

    def __new__(cls):
        print("Building your board!")
        cls.build_board()
        return object.__new__(cls)

    def __init__(self):
        self.mapping = []
        self.occupied_by = deque(['p0'], maxlen=1)  # p0: unoccupied position | p1(p2): occupied by player 1(player 2)
        for row in range(self.size):
            self.mapping.append([])
            for col in range(self.size):
                self.mapping[row].append(self.occupied_by)  # Init matrix mapping values to unoccupied
        
    def __str__(self):
        return f"{self.p1.name} it's your move"

    def print_board(self):  # __str__
        pass

    def make_move(self):
        pass

    def toggle_player(self):
        pass

    @classmethod
    def build_board(cls):
        while True:
            try:
                cls.size = int(input("Enter the board size (between 5 - 10): "))
            except ValueError:
                cls.attempts -= 1
                if cls.attempts == 0:
                    print("Too many wrong attempts! Board size has been defaulted to 7")
                    cls.size = 7
                    break
                else:
                    print("An invalid value has been entered!!\n"
                          "The valid values are: [5, 6, 7, 8 , 9, 10]\n"
                          f"You have {cls.attempts} left")
                    continue
            break


b = Board()
