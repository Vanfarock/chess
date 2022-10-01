from abc import ABC, abstractmethod
import pygame

class PieceCode:
    PAWN = 'P'
    ROOKIE = 'R'
    KNIGHT = 'N'
    BISHOP = 'B'
    QUEEN = 'Q'
    KING = 'K'

class PieceFactory:
    def create(fen_code: str, x: int, y: int, cell_size: int):
        return {
            PieceCode.PAWN: Pawn(x, y, cell_size, True),
            PieceCode.ROOKIE: Rookie(x, y, cell_size, True),
            PieceCode.KNIGHT: Knight(x, y, cell_size, True),
            PieceCode.BISHOP: Bishop(x, y, cell_size, True),
            PieceCode.QUEEN: Queen(x, y, cell_size, True),
            PieceCode.KING: King(x, y, cell_size, True),
            f'{PieceCode.PAWN.lower()}': Pawn(x, y, cell_size, False),
            f'{PieceCode.ROOKIE.lower()}': Rookie(x, y, cell_size, False),
            f'{PieceCode.KNIGHT.lower()}': Knight(x, y, cell_size, False),
            f'{PieceCode.BISHOP.lower()}': Bishop(x, y, cell_size, False),
            f'{PieceCode.QUEEN.lower()}': Queen(x, y, cell_size, False),
            f'{PieceCode.KING.lower()}': King(x, y, cell_size, False),
        }[fen_code]

class Piece(pygame.sprite.Sprite, ABC):
    def __init__(self, x: int, y: int, cell_size: int, white: bool):
        super().__init__()

        self.x, self.y = x, y
        self.white = white
        
        image_path = self.get_source_images()[self.get_fen_code()]
        image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(image, (cell_size, cell_size))
        self.rect = self.image.get_rect(topleft=(x, y))

    def get_source_images(self):
        return {
            PieceCode.PAWN: 'assets/pawn_white.png',
            PieceCode.ROOKIE: 'assets/rookie_white.png',
            PieceCode.KNIGHT: 'assets/knight_white.png',
            PieceCode.BISHOP: 'assets/bishop_white.png',
            PieceCode.QUEEN: 'assets/queen_white.png',
            PieceCode.KING: 'assets/king_white.png',
            f'{PieceCode.PAWN.lower()}': 'assets/pawn_black.png',
            f'{PieceCode.ROOKIE.lower()}': 'assets/rookie_black.png',
            f'{PieceCode.KNIGHT.lower()}': 'assets/knight_black.png',
            f'{PieceCode.BISHOP.lower()}': 'assets/bishop_black.png',
            f'{PieceCode.QUEEN.lower()}': 'assets/queen_black.png',
            f'{PieceCode.KING.lower()}': 'assets/king_black.png',
        }

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, (self.x, self.y))

    def is_inside_board(self, board, cell_x, cell_y):
        return not (cell_x < 0 or cell_y < 0 or cell_x >= len(board[0]) or cell_y >= len(board))

    def from_code(self, code: str):
        x = ord(code[0]) - 96
        y = int(code[1])
        return (x, y)

    def to_code(self, x: int, y: int):
        return (chr(x + 97), 8 - y)

    @abstractmethod
    def get_fen_code(self):
        pass

    @abstractmethod
    def get_available_movements(self, board, cell_x, cell_y):
        pass

class Pawn(Piece):
    def __init__(self, x: int, y: int, cell_size: int, white: bool):
        super().__init__(x, y, cell_size, white)

    def get_fen_code(self):
        if self.white:
            return PieceCode.PAWN
        return f'{PieceCode.PAWN.lower()}'

    def get_available_movements(self, board, cell_x, cell_y):
        movements = []
        
        if self.white: forward_y = cell_y - 1
        else: forward_y = cell_y + 1

        if self.is_inside_board(board, cell_x, forward_y) and board[forward_y][cell_x] is None:
            movements.append(self.to_code(cell_x, forward_y))

        if self.is_inside_board(board, cell_x + 1, forward_y):
            right_diagonal = board[forward_y][cell_x + 1]
            if right_diagonal is not None and right_diagonal.white != self.white:
                movements.append(self.to_code(cell_x + 1, forward_y))

        if self.is_inside_board(board, cell_x - 1, forward_y):
            left_diagonal = board[forward_y][cell_x - 1]
            if left_diagonal is not None and left_diagonal.white != self.white:
                movements.append(self.to_code(cell_x - 1, forward_y))

        return movements

class Rookie(Piece):
    def __init__(self, x: int, y: int, cell_size: int, white: bool):
        super().__init__(x, y, cell_size, white)

    def get_fen_code(self):
        if self.white:
            return PieceCode.ROOKIE
        return f'{PieceCode.ROOKIE.lower()}'

    def get_available_movements(self, board, cell_x, cell_y):
        pass

class Knight(Piece):
    def __init__(self, x: int, y: int, cell_size: int, white: bool):
        super().__init__(x, y, cell_size, white)

    def get_fen_code(self):
        if self.white:
            return PieceCode.KNIGHT
        return f'{PieceCode.KNIGHT.lower()}'

    def get_available_movements(self, board, cell_x, cell_y):
        pass

class Bishop(Piece):
    def __init__(self, x: int, y: int, cell_size: int, white: bool):
        super().__init__(x, y, cell_size, white)

    def get_fen_code(self):
        if self.white:
            return PieceCode.BISHOP
        return f'{PieceCode.BISHOP.lower()}'

    def get_available_movements(self, board, cell_x, cell_y):
        pass

class Queen(Piece):
    def __init__(self, x: int, y: int, cell_size: int, white: bool):
        super().__init__(x, y, cell_size, white)

    def get_fen_code(self):
        if self.white:
            return PieceCode.QUEEN
        return f'{PieceCode.QUEEN.lower()}'

    def get_available_movements(self, board, cell_x, cell_y):
        pass

class King(Piece):
    def __init__(self, x: int, y: int, cell_size: int, white: bool):
        super().__init__(x, y, cell_size, white)

    def get_fen_code(self):
        if self.white:
            return PieceCode.KING
        return f'{PieceCode.KING.lower()}'

    def get_available_movements(self, board, cell_x, cell_y):
        pass