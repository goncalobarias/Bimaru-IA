# File: bimaru.py
# Description: Python program that solves the bimaru game.
# Group 10:
#   103124 Gonçalo Bárias
#   102624 Raquel Braunschweig

from sys import stdin
import numpy as np
from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)

grids = ()


class Board:
    """Internal representation of a Bimaru board."""

    def __init__(self, cells, rows_num, cols_num, boats_num):
        """The board consists of cells with initial constraints."""
        self.cells = cells
        self.rows_num = rows_num
        self.cols_num = cols_num
        self.boats_num = boats_num
        self.size = len(cells)

    @staticmethod
    def generate_grids():
        """"""
        pass

    @staticmethod
    def parse_instance():
        """Reads the test from the standard input (stdin) that is passed as an
        argument and returns an instance of the Board class.

        Input format:
            ROW <count-0> ... <count-9>
            COLUMN <count-0> ... <count-9>
            <hint total>
            HINT <row> <column> <hint value>
        """
        pass

    def can_place_boat(self):
        """"""
        pass

    def place_boat(self):
        """"""
        pass

    def is_board_complete(self):
        """"""
        pass

    def __repr__(self):
        """External representation of a Bimaru board that follows the specified
        format."""
        pass


class BimaruState:
    """Represents the state used in the search algorithms."""

    state_id = 0

    def __init__(self, board: Board):
        """Each state has a board and a unique identifier."""
        self.board = board
        self.id = BimaruState.state_id
        BimaruState.state_id += 1

    def __lt__(self, other):
        """This method is used in case of a tie in the management of the
        open list in the informed searches."""
        return self.id < other.id


class Bimaru(Problem):
    """Implements the Problem superclass to solve the bimaru problem."""

    def __init__(self, board: Board):
        """The constructor specifies the initial state."""
        state = BimaruState(board)
        super().__init__(state)

    def actions(self, state: BimaruState):
        """Returns a list of actions that can be performed from
        from the state passed as an argument."""
        pass

    def result(self, state: BimaruState, action):
        """Returns the state obtained by executing the 'action' on the
        'state' passed as an argument. The action to execute must be one
        present in the list obtained by executing self.actions(state)."""
        pass

    def goal_test(self, state: BimaruState):
        """Returns True if and only if the state passed as an argument is
        a goal state. It should check that all positions on the board
        are filled according to the rules of the problem."""
        return state.board.is_board_complete()

    def h(self, node: Node):
        """Heuristic function used for informed searches."""
        return sum(node.state.board.boats_num)


if __name__ == "__main__":
    """Read the standard input file.
    Use a search technique to solve the instance.
    Retrieve the solution from the resulting node.
    Print to the standard output in the indicated format."""
    Board.generate_grids()
    board = Board.parse_instance()
    bimaru = Bimaru(board)
    goal_node = astar_search(bimaru)
    print(goal_node.state.board)
