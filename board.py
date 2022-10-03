import pygame
from util.colors import Colors
from pieces.piece import *
from pieces.piece_factory import PieceFactory
from util.utils import from_code, is_inside_board

class Board:
    def __init__(self, start_x: int, cell_size: int):
        self.cell_size = cell_size
        self.start_x = start_x
        self.black_color = Colors.ORANGE
        self.highlighted_black_color = Colors.BLUE
        self.is_white_color = Colors.BEIGE
        self.highlighted_white_color = Colors.GREEN
        self.board: list[list[Piece]] = self.setup_board('rnbkqbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR')
        
        self.hanging_piece: Piece = None
        self.hanging_piece_pos = None

        self.clicked_piece: Piece = None

        self.is_white_turn = True

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

        if self.clicked_left_mouse_button():
            self.handle_mouse_click(cell_x, cell_y)
        elif self.hanging_piece is not None:
            self.handle_mouse_release(cell_x, cell_y)
    
    def clicked_left_mouse_button(self):
        return pygame.mouse.get_pressed()[0]

    def handle_mouse_click(self, cell_x: int, cell_y: int):
        if self.clicked_piece is not None:
            clicked_cell_x, clicked_cell_y = self.get_cell(self.clicked_piece.x, self.clicked_piece.y)
            if self.clicked_piece.is_valid_movement(self.board, clicked_cell_x, clicked_cell_y, cell_x, cell_y):
                self.move_piece(self.clicked_piece, clicked_cell_x, clicked_cell_y, cell_x, cell_y)
            self.clicked_piece = None
            return

        piece = self.hanging_piece or self.board[cell_y][cell_x]
        if piece is None:
            self.clicked_piece = None
            return

        if piece.is_white != self.is_white_turn:
            return

        self.clicked_piece = piece

        mouse_movement = pygame.mouse.get_rel()
        if self.hanging_piece is None:
            self.hanging_piece = piece
            self.hanging_piece_pos = (cell_x, cell_y)
            return

        self.clicked_piece = None
        piece.x += mouse_movement[0]
        piece.y += mouse_movement[1]

    def handle_mouse_release(self, cell_x: int, cell_y: int):
        old_cell_x, old_cell_y = self.hanging_piece_pos
        if self.hanging_piece.is_valid_movement(self.board, old_cell_x, old_cell_y, cell_x, cell_y):
            self.move_piece(self.hanging_piece, old_cell_x, old_cell_y, cell_x, cell_y)
        else:
            old_x, old_y = self.cell_size * old_cell_x + self.start_x, self.cell_size * old_cell_y
            self.hanging_piece.x = old_x
            self.hanging_piece.y = old_y

        self.hanging_piece =  None
        self.hanging_piece_pos = None

    def move_piece(self, piece: Piece, old_cell_x: int, old_cell_y: int, cell_x: int, cell_y: int):
        if piece.is_white != self.is_white_turn:
            return

        self.board[old_cell_y][old_cell_x] = None

        new_x, new_y = self.cell_size * cell_x + self.start_x, self.cell_size * cell_y                
        piece.x = new_x
        piece.y = new_y
        self.board[cell_y][cell_x] = piece
        self.is_white_turn = not self.is_white_turn

    def get_cell(self, x: int, y: int):
        correct_x = x - self.start_x
        cell_x = round((correct_x - correct_x % self.cell_size) / self.cell_size)
        cell_y = round((y - y % self.cell_size) / self.cell_size)
        return (cell_x, cell_y)

    def draw(self, screen: pygame.Surface):
        self.draw_board(screen)
        self.draw_pieces(screen)
        
    def draw_board(self, screen: pygame.Surface):
        for i in range(8):
            for j in range(8):
                if (i + j) % 2 == 0: color = self.is_white_color
                else: color = self.black_color
                
                x, y = self.cell_size * j + self.start_x, self.cell_size * i
                pygame.draw.rect(
                    screen,
                    color, 
                    (x, y, self.cell_size, self.cell_size))

    def draw_pieces(self, screen: pygame.Surface):
        self.draw_piece_valid_movements(screen)

        for row in self.board:
            for piece in row:
                if piece is not None:
                    piece.draw(screen)

    def draw_piece_valid_movements(self, screen: pygame.Surface):
        if self.clicked_piece is None:
            return

        cell_x, cell_y = self.get_cell(self.clicked_piece.x, self.clicked_piece.y)
        movements = self.clicked_piece.get_valid_movements(self.board, cell_x, cell_y)
        for movement in movements:
            movement_cell_x, movement_cell_y = from_code(movement)
            
            if (movement_cell_x + movement_cell_y) % 2 == 0: color = self.highlighted_white_color
            else: color = self.highlighted_black_color

            x = movement_cell_x * self.cell_size + self.start_x
            y = movement_cell_y * self.cell_size
            pygame.draw.rect(
                screen,
                color, 
                (x, y, self.cell_size, self.cell_size))
