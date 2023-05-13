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

boat_piece_vals = ("t", "b", "l", "r", "c", "m", "x")
water_vals = ("W", ".")
incomp_vals = ("?", "x")
orientation_vecs = {
    "t": (1, 0, "b"),
    "b": (-1, 0, "t"),
    "l": (0, 1, "r"),
    "r": (0, -1, "l"),
    "c": (0, 0, "c"),
}


class Board:
    """Internal representation of a Bimaru board."""

    def __init__(self, cells, rows_fixed_num, cols_fixed_num):
        """The board consists of cells with initial constraints."""
        self.cells = cells
        self.size = len(cells)
        self.rows_fixed_num = rows_fixed_num
        self.cols_fixed_num = cols_fixed_num
        self.is_invalid = False

    def get_value(self, row: int, col: int):
        """Returns the value in the respective board position."""
        if 0 <= row < self.size and 0 <= col < self.size:
            return self.cells[row][col].lower()

    def set_value(self, row: int, col: int, val: str, override=False, count=True):
        """Sets the value in the respective board position."""
        if (
            0 <= row < self.size
            and 0 <= col < self.size
            and ((not override and self.get_value(row, col) == "?") or override)
        ):
            self.cells[row][col] = val
            if count:
                if val in water_vals:
                    self.rows_water_num[row] += 1
                    self.cols_water_num[col] += 1
                elif val in boat_piece_vals:
                    self.rows_boat_pieces_num[row] += 1
                    self.cols_boat_pieces_num[col] += 1

    def get_adjacent_touching_values(self, row: int, col: int):
        return (
            self.get_value(row - 1, col),
            self.get_value(row, col + 1),
            self.get_value(row + 1, col),
            self.get_value(row, col - 1),
        )

    def set_adjacent_touching_values(
        self, row: int, col: int, t: str, r: str, b: str, l: str
    ):
        self.set_value(row - 1, col, t)
        self.set_value(row, col + 1, r)
        self.set_value(row + 1, col, b)
        self.set_value(row, col - 1, l)

    def get_adjacent_diagonal_values(self, row: int, col: int):
        """Returns the values in the two diagonals of the selected position,
        starting from the top right diagonal positon and going
        around clockwise."""
        return (
            self.get_value(row - 1, col - 1),
            self.get_value(row - 1, col + 1),
            self.get_value(row + 1, col + 1),
            self.get_value(row + 1, col - 1),
        )

    def set_adjacent_diagonal_values(
        self, row: int, col: int, tl: str, tr: str, bl: str, br: str
    ):
        """Sets the diagonal values to the values it receives."""
        self.set_value(row - 1, col - 1, tl)
        self.set_value(row - 1, col + 1, tr)
        self.set_value(row + 1, col + 1, br)
        self.set_value(row + 1, col - 1, bl)

    def check_boat_piece_isolation(self, row: int, col: int, boat_type: str):
        """Checks if a boat piece is isolated."""
        if any(
            val in boat_piece_vals
            for val in self.get_adjacent_diagonal_values(row, col)
        ):
            return False

        touching_adjacents = self.get_adjacent_touching_values(row, col)
        if boat_type in ("t", "r", "b", "l"):
            d_row, d_col, other_extreme = orientation_vecs[boat_type]
            if self.get_value(row + d_row, col + d_col) not in (
                "?",
                "x",
                "m",
                other_extreme,
            ):
                return False
            if self.get_value(row - d_row, col - d_col) in boat_piece_vals:
                return False
            if self.get_value(row + d_col, col + d_row) in boat_piece_vals:
                return False
            if self.get_value(row - d_col, col - d_row) in boat_piece_vals:
                return False
        elif boat_type == "c":
            if any(val in boat_piece_vals for val in touching_adjacents):
                return False
        elif boat_type == "m":
            if sum(val in water_vals for val in touching_adjacents) >= 3:
                return False
            for i in range(3):
                if (
                    touching_adjacents[i] in water_vals
                    and touching_adjacents[i + 1] in water_vals
                ) or (
                    touching_adjacents[i] in boat_piece_vals
                    and touching_adjacents[i + 1] in boat_piece_vals
                ):
                    return False
        elif boat_type == "x":
            for i in range(3):
                if (
                    touching_adjacents[i] in boat_piece_vals
                    and touching_adjacents[i + 1] in boat_piece_vals
                ):
                    return False
        return True

    def isolate_boat_piece(self, row: int, col: int, boat_type: str):
        """Isolates boat pieces."""
        if not self.check_boat_piece_isolation(row, col, boat_type):
            self.is_invalid = True
            return

        self.set_adjacent_diagonal_values(row, col, ".", ".", ".", ".")
        if boat_type in ("t", "r", "b", "l"):
            d_row, d_col, _ = orientation_vecs[boat_type]
            self.set_value(row + d_row, col + d_col, "x")
            self.set_adjacent_touching_values(row, col, ".", ".", ".", ".")
        elif boat_type == "c":
            self.set_adjacent_touching_values(row, col, ".", ".", ".", ".")
        elif boat_type == "m":
            touching_adjacents = self.get_adjacent_touching_values(row, col)
            if touching_adjacents.count("?") == 4:
                return
            for i, touching_adjacent in enumerate(touching_adjacents):
                if touching_adjacent != "?":
                    break
            if (touching_adjacent in boat_piece_vals and (i == 0 or i == 2)) or (
                touching_adjacent in water_vals and (i == 1 or i == 3)
            ):
                self.set_adjacent_touching_values(row, col, "x", ".", "x", ".")
            elif (touching_adjacent in boat_piece_vals and (i == 1 or i == 3)) or (
                touching_adjacent in water_vals and (i == 0 or i == 2)
            ):
                self.set_adjacent_touching_values(row, col, ".", "x", ".", "x")

    def check_boat_completion(self, row: int, col: int):
        """Given an extreme piece of a boat it checks if it is part of a
        complete boat by finding the other extreme piece. If it discovers a
        boat it updates the counter with the number of boats available."""
        val = self.get_value(row, col)
        if val == "c":
            self.boats_distribution[1] -= 1  # it's a submarine that has size 1
            return
        if val == "m" and self.get_value(row - 1, col) in boat_piece_vals:
            d_row, d_col = -1, 0
            row, col = row + d_row, col + d_col
            val = self.get_value(row, col)
        elif val == "m" and self.get_value(row, col - 1) in boat_piece_vals:
            d_row, d_col = 0, -1
            row, col = row + d_row, col + d_col
            val = self.get_value(row, col)
        elif val == "m":
            return
        while val == "m":
            row += d_row
            col += d_col
            val = self.get_value(row, col)
        if val in incomp_vals or val in water_vals:
            return  # if it's not a boat piece we return

        d_row, d_col, other_extreme = orientation_vecs[val]
        size = 2  # every other boat has two extremes besides the submarine
        while self.get_value(row + d_row, col + d_col) == "m":
            row += d_row
            col += d_col
            size += 1
        if size > 4:
            self.is_invalid = True
            return
        if self.get_value(row + d_row, col + d_col) == other_extreme:
            self.boats_distribution[size] -= 1

    def get_initial_state(self):
        """"""
        self.boats_distribution = [0, 4, 3, 2, 1]

        sum_rows_fixed_num = sum(self.rows_fixed_num)
        if sum_rows_fixed_num != 20 or sum_rows_fixed_num != sum(self.cols_fixed_num):
            # The total board has to have 20 boat pieces, no more and no less.
            # Therefore if the constraints ask for less or more, the puzzle is
            # invalid.
            self.is_invalid = True
            return self

        self.rows_boat_pieces_num = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.rows_water_num = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.cols_boat_pieces_num = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.cols_water_num = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for row in range(self.size):
            for col in range(self.size):
                if self.get_value(row, col) in boat_piece_vals:
                    self.rows_boat_pieces_num[row] += 1
                    self.cols_boat_pieces_num[col] += 1
                elif self.get_value(row, col) in water_vals:
                    self.rows_water_num[row] += 1
                    self.cols_water_num[col] += 1
                if self.cols_boat_pieces_num[col] > self.cols_fixed_num[col]:
                    self.is_invalid = True
                    return self  # abort immediately to save computing costs
            if self.rows_boat_pieces_num[row] > self.rows_fixed_num[row]:
                self.is_invalid = True
                return self  # abort immediately to save computing costs
        for row in range(self.size):
            for col in range(self.size):
                if self.get_value(row, col) in boat_piece_vals:
                    self.isolate_boat_piece(row, col, self.get_value(row, col))
                    if self.is_invalid:
                        return self  # abort immediately to save computing costs
        for row in range(self.size):
            for col in range(self.size):
                if self.get_value(row, col) in ("t", "l", "c"):
                    self.check_boat_completion(row, col)
        return self.reduce_board()

    def find_boat_piece(self, row: int, col: int):
        """"""
        if self.get_value(row, col) != "x":
            return
        if "?" in self.get_adjacent_touching_values(row, col):
            return

        for boat_piece_val in boat_piece_vals:
            if self.check_boat_piece_isolation(row, col, boat_piece_val):
                break

        self.set_value(row, col, boat_piece_val, True, False)
        self.check_boat_completion(row, col)

    def reduce_board(self):
        """"""
        for _ in range(2):
            for diag in range(self.size):
                if self.size - self.rows_water_num[diag] == self.rows_fixed_num[diag]:
                    for col in range(self.size):
                        self.set_value(diag, col, "x")
                elif self.rows_boat_pieces_num[diag] == self.rows_fixed_num[diag]:
                    for col in range(self.size):
                        self.set_value(diag, col, ".")
                if self.size - self.cols_water_num[diag] == self.cols_fixed_num[diag]:
                    for row in range(self.size):
                        self.set_value(row, diag, "x")
                elif self.cols_boat_pieces_num[diag] == self.cols_fixed_num[diag]:
                    for row in range(self.size):
                        self.set_value(row, diag, ".")
            for row in range(self.size):
                for col in range(self.size):
                    if self.get_value(row, col) in boat_piece_vals:
                        self.isolate_boat_piece(row, col, self.get_value(row, col))
                        self.find_boat_piece(row, col)
        return self

    def is_placement_valid(self, row: int, col: int, size: int, orientation: str):
        """Checks if a placement is valid. It has to add a boat in a position
        such that it won't touch another boat diagonally, vertically or
        horizontally. It also has to respect the column and row constraints.
        """
        d_row, d_col, other_extreme = orientation_vecs[orientation]
        i_row, i_col = row, col
        count = 0
        for _ in range(size):
            val = self.get_value(i_row, i_col)
            if val != "x" and val in boat_piece_vals:
                count += 1
            i_row += d_row
            i_col += d_col
        if count == size:
            return False
        for i in range(size):
            if i == 0 and self.get_value(row, col) not in (
                "?",
                "x",
                orientation,
            ):
                return False
            elif i == size - 1 and self.get_value(row, col) not in (
                "?",
                "x",
                other_extreme,
            ):
                return False
            elif (
                i != 0
                and i != size - 1
                and self.get_value(row, col) not in ("?", "x", "m")
            ):
                return False
            if i == 0 and not self.check_boat_piece_isolation(row, col, orientation):
                return False
            elif i == size - 1 and not self.check_boat_piece_isolation(
                row, col, other_extreme
            ):
                return False
            elif (
                i != 0
                and i != size - 1
                and not self.check_boat_piece_isolation(row, col, "m")
            ):
                return False
            row += d_row
            col += d_col
        return True

    def get_placements_for_boat(self, size: int):
        """"""

        placements = ()
        for diag in range(self.size):
            orientation = "l"
            if size == 1:
                orientation = "c"
            if self.rows_fixed_num[diag] >= size:
                for col in range(self.size - size + 1):
                    if self.is_placement_valid(diag, col, size, orientation):
                        placements += ((diag, col, size, orientation),)

            orientation = "t"
            if size == 1:
                orientation = "c"
            if self.cols_fixed_num[diag] >= size:
                for row in range(self.size - size + 1):
                    if self.is_placement_valid(row, diag, size, orientation):
                        placements += ((row, diag, size, orientation),)

        return placements

    def place_boat(self, row: int, col: int, size: int, orientation: str):
        """Returns a new board that results from placing the given boat in the
        valid position. In order to be valid the is_placement_valid function
        must return True for the given placement/position."""
        new_cells = [[val for val in self.cells[row]] for row in range(self.size)]
        new_board = Board(new_cells, self.rows_fixed_num, self.cols_fixed_num)

        new_board.rows_boat_pieces_num = self.rows_boat_pieces_num.copy()
        new_board.cols_boat_pieces_num = self.cols_boat_pieces_num.copy()
        new_board.rows_water_num = self.rows_water_num.copy()
        new_board.cols_water_num = self.cols_water_num.copy()
        new_board.boats_distribution = self.boats_distribution.copy()
        new_board.boats_distribution[size] -= 1
        d_row, d_col, other_extreme = orientation_vecs[orientation]
        for i in range(size):
            if i == 0:
                boat_type = orientation
            elif i == size - 1:
                boat_type = other_extreme
            else:
                boat_type = "m"
            if new_board.get_value(row, col) == "?":
                new_board.set_value(row, col, boat_type)
            elif new_board.get_value(row, col) == "x":
                new_board.set_value(row, col, boat_type, True, False)
            new_board.isolate_boat_piece(row, col, boat_type)
            row += d_row
            col += d_col

        return new_board.reduce_board()

    def is_board_complete(self):
        """Checks if the board is a valid solution to the puzzle. For a
        Bimaru puzzle to be complete it needs to have all the constraints in
        the columns and rows satisfied, have zero incomplete cells to
        fill and be a valid board."""
        if any(num < 0 for num in self.boats_distribution):
            self.is_invalid = True
        if self.is_invalid or sum(self.boats_distribution) != 0:
            return False

        for row, row_num in enumerate(self.rows_fixed_num):
            if self.rows_boat_pieces_num[row] != row_num or any(
                val in incomp_vals for val in self.cells[row]
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
            cells[hint_row][hint_col] = hint[2]  # inserts the hint into the board

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
        if state.board.is_invalid or sum(state.board.boats_distribution) == 0:
            return ()

        for next_size in reversed(range(4 + 1)):
            if next_size == 0:
                return ()
            if state.board.boats_distribution[next_size] != 0:
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
        return sum(node.state.board.boats_distribution)


if __name__ == "__main__":
    """Read the standard input file.
    Use a search technique to solve the instance.
    Retrieve the solution from the resulting node.
    Print to the standard output in the indicated format."""
    board = Board.parse_instance()
    bimaru = Bimaru(board)
    goal_node = greedy_search(bimaru)
    print(goal_node.state.board)
