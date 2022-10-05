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
  
        if self.is_white: delta = -1
        else: delta = 1

        if is_inside_board(board, cell_x, cell_y + delta) and board[cell_y + delta][cell_x] is None:
            movements.append(to_code(cell_x, cell_y + delta))
            if not self._was_moved:
                if is_inside_board(board, cell_x, cell_y + delta*2) and board[cell_y + delta*2][cell_x] is None:
                    movements.append(to_code(cell_x, cell_y + delta*2))

        if is_inside_board(board, cell_x + 1, cell_y + delta):
            right_diagonal = board[cell_y + delta][cell_x + 1]
            if right_diagonal is not None and right_diagonal.is_white != self.is_white:
                movements.append(to_code(cell_x + 1, cell_y + delta, will_eat=True))

        if is_inside_board(board, cell_x - 1, cell_y + delta):
            left_diagonal = board[cell_y + delta][cell_x - 1]
            if left_diagonal is not None and left_diagonal.is_white != self.is_white:
                movements.append(to_code(cell_x - 1, cell_y + delta, will_eat=True))


        return movements