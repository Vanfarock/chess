from pieces.piece import Piece
from pieces.piece_code import PieceCode
from util.utils import is_inside_board, to_code


class Pawn(Piece):
    def __init__(self, cell_size: int, is_white: bool):
        super().__init__(cell_size, is_white)

    def get_fen_code(self):
        if self.is_white:
            return PieceCode.PAWN
        return f'{PieceCode.PAWN.lower()}'

    def get_valid_movements(self, board: 'list[list[Piece]]', cell: 'tuple[int, int]'):
        movements = []
  
        if self.is_white: delta = -1
        else: delta = 1

        x, y = cell
        if is_inside_board(board, x, y + delta) and board[y + delta][x] is None:
            movements.append(to_code(x, y + delta, will_promote=self.will_promote(board, y + delta)))
            if not self._was_moved:
                if is_inside_board(board, x, y + delta*2) and board[y + delta*2][x] is None:
                    movements.append(to_code(x, y + delta*2))

        if is_inside_board(board, x + 1, y + delta):
            right_diagonal = board[y + delta][x + 1]
            if right_diagonal is not None and right_diagonal.is_white != self.is_white:
                movements.append(to_code(x + 1, y + delta, will_eat=True, will_promote=self.will_promote(board, y + delta)))

        if is_inside_board(board, x - 1, y + delta):
            left_diagonal = board[y + delta][x - 1]
            if left_diagonal is not None and left_diagonal.is_white != self.is_white:
                movements.append(to_code(x - 1, y + delta, will_eat=True, will_promote=self.will_promote(board, y + delta)))


        return movements

    def will_promote(self, board: 'list[list[Piece]]', y: int) -> bool:
        return y == 0 or y == len(board) - 1