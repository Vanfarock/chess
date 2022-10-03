from pieces.piece import Piece
from pieces.piece_code import PieceCode
from util.utils import is_inside_board, to_code


class Pawn(Piece):
    def __init__(self, x: int, y: int, cell_size: int, is_white: bool):
        super().__init__(x, y, cell_size, is_white)

    def get_fen_code(self):
        if self.is_white:
            return PieceCode.PAWN
        return f'{PieceCode.PAWN.lower()}'

    def get_valid_movements(self, board, cell_x, cell_y):
        movements = []
  
        if self.is_white: forward_y = cell_y - 1
        else: forward_y = cell_y + 1

        if is_inside_board(board, cell_x, forward_y) and board[forward_y][cell_x] is None:
            movements.append(to_code(cell_x, forward_y))

        if is_inside_board(board, cell_x + 1, forward_y):
            right_diagonal = board[forward_y][cell_x + 1]
            if right_diagonal is not None and right_diagonal.is_white != self.is_white:
                movements.append(to_code(cell_x + 1, forward_y, will_eat=True))

        if is_inside_board(board, cell_x - 1, forward_y):
            left_diagonal = board[forward_y][cell_x - 1]
            if left_diagonal is not None and left_diagonal.is_white != self.is_white:
                movements.append(to_code(cell_x - 1, forward_y, will_eat=True))

        if not self._was_moved:
            if self.is_white: forward_y -= 1
            else: forward_y += 1

            if is_inside_board(board, cell_x, forward_y) and board[forward_y][cell_x] is None:
              movements.append(to_code(cell_x, forward_y))

        return movements