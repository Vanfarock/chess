import pygame
from util.colors import Colors
from pieces.piece import *
from pieces.piece_factory import PieceFactory
from util.utils import is_inside_board

class Board:
    def __init__(self, start_x: int, cell_size: int):
        self.cell_size = cell_size
        self.start_x = start_x
        self.black_color = Colors.ORANGE
        self.white_color = Colors.BEIGE
        self.board = self.setup_board('rnbkqbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR')
        
        self.hanging_piece: Piece = None
        self.hanging_piece_pos = None

    def setup_board(self, fen_code: str):
        board = []
        for i, row in enumerate(fen_code.split('/')):
            board_row = []
            for j, item in enumerate(row):
                if item.isdigit():
                    board_row.extend([None] * int(item))
                else:
                    x, y = self.cell_size * j + self.start_x, self.cell_size * i
                    board_row.append(PieceFactory.create(item, x, y, self.cell_size))
            board.append(board_row)
        return board

    def handle_events(self, event: pygame.event.Event):
        self.handle_mouse()

    def handle_mouse(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        cell_x, cell_y = self.get_cell(mouse_x, mouse_y)

        if not is_inside_board(self.board, cell_x, cell_y):
            return

        if pygame.mouse.get_pressed()[0]:
            piece = self.hanging_piece or self.board[cell_y][cell_x]
            if piece is None:
                return

            mouse_movement = pygame.mouse.get_rel()
            if self.hanging_piece is None:
                self.hanging_piece = piece
                self.hanging_piece_pos = (cell_x, cell_y)
                return

            piece.x += mouse_movement[0]
            piece.y += mouse_movement[1]
        elif self.hanging_piece is not None:
            old_cell_x, old_cell_y = self.hanging_piece_pos
            if self.hanging_piece.is_valid_movement(self.board, old_cell_x, old_cell_y, cell_x, cell_y):
                self.board[old_cell_y][old_cell_x] = None

                new_x, new_y = self.cell_size * cell_x + self.start_x, self.cell_size * cell_y                
                self.hanging_piece.x = new_x
                self.hanging_piece.y = new_y
                self.board[cell_y][cell_x] = self.hanging_piece
            else:
                old_x, old_y = self.cell_size * old_cell_x + self.start_x, self.cell_size * old_cell_y
                self.hanging_piece.x = old_x
                self.hanging_piece.y = old_y

            self.hanging_piece =  None
            self.hanging_piece_pos = None
            

    def get_cell(self, x: int, y: int):
        cell_x = round((x - self.start_x - x % self.cell_size) / self.cell_size)
        cell_y = round((y - y % self.cell_size) / self.cell_size)
        return (cell_x, cell_y)

    def draw(self, screen: pygame.Surface):
        self.draw_board(screen)
        self.draw_pieces(screen)
        
    def draw_board(self, screen: pygame.Surface):
        for i in range(8):
            for j in range(8):
                if (i + j) % 2 == 0:
                    color = self.white_color
                else:
                    color = self.black_color
                
                x, y = self.cell_size * j + self.start_x, self.cell_size * i
                pygame.draw.rect(
                    screen,
                    color, 
                    (x, y, self.cell_size, self.cell_size))

    def draw_pieces(self, screen: pygame.Surface):
        for row in self.board:
            for piece in row:
                if piece is not None:
                    piece.draw(screen)
