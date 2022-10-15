from abc import ABC, abstractmethod
import pygame

from pieces.piece_code import PieceCode
from util.utils import remove_code_modifiers, to_code

class Piece(pygame.sprite.Sprite, ABC):
    def __init__(self, cell_size: int, is_white: bool):
        super().__init__()

        self.is_white = is_white
        
        image_path = self.get_source_images()[self.get_fen_code()]
        image = pygame.image.load(image_path).convert_alpha()
        self.image: pygame.surface.Surface = pygame.transform.scale(image, (cell_size, cell_size))
        self.was_moved = False

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

    def draw(self, screen: pygame.Surface, pos: 'tuple[int, int]'):
        screen.blit(self.image, pos)

    def is_valid_movement(self, board: 'list[list[Piece]]', cell: 'tuple[int, int]', new_cell_x: int, new_cell_y: int):
        movements = self.get_valid_movements(board, cell)
        movements_without_modifiers = map(remove_code_modifiers, movements)
        return to_code(new_cell_x, new_cell_y) in movements_without_modifiers

    def get_movement(self, board: 'list[list[Piece]]', cell: 'tuple[int, int]', clicked_cell: 'tuple[int, int]'):
        movements = self.get_valid_movements(board, cell)
        for movement in movements:
            code_without_modifier = remove_code_modifiers(movement)
            if code_without_modifier == to_code(clicked_cell[0], clicked_cell[1]):
                return movement
        return None

    def move(self, new_pos: 'tuple[int, int]'):
        self.x = new_pos[0]
        self.y = new_pos[1]

    def moved(self):
        self.was_moved = True

    @abstractmethod
    def get_fen_code(self) -> str:
        pass

    @abstractmethod
    def get_valid_movements(self, board: 'list[list[Piece]]', cell: 'tuple[int, int]') -> 'list[str]':
        pass

    @abstractmethod
    def score(self, cell: 'tuple[int, int]') -> float:
        pass