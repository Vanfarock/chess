from pieces.piece import Piece
from pieces.piece_code import PieceCode
from util.utils import is_inside_board, to_code


class Queen(Piece):
    def __init__(self, x: int, y: int, cell_size: int, is_white: bool):
        super().__init__(x, y, cell_size, is_white)

    def get_fen_code(self):
        if self.is_white:
            return PieceCode.QUEEN
        return f'{PieceCode.QUEEN.lower()}'

    def get_valid_movements(self, board, cell_x, cell_y):
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
            x = cell_x + direction[0]
            y = cell_y + direction[1]

            while is_inside_board(board, x, y):
                cell = board[y][x]
                if cell is not None:
                    if cell.is_white != self.is_white:
                        movements.append(to_code(x, y, will_eat=True))
                    break
                
                movements.append(to_code(x, y))
                x += direction[0]
                y += direction[1]

        return movements