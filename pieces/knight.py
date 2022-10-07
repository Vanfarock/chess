from pieces.piece import Piece
from pieces.piece_code import PieceCode
from util.utils import is_inside_board, to_code


class Knight(Piece):
    def __init__(self, cell_size: int, is_white: bool):
        super().__init__(cell_size, is_white)

    def get_fen_code(self):
        if self.is_white:
            return PieceCode.KNIGHT
        return f'{PieceCode.KNIGHT.lower()}'

    def get_valid_movements(self, board: 'list[list[Piece]]', cell: 'tuple[int, int]'):
        movements = []

        directions = [
            (1 , 2),
            (1 ,-2),
            (-1, 2),
            (-1,-2),
            ( 2, 1),
            ( 2,-1),
            (-2, 1),
            (-2,-1),
        ]

        for direction in directions:
            x = cell[0] + direction[0]
            y = cell[1] + direction[1]

            if is_inside_board(board, x, y):
                piece = board[y][x]
                if piece is None:
                    movements.append(to_code(x, y))
                elif piece.is_white != self.is_white:
                    movements.append(to_code(x, y, will_eat=True))

        return movements