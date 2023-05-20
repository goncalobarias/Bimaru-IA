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

grids = []
hints = set()
vals = {"000010010": "t", "010010000": "b", "000110000": "l", "000011000": "r"}


class Board:
    """Internal representation of a Bimaru board."""

    def __init__(self, cells, rows_num, cols_num, boats_num, choices):
        """The board consists of cells with initial constraints."""
        self.cells = cells
        self.rows_num = rows_num
        self.cols_num = cols_num
        self.boats_num = boats_num
        self.choices = choices
        self.size = len(cells)

    @staticmethod
    def generate_grids():
        """Generates all the possible grids for each size of boat. A grid
        consists of a single boat (size 1 to 4) placed horizontally or
        vertically."""
        for size in range(1, 5):
            for row in range(10):
                for col in range(10):
                    if 10 - row >= size:
                        # Gets the horizontal placed grids
                        grid = np.zeros((10, 10), dtype=int)
                        for d_row in range(size):
                            grid[row + d_row, col] = 1
                        grids.append(grid)
                    if size != 1 and 10 - col >= size:
                        # Gets the vertical placed grids if it's not a submarine
                        grid = np.zeros((10, 10), dtype=int)
                        for d_col in range(size):
                            grid[row, col + d_col] = 1
                        grids.append(grid)

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
        rows_info = stdin.readline().strip("\n")
        rows_num = np.array(tuple(map(int, rows_info.split("\t")[1:])))
        cols_info = stdin.readline().strip("\n")
        cols_num = np.array(tuple(map(int, cols_info.split("\t")[1:])))
        boats_num = [0, 4, 3, 2, 1]
        choices = ()
        board_size = len(rows_num)
        cells = np.zeros((board_size, board_size), dtype=int)

        hint_total = int(input())
        for _ in range(hint_total):
            hint = stdin.readline().strip("\n").split("\t")[1:]
            hint[0], hint[1] = int(hint[0]), int(hint[1])
            hints.add(tuple(hint))

        return Board(cells, rows_num, cols_num, boats_num, choices)

    def get_adjacent_values(self, row: int, col: int):
        """Gets adjacent values of a certain position (row, col) and pads them."""
        padded_cells = np.pad(self.cells, ((1, 1), (1, 1)), mode="constant")
        return padded_cells[row: row + 3, col: col + 3].ravel()

    def check_hints(self):
        """"""
        
        for hint in hints:
            if hint[2] == "W" and self.cells[hint[0], hint[1]] != 0:
                return False
            adj = self.get_adjacent_values(hint[0], hint[1])
            ones = np.count_nonzero(adj)
            if ones == 1 and hint[2] != "C":
                return False
            if ones == 3 and hint[2] != "M":
                return False
            if ones == 2 and hint[2].lower() != vals["".join(adj)]:
                return False
        return True
    
    def can_place_boat(self, grid):
        """"""
        rows_diff = self.rows_num - np.sum(grid, axis=0)
        cols_diff = self.cols_num - np.sum(grid, axis=1)
        if any(num < 0 for num in rows_diff) or any(num < 0 for num in cols_diff):
            return False
        augmented_grid = grid.copy()
        pos_with_ones = np.where(grid == 1)
        row_i, col_i = pos_with_ones[0], pos_with_ones[1]
        for row, col in zip(row_i, col_i):
            for d_row in range(-1, 2):
                for d_col in range(-1, 2):
                    if 0 <= row + d_row < self.size and 0 <= col + d_col < self.size:
                        augmented_grid[row + d_row, col + d_col] = 1
        if np.count_nonzero(augmented_grid & self.cells) != 0:
            return False
        return self.check_hints()

    def place_boat(self, action):
        """Places boat in the grid."""

        if action == 0:
            return Board(
                self.cells,
                self.rows_num,
                self.cols_num,
                self.boats_num,
                np.append(self.choices, action),
            )

        grid_to_add = grids[len(self.choices)]

        new_cells = np.add(self.cells, grid_to_add)
        new_rows_num = self.rows_num - np.sum(grid_to_add, axis=0)
        new_cols_num = self.cols_num - np.sum(grid_to_add, axis=1)
        new_boats_num = self.boats_num.copy()
        new_boats_num[np.sum(grid_to_add)] -= 1

        return Board(
            new_cells,
            new_rows_num,
            new_cols_num,
            new_boats_num,
            np.append(self.choices, action),
        )

    def is_board_complete(self):
        """"""
        if sum(self.boats_num) != 0:
            return False
        return self.check_hints()

    def __repr__(self):
        """External representation of a Bimaru board that follows the specified
        format."""
        board_repr = self.cells.tolist()
        for row in range(self.size):
            for col in range(self.size):
                if self.cells[row, col] == 0:
                    board_repr[row][col] = "."
                    continue
                adj = self.get_adjacent_values(row, col)
                ones = np.count_nonzero(adj)
                if ones == 1:
                    board_repr[row][col] = "c"
                elif ones == 3:
                    board_repr[row][col] = "m"
                else:
                    board_repr[row][col] = vals["".join(adj)]
        for hint in hints:
            board_repr[hint[0]][hint[1]] = hint[2]
        return "\n".join(map(lambda vals: "".join(vals), board_repr))


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
        next_grid = len(state.board.choices)
        # TODO: might be able to skip a few grids if the last choice was 1
        if next_grid == len(grids):
            return ()
        if state.board.can_place_boat(grids[next_grid]):
            return (0, 1)
        return (0,)

    def result(self, state: BimaruState, action):
        """Returns the state obtained by executing the 'action' on the
        'state' passed as an argument. The action to execute must be one
        present in the list obtained by executing self.actions(state)."""
        return BimaruState(state.board.place_boat(action))

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
