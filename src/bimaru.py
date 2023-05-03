# File: bimaru.py
# Group 10:
#   103124 Gonçalo Bárias
#   102624 Raquel Braunschweig

import sys
from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)


class BimaruState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = BimaruState.state_id
        BimaruState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id

    # TODO: other methods of the class


class Board:
    """Internal representation of a Bimaru board."""

    def get_value(self, row: int, col: int) -> str:
        """Returns the value in the respective board position."""
        # TODO
        pass

    def adjacent_vertical_values(self, row: int, col: int) -> (str, str):
        """Returns the values immediately above and below,
        respectively."""
        # TODO
        pass

    def adjacent_horizontal_values(self, row: int, col: int) -> (str, str):
        """Returns the values immediately to the left and right,
        respectively."""
        # TODO
        pass

    @staticmethod
    def parse_instance():
        """Reads the test from the standard input (stdin) that is passed as an
        argument and returns an instance of the Board class.

        For example:
            $ python3 bimaru.py < input_T01

            > from sys import stdin
            > line = stdin.readline().split()
        """
        # TODO
        pass

    # TODO: other methods of the class


class Bimaru(Problem):
    def __init__(self, board: Board):
        """The constructor specifies the initial state."""
        # TODO
        pass

    def actions(self, state: BimaruState):
        """Returns a list of actions that can be performed from
        from the state passed as an argument."""
        # TODO
        pass

    def result(self, state: BimaruState, action):
        """Returns the state obtained by executing the 'action' on the
        'state' passed as an argument. The action to execute must be one
        present in the list obtained by executing
        self.actions(state)."""
        # TODO
        pass

    def goal_test(self, state: BimaruState):
        """Returns True if and only if the state passed as an argument is
        an objective state. It should check that all positions on the board
        are filled according to the rules of the problem."""
        # TODO
        pass

    def h(self, node: Node):
        """Heuristic function used for the A* search."""
        # TODO
        pass

    # TODO: other methods of the class


if __name__ == "__main__":
    # TODO:
    # Read the standard input file,
    # Use a search technique to solve the instance,
    # Retrieve the solution from the resulting node,
    # Print to the standard output in the indicated format.
    pass
