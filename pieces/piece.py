from abc import ABC, abstractmethod
import pygame

from pieces.piece_code import PieceCode
from util.utils import remove_code_modifiers, to_code

class Piece(pygame.sprite.Sprite, ABC):
    def __init__(self, x: int, y: int, cell_size: int, is_white: bool):
        super().__init__()

        self.x, self.y = x, y
        self.is_white = is_white
        
        image_path = self.get_source_images()[self.get_fen_code()]
        image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(image, (cell_size, cell_size))
        self.rect = self.image.get_rect(topleft=(x, y))
        self._was_moved = False

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

    def is_valid_movement(self, board: list[list['Piece']], cell: tuple[int, int], new_cell_x: int, new_cell_y: int):
        movements = self.get_valid_movements(board, cell)
        movements_without_modifiers = map(remove_code_modifiers, movements)
        return to_code(new_cell_x, new_cell_y) in movements_without_modifiers

    def move(self, new_pos: tuple[int, int]):
        self.x = new_pos[0]
        self.y = new_pos[1]

    def moved(self):
        self._was_moved = True

    @abstractmethod
    def get_fen_code(self):
        pass

    @abstractmethod
    def get_valid_movements(self, board: list[list['Piece']], cell: tuple[int, int]):
        pass
