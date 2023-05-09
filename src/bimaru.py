# File: bimaru.py
# Description: Python program that solves the bimaru game.
# Group 10:
#   103124 Gonçalo Bárias
#   102624 Raquel Braunschweig

from sys import stdin
from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)

_boat_piece_vals = ("T", "t", "B", "b", "L", "l", "R", "r", "M", "m", "C", "c")
_water_vals = ("W", ".")
_boat_piece_extreme_vals = ("T", "t", "L", "l", "C", "c")
_incomp_vals = ("?", "x")


class Board:
    """Internal representation of a Bimaru board."""

    def __init__(self, cells, rows_fixed_num, cols_fixed_num):
        """The board consists of cells with initial constraints."""
        self.cells = cells
        self.size = len(cells)
        self.rows_fixed_num = rows_fixed_num
        self.cols_fixed_num = cols_fixed_num
        self.is_invalid = False

    def get_value(self, row: int, col: int) -> str:
        """Returns the value in the respective board position."""
        if 0 <= row < self.size and 0 <= col < self.size:
            return self.cells[row][col]

    def get_row(self, row: int):
        """Returns the given row in the board."""
        return tuple(self.cells[row])

    def get_col(self, col: int):
        """Returns the given column in the board."""
        return tuple(self.cells[row][col] for row in range(self.size))

    def get_adjacent_vertical_values(self, row: int, col: int) -> (str, str):
        """Returns the values immediately above and below,
        respectively."""
        return (self.get_value(row - 1, col), self.get_value(row + 1, col))

    def get_adjacent_horizontal_values(self, row: int, col: int) -> (str, str):
        """Returns the values immediately to the left and right,
        respectively."""
        return (self.get_value(row, col - 1), self.get_value(row, col + 1))

    def get_adjacent_diagonal_values(self, row: int, col: int):
        """Returns the values in the two diagonals of the selected position,
        starting from the top right diagonal positon and going
        around clockwise."""
        return (
            self.get_value(row - 1, col - 1),
            self.get_value(row - 1, col + 1),
            self.get_value(row + 1, col - 1),
            self.get_value(row + 1, col + 1),
        )

    def get_adjacent_values(self, row: int, col: int):
        """Returns all the adjacent values to the given position."""
        return (
            self.get_adjacent_vertical_values(row, col)
            + self.get_adjacent_horizontal_values(row, col)
            + self.get_adjacent_diagonal_values(row, col)
        )

    def check_boat_piece_isolation(self, row: int, col: int, boat_type: str):
        """"""
        # TODO
        pass

    def check_boat_completion(self, row: int, col: int):
        """Returns boolean value true if boat is complete, false otherwise."""
        val = self.get_value(row, col).lower()

        match val:
            case "c":
                return True
            case "t" | "b":
                adj_vals = self.get_adjacent_vertical_values(row, col)
                i = 0
                if val == "t":
                    i = 1
                while adj_vals[i].lower() == "m":
                    row += (-1) ^ i  # know if it's positive or negative direction
                    adj_vals = self.get_adjacent_vertical_values(row, col)
                if adj_vals[i].lower() == "b" or adj_vals[i].lower() == "t":
                    return True
            case "r" | "l":
                adj_vals = self.get_adjacent_horizontal_values(row, col)
                i = 0
                if val == "l":
                    i = 1
                while adj_vals[i].lower() == "m":
                    col += (-1) ^ i  # know if it's positive or negative direction
                    adj_vals = self.get_adjacent_vertical_values(row, col)
                if adj_vals[i].lower() == "r" or adj_vals[i].lower() == "l":
                    return True
            case other:
                return False

        return False

    def get_initial_state(self):
        """"""
        self.remaining_cells_num = 100
        self.boats_distribution = [0, 4, 3, 2, 1]

        sum_rows_fixed_num = sum(self.rows_fixed_num)
        if sum_rows_fixed_num != 20 or sum_rows_fixed_num != sum(self.cols_fixed_num):
            # The total board has to have 20 boat pieces, no more and no less.
            # Therefore if the constraints ask for less or more, the puzzle is
            # invalid.
            self.is_invalid = True
            return self

        self.rows_boat_pieces_num = []
        self.rows_water_num = []
        for row in range(self.size):
            boat_pieces_num, water_num = 0, 0
            for col in range(self.size):
                val = self.get_value(row, col)
                if val in _boat_piece_vals:
                    self.check_boat_piece_isolation(row, col, val)
                    boat_pieces_num += 1
                elif val in _water_vals:
                    water_num += 1
            if boat_pieces_num > self.rows_fixed_num:
                self.is_invalid = True
            if self.is_invalid:
                return self  # abort immediately to save computing costs
            self.rows_boat_pieces_num.append(boat_pieces_num)
            self.rows_water_num.append(water_num)

        self.cols_boat_pieces_num = []
        self.cols_water_num = []
        for col in range(self.size):
            boat_pieces_num, water_num = 0, 0
            for row in range(self.size):
                if self.get_value(row, col) in _boat_piece_vals:
                    if self.get_value(row, col) in _boat_piece_extreme_vals:
                        self.check_boat_completion(row, col)
                    boat_pieces_num += 1
                elif self.get_value(row, col) in _water_vals:
                    water_num += 1
            if boat_pieces_num > self.cols_fixed_num:
                self.is_invalid = True
            if self.is_invalid:
                return self  # abort immediately to save computing costs
            self.cols_boat_pieces_num.append(boat_pieces_num)
            self.cols_water_num.append(water_num)

        return self.reduce_board()

    def isolate_boat_piece(self, row: int, col: int, boat_type: str):
        """"""
        # TODO
        pass

    def find_boat_piece(self, row: int, col: int):
        """"""
        # TODO: Has to check if a boat was completed (if the boat piece found
        # is an extreme) by calling check_boat_completion on extreme pieces.
        pass

    def reduce_board(self):
        """"""

        # TODO: traverse the rows while "cleaning" them and isolating boat
        # pieces

        # TODO: traverse the cols while "cleaning" them and finding the boat
        # pieces

        return self

    def get_placements_for_boat(self, size: int):
        """"""
        # TODO
        pass

    def is_placement_valid(self, row: int, col: int, size: int, orientation: str):
        """Checks if a placement is valid. It has to add a boat in a position
        such that it won't touch another boat diagonally, vertically or
        horizontally. It also has to respect the column and row constraints."""
        # TODO: Use check_boat_piece_isolation to make sure no boats are around
        # any of its pieces. Has to make sure the constraints are met on each
        # col/row. Has to make sure the boat doesn't surprass the counter.
        pass

    def place_boat(self, row: int, col: int, size: int, orientation: str):
        """Returns a new board that results from placing the given boat in the
        valid position. In order to be valid the is_placement_valid function
        must return True for the given placement/position."""
        # TODO: Has to decrease the boat counter for the given size.
        return Board(self.cells, self.rows_fixed_num, self.cols_fixed_num).reduce_board

    def is_board_complete(self):
        """Checks if the board is a valid solution to the puzzle. For a
        Bimaru puzzle to be complete it needs to have all the constraints in
        the columns and rows satisfied, have zero incomplete cells to
        fill and be a valid board."""
        if self.is_invalid or self.remaining_cells_num != 0:
            return False

        for row, row_num in enumerate(self.rows_fixed_num):
            if self.rows_boat_pieces_num[row] != row_num or any(
                incomp_val in _incomp_vals for incomp_val in self.get_row(row)
            ):
                return False
        for col, col_num in enumerate(self.cols_fixed_num):
            if self.cols_boat_pieces_num[col] != col_num:
                return False

        return True

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
        rows_fixed_num = tuple(map(int, rows_info.split("\t")[1:]))
        cols_info = stdin.readline().strip("\n")
        cols_fixed_num = tuple(map(int, cols_info.split("\t")[1:]))
        board_size = len(rows_fixed_num)

        cells = [["?" for _ in range(board_size)] for _ in range(board_size)]
        hint_total = int(input())
        for _ in range(hint_total):
            hint = stdin.readline().strip("\n").split("\t")[1:]
            hint_row, hint_col = int(hint[0]), int(hint[1])
            cells[hint_row][hint_col] = hint[2]

        return Board(cells, rows_fixed_num, cols_fixed_num).get_initial_state()

    def __repr__(self):
        """External representation of a Bimaru board that follows the specified
        format."""
        return "\n".join(map(lambda val: "".join(val), self.cells))


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
    def __init__(self, board: Board):
        """The constructor specifies the initial state."""
        state = BimaruState(board)
        super().__init__(state)

    def actions(self, state: BimaruState):
        """Returns a list of actions that can be performed from
        from the state passed as an argument."""
        if state.board.remaining_cells_num == 0 or state.board.is_invalid:
            return []

        for next_size in reversed(range(4 + 1)):
            if next_size == 0:
                return []
            if self.boats_distribution[next_size] != 0:
                break

        return state.board.get_placements_for_boat(next_size)

    def result(self, state: BimaruState, action):
        """Returns the state obtained by executing the 'action' on the
        'state' passed as an argument. The action to execute must be one
        present in the list obtained by executing self.actions(state)."""
        (row, col, size, orientation) = action
        return BimaruState(state.board.place_boat(row, col, size, orientation))

    def goal_test(self, state: BimaruState):
        """Returns True if and only if the state passed as an argument is
        a goal state. It should check that all positions on the board
        are filled according to the rules of the problem."""
        return state.board.is_board_complete()

    def h(self, node: Node):
        """Heuristic function used for informed searches."""
        # TODO: não faço ideia o que usar como heurística ngl
        pass


if __name__ == "__main__":
    """Read the standard input file.
    Use a search technique to solve the instance.
    Retrieve the solution from the resulting node.
    Print to the standard output in the indicated format."""
    board = Board.parse_instance()
    bimaru = Bimaru(board)
    goal_node = breadth_first_tree_search(bimaru)
    print(goal_node.state.board)
