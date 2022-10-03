from pieces.piece import Piece
from pieces.piece_code import PieceCode
from util.utils import is_inside_board, to_code


class Knight(Piece):
    def __init__(self, x: int, y: int, cell_size: int, is_white: bool):
        super().__init__(x, y, cell_size, is_white)

    def get_fen_code(self):
        if self.is_white:
            return PieceCode.KNIGHT
        return f'{PieceCode.KNIGHT.lower()}'

    def get_valid_movements(self, board, cell_x, cell_y):
        movements = []
        
        x = cell_x + 1
        y = cell_y + 2
        if is_inside_board(board, x, y):
            cell = board[y][x]
            if cell is None or cell.is_white != self.is_white:
                movements.append(to_code(x, y))

        x = cell_x + 1
        y = cell_y - 2
        if is_inside_board(board, x, y):
            cell = board[y][x]
            if cell is None or cell.is_white != self.is_white:
                movements.append(to_code(x, y))

        x = cell_x - 1
        y = cell_y + 2
        if is_inside_board(board, x, y):
            cell = board[y][x]
            if cell is None or cell.is_white != self.is_white:
                movements.append(to_code(x, y))

        x = cell_x - 1
        y = cell_y - 2
        if is_inside_board(board, x, y):
            cell = board[y][x]
            if cell is None or cell.is_white != self.is_white:
                movements.append(to_code(x, y))

        x = cell_x + 2
        y = cell_y + 1
        if is_inside_board(board, x, y):
            cell = board[y][x]
            if cell is None or cell.is_white != self.is_white:
                movements.append(to_code(x, y))

        x = cell_x + 2
        y = cell_y - 1
        if is_inside_board(board, x, y):
            cell = board[y][x]
            if cell is None or cell.is_white != self.is_white:
                movements.append(to_code(x, y))

        x = cell_x - 2
        y = cell_y + 1
        if is_inside_board(board, x, y):
            cell = board[y][x]
            if cell is None or cell.is_white != self.is_white:
                movements.append(to_code(x, y))

        x = cell_x - 2
        y = cell_y - 1
        if is_inside_board(board, x, y):
            cell = board[y][x]
            if cell is None or cell.is_white != self.is_white:
                movements.append(to_code(x, y))

        return movements