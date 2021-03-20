from game import (
    TwoPlayerGameState,
)

from tournament import (
    StudentHeuristic,
)

import math


class MaxCellsKJ(StudentHeuristic):
    def get_name(self) -> str:
        return "MaxCellsKJ"

    def evaluate(self, state: TwoPlayerGameState) -> float:
        return self.possible_score(state)

    def possible_score(self, state: TwoPlayerGameState) -> int:
        """Method to get the "score" in the state. The more cells
        we have, the better.

        possible_score = max_score - #·cells occupied by us

        The smaller the number, the better.

        Args:
            state (TwoPlayerGameState): State of the actual game

        Returns:
            int: The "score" of the state
        """
        enemy_label = state.next_player.label
        max_possible_score = state.game.width*state.game.height
        board = state.board

        for cell in board:
            if board[cell] != enemy_label:
                max_possible_score -= 1

        return max_possible_score


class WeightedBoardKJ(StudentHeuristic):
    def __init__(self, name, evaluation_function):
        super().__init__(name, evaluation_function)

        # Attribute to check if the data is set
        self.info_set = False

        # Attributes related with the previous board
        self.previous_board = None
        # Each cell is stored with (label, value)
        self.previous_board_cells = {}

    def get_name(self) -> str:
        return "mysolution1"

    def evaluate(self, state: TwoPlayerGameState) -> float:
        if self.info_set is False:
            self.set_info(state.game.width, state.game.height, state)

        return self.get_weigthed_sum(state)

    def set_info(self, width, height, state):
        """Setter for the info

        Args:
            width (int): Width of the board
            height (int): Height of the board
            state (TwoPlayerGameState): State of the game
        """
        self.info_set = True
        self.width = width
        self.height = height
        self.enemy_label = state.next_player.label

        # Setting the attributes for the postion of each important cells
        self.corners = self.get_corners(self.width,
                                        self.height)

        self.diag_corners = self.get_contiguous_diagonal_to_corner(self.width,
                                                                   self.height)

        self.contiguous_corners = self.get_contiguous_to_corner(self.width,
                                                                self.height)

        self.powerful_cells = self.get_powefull_cells(self.width,
                                                      self.height)

    def get_weigthed_sum(self, state: TwoPlayerGameState) -> int:
        """Method to get the weighted sum of the board

        Args:
            state (TwoPlayerGameState): State of the game

        Returns:
            int: Sum
        """
        parent_board = state.parent.board
        if self.previous_board != parent_board:
            self.previous_board = parent_board

            # Getting the previous board sum
            self.store_cell_values(parent_board)

        # Getting the current board sum
        return self.get_current_sum(state.board)

    def get_current_sum(self, board):
        """Method to get the sum of a given board

        Args:
            board (dict): Dictionary with the occupied cells.

        Returns:
            int: Weighted sum of the entire board
        """
        sum_value = 0
        for cell in board:
            # If the cell changed from the previous
            # board, we compute a new value
            if cell in self.previous_board_cells:
                if board[cell] != self.previous_board_cells[cell][0]:
                    sum_value += self.get_cell_value(cell, board)
                else:
                    sum_value += self.previous_board_cells[cell][1]
            else:
                sum_value += self.get_cell_value(cell, board)
        return sum_value

    def store_cell_values(self, board):
        """Method to store the value of each cell. This method
        is designed to store the prevous board, so when we compute
        the new board we can get rid of the cells that didn't change

        Args:
            board (dict): Dictionary containing the occupied cells
        """
        cell_value = 0
        for cell in board:
            # Checking who occupied the cell.
            if cell in board:

                # Storing each cell value
                cell_value = self.get_cell_value(cell, board)

                # Each cell in the board is stored with:
                # (Player on that cell, value of the cell)
                self.previous_board_cells[cell] = (board[cell], cell_value)

    def get_cell_value(self, cell, board):
        """Method to get the cell value

        Args:
            cell (tuple): Postion of the cell
            board (dict): Board of the game

        Returns:
            int: Value of the cell
        """
        # If enemy -1, if us 1
        if self.enemy_label == board[cell]:
            occupied_by = -1
        else:
            occupied_by = 1

        # Corners have a value of 100
        if cell in self.corners:
            return 100*occupied_by

        # Cells diagonal next to the corners -50
        elif cell in self.diag_corners:
            return -50*occupied_by

        # Contiguous cells next to the corners
        elif cell in self.contiguous_corners:
            return -20*occupied_by

        # Cells that give an advantadge
        elif cell in self.powerful_cells:
            return 10*occupied_by

        # Cells that are in a wall and not in
        # the previous places
        elif cell[0] == self.width or cell[0] == 1\
                or cell[1] == self.height or cell[1] == 1:
            return 5*occupied_by

        # Internal cells
        else:
            return -occupied_by

    def get_corners(self, width, height):
        """Method to get the corners of the board

        Args:
            width (int): Width of the board
            height (int): Height of the board

        Returns:
            list: List with the corners
        """
        corners = [(1, 1), (1, height), (width, 1), (width, height)]
        return corners

    def get_contiguous_diagonal_to_corner(self, width, height):
        """Method to get the contiguous cells of each corner that
        are positioned in the diagonal of the board.
        .
        .
        .
        A B
        X A . . .

        We only take B

        Args:
            width (int): Width of the game
            height ([type]): Height of the game

        Returns:
            list: List containing the contiguous cells of the corners
            in the diagonal.
        """
        cont_diagonal_to_corner = []

        # Left down
        cont_diagonal_to_corner.append((1+1, 1+1))

        # Left up
        cont_diagonal_to_corner.append((1+1, height-1))

        # Right down
        cont_diagonal_to_corner.append((width-1, 1+1))

        # Right up
        cont_diagonal_to_corner.append((width-1, height-1))

        return cont_diagonal_to_corner

    def get_contiguous_to_corner(self, width, height):
        """Method to get the contiguous places of the corners.
        We only focuse on the vertical and horizontal contigous.
        .
        .
        .
        A B
        X A . . .

        We don't take into account B, only A's

        Args:
            width (int): Width of the board
            height (int): Height of the board

        Returns:
            List: List containing the contigous cells.
        """
        contiguous_to_corners = []

        # Left down corner
        contiguous_to_corners.append((1, 1+1))
        contiguous_to_corners.append((1+1, 1))

        # Left up corner
        contiguous_to_corners.append((1, height-1))
        contiguous_to_corners.append((1+1, height))

        # Right down corner
        contiguous_to_corners.append((width, 1+1))
        contiguous_to_corners.append((width-1, 1))

        # Right up corner
        contiguous_to_corners.append((width, height-1))
        contiguous_to_corners.append((width-1, height))

        return contiguous_to_corners

    def get_powefull_cells(self, width, height):
        """Method to get a powefull cell. Powefull cells
        are the ones that give us the chance of getting
        the corners.
        .
        .
        .
        A
        B C
        X B A . . .

        A's are powefull cells because if the other player
        takes B then we can take the corner.

        Args:
            width (int): Width of the board
            height (int): Height of the board

        Returns:
            list: List with the positions of the powerfull
            cells.
        """
        powerful_cells = []

        # Left down
        powerful_cells.append((1+2, 1))
        powerful_cells.append((1, 1+2))

        # Left up
        powerful_cells.append((1+2, height))
        powerful_cells.append((1, height-2))

        # Right down
        powerful_cells.append((width-2, 1))
        powerful_cells.append((width, 1+2))

        # Right up
        powerful_cells.append((width-2, height))
        powerful_cells.append((width, height-2))

        return powerful_cells
