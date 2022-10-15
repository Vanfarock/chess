from pieces.piece import Piece
from pieces.piece_code import PieceCode
from util.utils import is_inside_board, is_rookie, to_code

class King(Piece):
    def __init__(self, cell_size: int, is_white: bool):
        super().__init__(cell_size, is_white)

    def get_fen_code(self) -> str:
        if self.is_white:
            return PieceCode.KING
        return f'{PieceCode.KING.lower()}'

    def get_valid_movements(self, board: 'list[list[Piece]]', cell: 'tuple[int, int]') -> 'list[str]':
        movements = []

        directions = [
            (1 , 0),
            (-1, 0),
            (0 , 1),
            (0 ,-1),
            (1 , 1),
            (1 ,-1),
            (-1, 1),
            (-1,-1),
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

        if not self.was_moved:
            x = cell[0] + 1
            y = cell[1]
            while True:
                if not is_inside_board(board, x, y):
                    break
                piece = board[y][x]
                if piece is not None:
                    if is_rookie(piece) and not piece.was_moved:
                        movements.append(to_code(cell[0] + 2, y, will_castle=True))
                    break
                x += 1

            x = cell[0] - 1
            y = cell[1]
            while True:
                if not is_inside_board(board, x, y):
                    break
                piece = board[y][x]
                if piece is not None:
                    if is_rookie(piece) and not piece.was_moved:
                        movements.append(to_code(cell[0] - 2, y, will_castle=True))
                    break
                x -= 1

        return movements

    def score(self, cell: 'tuple[int, int]') -> float:
        position_table = [
            [-3, -4, -4, -5, -5, -4, -4, -3],
            [-3, -4, -4, -5, -5, -4, -4, -3],
            [-3, -4, -4, -5, -5, -4, -4, -3],
            [-3, -4, -4, -5, -5, -4, -4, -3],
            [-2, -3, -3, -4, -4, -3, -3, -2],
            [-1, -2, -2, -2, -2, -2, -2, -1],
            [ 2,  2,  0,  0,  0,  0,  2,  2],
            [ 2,  3,  1,  0,  0,  1,  3,  2],
        ]
        if not self.is_white:
            position_table = list(reversed(position_table))

        x, y = cell
        return 10000 + position_table[y][x]