import pygame
from colors import Colors
from piece import *

class Board:
    def __init__(self, start_x: int, cell_size: int):
        self.cell_size = cell_size
        self.start_x = start_x
        self.black_color = Colors.ORANGE
        self.white_color = Colors.BEIGE
        self.board = self.setup_board('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR')
        
        self.hanging_piece = None
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

        if not self.is_inside_board(cell_x, cell_y):
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
            if self.is_valid_movement(cell_x, cell_y):
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

    def is_inside_board(self, x, y):
        if x < 0 or y < 0:
            return False

        if x >= len(self.board[0]) or y >= len(self.board):
            return False

        return True

    def is_valid_movement(self, x, y):
        old_cell_x, old_cell_y = self.hanging_piece_pos
        movements = self.hanging_piece.get_available_movements(self.board, old_cell_x, old_cell_y)
        return self.to_code(x, y) in movements

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

    def from_code(self, code: str):
        x = ord(code[0]) - 96
        y = int(code[1])
        return (x, y)

    def to_code(self, x: int, y: int):
        return (chr(x + 97), 8 - y)
        