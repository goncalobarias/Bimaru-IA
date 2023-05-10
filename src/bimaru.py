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

_boat_piece_vals = ("t", "b", "l", "r", "m", "c")
_water_vals = ("W", ".")
_incomp_vals = ("?", "x")
_orientation_vecs = {
    "t": (1, 0, "b"),
    "b": (-1, 0, "t"),
    "l": (0, 1, "r"),
    "r": (0, -1, "l"),
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

    def get_adjacent_vertical_values(self, row: int, col: int):
        """Returns the values immediately above and below,
        respectively."""
        return (self.get_value(row - 1, col), self.get_value(row + 1, col))

    def get_adjacent_horizontal_values(self, row: int, col: int):
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

    def turn_diagonal_values_water(self, row: int, col: int):
        """Turns diagonal values into water if they arent "W" or out of limit."""
        if self.get_value(row - 1, col - 1) == _incomp_vals[0]:  # only if "?"
            self.cell[row - 1, col - 1] = _water_vals[1]
        if self.get_value(row + 1, col - 1) == _incomp_vals[0]:
            self.cell[row + 1, col - 1] = _water_vals[1]
        if self.get_value(row + 1, col + 1) == _incomp_vals[0]:
            self.cell[row + 1, col + 1] = _water_vals[1]
        if self.get_value(row + 1, col - 1) == _incomp_vals[0]:
            self.cell[row + 1, col - 1] = _water_vals[1]
        pass

    def isolate_top_bottom(self, row: int, col: int, i: int):
        """Isolates top (T or t) and bottom (B or b) pieces."""
        # puts cell above in case of t as water, otherwise for b
        if self.get_value(row + (-1) ^ (i + 1), col) == _incomp_vals[0]:  # only if "?"
            self.cells[row + (-1) ^ (i + 1), col] = _water_vals[1]
        # adds x bellow in case of t, otherwise for b
        if self.get_value(row + (-1) ^ (i), col) == _incomp_vals[0]:
            self.cells[row + (-1) ^ (i), col] = _incomp_vals[1]
            self.turn_diagonal_values_water(self, row + (-1) ^ (i), col)
        pass

    def isolate_left_right(self, row: int, col: int, i: int):
        """Isolates left (L or l) and right (R or r) pieces."""
        # puts cell at the left in case of r as water, otherwise for l
        if self.get_value(row, col + (-1) ^ (i + 1)) == _incomp_vals[0]:  # only if "?"
            self.cells[row, col + (-1) ^ (i + 1)] = _water_vals[1]
        # adds x at the right in case of l, otherwise for r
        if self.get_value(row, col + (-1) ^ (i)) == _incomp_vals[0]:
            self.cells[row, col + (-1) ^ (i)] = _incomp_vals[1]
            self.turn_diagonal_values_water(self, row, col + (-1) ^ (i))
        pass

    def isolate_circle(self, row: int, col: int):
        """Isolates circle (C or c) pieces."""
        water = _water_vals[1]
        question_mark = _incomp_vals[0]

        # adds waters around vertical and horizontal adjacent values
        if self.get_value(row, col - 1) == question_mark:
            self.cells[row, col - 1] = water
        if self.get_value(row, col + 1) == question_mark:
            self.cells[row, col + 1] = water
        if self.get_value(row - 1, col) == question_mark:
            self.cells[row - 1, col] = water
        if self.get_value(row + 1, col) == question_mark:
            self.cells[row + 1, col] = water
        pass

    def isolate_middle(self, row: int, col: int):
        """Isolates middle (M or m) pieces."""
        water = _water_vals[1]
        question_mark = _incomp_vals[0]
        x = _incomp_vals[1]

        horizontal_vals = self.get_adjacent_horizontal_values(self, row, col)
        i = 0
        while i < 2:
            val = horizontal_vals[i]
            if val == water or val == _water_vals[0]:
                # adds x in vertical values
                if self.get_value(row + 1, col) == question_mark:
                    self.cells[row + 1, col] = x
                    self.turn_diagonal_values_water(self, row + 1, col)
                if self.get_value(row - 1, col) == question_mark:
                    self.cells[row - 1, col] = x
                    self.turn_diagonal_values_water(self, row - 1, col)
                # adds water in other horizontal value
                if self.get_value(row, col + (-1) ^ (i)) == question_mark:
                    self.cells[row, col] = water
                    pass
            i += 1

        vertical_vals = self.get_adjacent_vertical_values(self, row, col)
        i = 0
        while i < 2:
            val = vertical_vals[i]
            if val == water or val == _water_vals[0]:
                # adds x in horizontal values
                if self.get_value(row, col + 1) == question_mark:
                    self.cells[row, col + 1] = x
                    self.turn_diagonal_values_water(self, row, col + 1)
                if self.get_value(row, col - 1) == question_mark:
                    self.cells[row, col - 1] = x
                    self.turn_diagonal_values_water(self, row, col - 1)
                # adds water in other vertical value
                if self.get_value(row + (-1) ^ (i), col) == question_mark:
                    self.cells[row, col] = water
                pass
            i += 1
        pass

    def isolate_boat_piece(self, row: int, col: int, boat_type: str):
        """Isolates boat pieces."""
        self.turn_diagonal_values_water(self, row, col)
        type = boat_type.lower()

        match type:
            case "t" | "b":
                i = 0  # to be able to differentiate
                if type == "t":
                    i = 1
                self.isolate_top_bottom(self, row, col, i)
            case "l" | "r":
                i = 0  # to be able to differentiate
                if type == "l":
                    i = 1
                self.isolate_left_right(self, row, col, i)
            case "m":
                self.isolate_middle(self, row, col)
            case "c":
                self.isolate_circle(row, col)
            case other:
                pass
        pass

    def check_boat_completion(self, row: int, col: int):
        """Given an extreme piece of a boat it checks if it is part of a
        complete boat by finding the other extreme piece. If it discovers a
        boat it updates the counter with the number of boats available."""
        val = self.get_value(row, col).lower()
        if val in _incomp_vals or val == "m":
            return  # if it's a middle boat piece we don't know the orientation
        if val == "c":
            self.boats_distribution[1] -= 1  # it's a submarine that has size 1
            return
        d_row, d_col, other_extreme = _orientation_vecs[val]

        size = 2  # every other boat has two extremes besides the submarine
        while self.get_value(row + d_row, col + d_col).lower() == "m":
            row += d_row
            col += d_col
            size += 1
        if self.get_value(row + d_row, col + d_col).lower() == other_extreme:
            self.boats_distribution[size] -= 1

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
                if val.lower() in _boat_piece_vals:
                    self.isolate_boat_piece(row, col, val)
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
                if self.get_value(row, col).lower() in _boat_piece_vals:
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

    def check_boat_piece_isolation(self, row: int, col: int, boat_type: str):
        """Checks if a boat piece is isolated, returns true if it is."""
        adj_values = self.get_adjacent_values(self, row, col)
        for val in adj_values:
            # if value is yet to be defined piece is not isolated
            if val == _incomp_vals[0]:
                return False
        return True

    def find_boat_piece(self, row: int, col: int):
        """"""
        # TODO: Has to check if a boat was completed (if the boat piece found
        # is an extreme) by calling check_boat_completion on extreme pieces.
        pass

    def reduce_board(self):
        """"""

        # TODO: traverse the whole board and clean each row and column

        return self

    def get_placements_for_boat(self, size: int):
        """"""

        def is_placement_valid(self, row: int, col: int, size: int, orientation: str):
            """Checks if a placement is valid. It has to add a boat in a position
            such that it won't touch another boat diagonally, vertically or
            horizontally. It also has to respect the column and row constraints.
            """
            # TODO: Use check_boat_piece_isolation to make sure no boats are around
            # any of its pieces. Has to make sure the constraints are met on each
            # col/row. Has to make sure the boat doesn't surprass the counter.
            pass

        placements = ()
        for diag in range(self.size):
            if self.rows_fixed_num[diag] - self.rows_boat_pieces_num[diag] >= size:
                for col in range(self.size - size):
                    if is_placement_valid(diag, col, size, "L"):
                        placements += ((diag, col, size, "L"),)

            if self.cols_fixed_num[diag] - self.cols_boat_pieces_num[diag] >= size:
                for row in range(self.size - size):
                    if is_placement_valid(row, diag, size, "T"):
                        placements += ((row, diag, size, "T"),)

        return placements

    def place_boat(self, row: int, col: int, size: int, orientation: str):
        """Returns a new board that results from placing the given boat in the
        valid position. In order to be valid the is_placement_valid function
        must return True for the given placement/position."""
        new_cells = [[val for val in self.cells[row]] for row in range(self.size)]

        new_rows_fixed_num = self.rows_fixed_num.copy()
        new_cols_fixed_num = self.cols_fixed_num.copy()
        d_row, d_col, _ = _orientation_vecs[orientation]
        for _ in range(size):
            new_rows_fixed_num[row] -= 1
            new_cols_fixed_num[col] -= 1
            row += d_row
            col += d_col

        new_board = Board(new_cells, new_rows_fixed_num, new_cols_fixed_num)

        new_board.remaining_cells_num = self.remaining_cells_num - size
        new_board.boats_distribution = self.boats_distribution.copy()
        new_board.boats_distribution[size] -= 1

        return new_board.reduce_board()

    def is_board_complete(self):
        """Checks if the board is a valid solution to the puzzle. For a
        Bimaru puzzle to be complete it needs to have all the constraints in
        the columns and rows satisfied, have zero incomplete cells to
        fill and be a valid board."""
        if self.is_invalid or self.remaining_cells_num != 0:
            return False

        for row, row_num in enumerate(self.rows_fixed_num):
            if self.rows_boat_pieces_num[row] != row_num or any(
                val in _incomp_vals for val in self.get_row(row)
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
        if state.board.is_invalid or state.board.remaining_cells_num == 0:
            return ()

        for next_size in reversed(range(4 + 1)):
            if next_size == 0:
                return ()
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
        return node.state.board.remaining_cells_num


if __name__ == "__main__":
    """Read the standard input file.
    Use a search technique to solve the instance.
    Retrieve the solution from the resulting node.
    Print to the standard output in the indicated format."""
    board = Board.parse_instance()
    bimaru = Bimaru(board)
    goal_node = breadth_first_tree_search(bimaru)
    print(goal_node.state.board)
