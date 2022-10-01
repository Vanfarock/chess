from pieces.piece import Piece
from pieces.piece_code import PieceCode


class Queen(Piece):
    def __init__(self, x: int, y: int, cell_size: int, white: bool):
        super().__init__(x, y, cell_size, white)

    def get_fen_code(self):
        if self.white:
            return PieceCode.QUEEN
        return f'{PieceCode.QUEEN.lower()}'

    def get_available_movements(self, board, cell_x, cell_y):
        pass
