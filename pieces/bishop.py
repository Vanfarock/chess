from pieces.piece import Piece
from pieces.piece_code import PieceCode
from util.utils import is_inside_board, to_code


class Bishop(Piece):
    def __init__(self, cell_size: int, is_white: bool):
        super().__init__(cell_size, is_white)

    def get_fen_code(self) -> str:
        if self.is_white:
            return PieceCode.BISHOP
        return f'{PieceCode.BISHOP.lower()}'

    def get_valid_movements(self, board: 'list[list[Piece]]', cell: 'tuple[int, int]') -> 'list[str]':
        movements = []
        
        directions = [
            (1 , 1),
            (1 ,-1),
            (-1, 1),
            (-1,-1),
        ]

        for direction in directions:
            x = cell[0] + direction[0]
            y = cell[1] + direction[1]

            while is_inside_board(board, x, y):
                piece = board[y][x]
                if piece is not None:
                    if piece.is_white != self.is_white:
                        movements.append(to_code(x, y, will_eat=True))
                    break
                
                movements.append(to_code(x, y))
                x += direction[0]
                y += direction[1]

        return movements

    def score(self, cell: 'tuple[int, int]') -> float:
        position_table = [
            [-2, -1  , -1  , -1, -1, -1  , -1  , -2],
            [-1,  0  ,  0  ,  0,  0,  0  ,  0  , -1],
            [-1,  0  ,  0.5,  1,  1,  0.5,  0  , -1],
            [-1,  0.5,  0.5,  1,  1,  0.5,  0.5, -1],
            [-1,  0  ,  1  ,  1,  1,  1  ,  0  , -1],
            [-1,  1  ,  1  ,  1,  1,  1  ,  1  , -1],
            [-1,  0.5,  0  ,  0,  0,  0  ,  0.5, -1],
            [-2, -1  , -1  , -1, -1, -1  , -1  , -2],
        ]
        if not self.is_white:
            position_table = list(reversed(position_table))

        x, y = cell
        return 30 + position_table[y][x]