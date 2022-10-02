from pieces.piece import Piece
from pieces.piece_code import PieceCode
from util.utils import is_inside_board, to_code


class Rookie(Piece):
    def __init__(self, x: int, y: int, cell_size: int, white: bool):
        super().__init__(x, y, cell_size, white)

    def get_fen_code(self):
        if self.white:
            return PieceCode.ROOKIE
        return f'{PieceCode.ROOKIE.lower()}'

    def get_valid_movements(self, board, cell_x, cell_y):
        movements = []
        
        x = cell_x + 1
        while is_inside_board(board, x, cell_y):
            cell = board[cell_y][x]
            if cell is not None:
                if cell.white != self.white:
                    movements.append(to_code(x, cell_y))
                break
            
            movements.append(to_code(x, cell_y))
            x += 1

        x = cell_x - 1
        while is_inside_board(board, x, cell_y):
            cell = board[cell_y][x]
            if cell is not None:
                if cell.white != self.white:
                    movements.append(to_code(x, cell_y))
                break
            
            movements.append(to_code(x, cell_y))
            x -= 1

        y = cell_y + 1
        while is_inside_board(board, cell_x, y):
            cell = board[y][cell_x]
            if cell is not None:
                if cell.white != self.white:
                    movements.append(to_code(cell_x, y))
                break
            
            movements.append(to_code(cell_x, y))
            y += 1

        y = cell_y - 1
        while is_inside_board(board, cell_x, y):
            cell = board[y][cell_x]
            if cell is not None:
                if cell.white != self.white:
                    movements.append(to_code(cell_x, y))
                break
            
            movements.append(to_code(cell_x, y))
            y -= 1

        return movements
