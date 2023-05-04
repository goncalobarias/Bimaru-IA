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
    """Represents the state used in the search algorithms."""

    state_id = 0

    def __init__(self, board):
        """Each state has a board and a unique identifier."""
        self.board = board
        self.id = BimaruState.state_id
        BimaruState.state_id += 1

    def __lt__(self, other):
        """This method is used in case of a tie in the management of the
        open list in the informed searches."""
        return self.id < other.id

    # TODO: other methods of the class


class Board:
    """Internal representation of a Bimaru board."""

    def __init__(self, cells, rows_n, cols_n):
        """The board consists of cells with initial constraints."""
        self.cells = cells
        self.rows_n = rows_n
        self.cells_n = cols_n

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

        Format:
            ROW <count-0> ... <count-9>
            COLUMN <count-0> ... <count-9
            <hint total>
            HINT <row> <column> <hint value>
        """
        rows_info = sys.stdin.readline().strip("\n")
        rows_n = tuple(map(int, rows_info.split("\t")[1:]))
        cols_info = sys.stdin.readline().strip("\n")
        cols_n = tuple(map(int, cols_info.split("\t")[1:]))

        hint_total = int(input())
        cells = [["." for _ in range(10)] for _ in range(10)]
        for _ in range(hint_total):
            hint = sys.stdin.readline().strip("\n").split("\t")[1:]
            hint_x = int(hint[1])
            hint_y = int(hint[0])
            cells[hint_y][hint_x] = hint[2]

        return Board(cells, rows_n, cols_n).get_instance()

    def get_instance(self):
        """Obtains the initial state of the bimaru board."""
        return self

    def __repr__(self):
        """External representation of the board that follows the specified
        format."""
        return "\n".join(map(lambda x: "".join(x), self.cells))

    # TODO: other methods of the class


class Bimaru(Problem):
    def __init__(self, board: Board):
        """The constructor specifies the initial state."""
        state = BimaruState(board)
        super().__init__(state)

    def actions(self, state: BimaruState):
        """Returns a list of actions that can be performed from
        from the state passed as an argument."""
        # TODO
        pass

    def result(self, state: BimaruState, action):
        """Returns the state obtained by executing the 'action' on the
        'state' passed as an argument. The action to execute must be one
        present in the list obtained by executing self.actions(state)."""
        # TODO
        pass

    def goal_test(self, state: BimaruState):
        """Returns True if and only if the state passed as an argument is
        a goal state. It should check that all positions on the board
        are filled according to the rules of the problem."""
        # TODO
        pass

    def h(self, node: Node):
        """Heuristic function used for informed searches."""
        # TODO
        pass

    # TODO: other methods of the class


if __name__ == "__main__":
    # Read the standard input file,
    # Use a search technique to solve the instance,
    # Retrieve the solution from the resulting node,
    # Print to the standard output in the indicated format.
    board = Board.parse_instance()
    bimaru = Bimaru(board)
    goal_node = greedy_search(bimaru)
    print(goal_node.state.board)
