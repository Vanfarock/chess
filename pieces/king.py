from pieces.piece import Piece
from pieces.piece_code import PieceCode
from util.utils import is_inside_board, to_code

class King(Piece):
    def __init__(self, x: int, y: int, cell_size: int, white: bool):
        super().__init__(x, y, cell_size, white)

    def get_fen_code(self):
        if self.white:
            return PieceCode.KING
        return f'{PieceCode.KING.lower()}'

    def get_valid_movements(self, board, cell_x, cell_y):
        movements = []

        x = cell_x + 1
        y = cell_y + 1
        if is_inside_board(board, x, y):
            cell = board[y][x]
            if cell is None or cell.white != self.white:
                movements.append(to_code(x, y))

        x = cell_x - 1
        y = cell_y + 1
        if is_inside_board(board, x, y):
            cell = board[y][x]
            if cell is None or cell.white != self.white:
                movements.append(to_code(x, y))

        x = cell_x + 1
        y = cell_y - 1
        if is_inside_board(board, x, y):
            cell = board[y][x]
            if cell is None or cell.white != self.white:
                movements.append(to_code(x, y))

        x = cell_x - 1
        y = cell_y - 1
        if is_inside_board(board, x, y):
            cell = board[y][x]
            if cell is None or cell.white != self.white:
                movements.append(to_code(x, y))

        x = cell_x + 1
        y = cell_y
        if is_inside_board(board, x, y):
            cell = board[y][x]
            if cell is None or cell.white != self.white:
                movements.append(to_code(x, y))

        x = cell_x - 1
        y = cell_y
        if is_inside_board(board, x, y):
            cell = board[y][x]
            if cell is None or cell.white != self.white:
                movements.append(to_code(x, y))

        x = cell_x
        y = cell_y + 1
        if is_inside_board(board, x, y):
            cell = board[y][x]
            if cell is None or cell.white != self.white:
                movements.append(to_code(x, y))

        x = cell_x
        y = cell_y - 1
        if is_inside_board(board, x, y):
            cell = board[y][x]
            if cell is None or cell.white != self.white:
                movements.append(to_code(x, y))

        return movements
