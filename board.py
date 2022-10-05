import pygame
from util.colors import Colors
from pieces.piece import *
from pieces.piece_factory import PieceFactory
from util.utils import from_code, is_inside_board, is_king

class Board:
    def __init__(self, start_x: int, cell_size: int):
        self.cell_size = cell_size
        self.start_x = start_x
        self.black_color = Colors.ORANGE
        self.highlighted_black_color = Colors.BLUE
        self.white_color = Colors.BEIGE
        self.highlighted_white_color = Colors.BLUE
        self.eat_color = Colors.RED
        self.summary_color = Colors.WHITE
        self.board: list[list[Piece]] = self.setup_board('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR')

        # Stalemate test
        # self.board: list[list[Piece]] = self.setup_board('2Q2bnr/4p1pq/5pkr/7p/2P4P/8/PP1PPPP1/RNB1KBNR')
        
        self.hanging_piece: Piece = None
        self.hanging_piece_pos = None

        self.clicked_piece: Piece = None

        self.is_white_turn = True
        self.is_checked = None
        self.eaten_pieces: list[Piece] = []
        self.checkmate = False
        self.stalemate = False

    def setup_board(self, fen_code: str):
        board = []
        for i, row in enumerate(fen_code.split('/')):
            board_row = []
            offset = 0
            for j, item in enumerate(row):
                if item.isdigit():
                    offset += int(item) - 1
                    board_row.extend([None] * int(item))
                else:
                    x, y = self.cell_size * (j + offset) + self.start_x, self.cell_size * i
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
        self.handle_move_by_click(cell_x, cell_y)

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

    def handle_move_by_click(self, cell_x: int, cell_y: int):
        if self.clicked_piece is None:
            return
        clicked_cell_x, clicked_cell_y = self.get_cell(self.clicked_piece.x, self.clicked_piece.y)
        if self.clicked_piece.is_valid_movement(self.board, clicked_cell_x, clicked_cell_y, cell_x, cell_y):
            self.move_piece(self.clicked_piece, clicked_cell_x, clicked_cell_y, cell_x, cell_y)
        self.clicked_piece = None

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
        eaten_piece = self.board[cell_y][cell_x]
        self.board[cell_y][cell_x] = piece
        
        new_x, new_y = self.cell_size * cell_x + self.start_x, self.cell_size * cell_y                
        piece.x, piece.y = new_x, new_y
        
        self.is_checked = self.player_is_checked(self.board, self.is_white_turn)
        if self.is_checked:
            if eaten_piece is not None:
                self.eaten_pieces.append(eaten_piece)

            self.board[old_cell_y][old_cell_x] = piece
            self.board[cell_y][cell_x] = eaten_piece
            old_x, old_y = self.cell_size * old_cell_x + self.start_x, self.cell_size * old_cell_y
            piece.x, piece.y = old_x, old_y
        else:
            self.is_white_turn = not self.is_white_turn
            if eaten_piece is not None:
                self.eaten_pieces.append(eaten_piece)

            piece.moved()
            self.check_end_game()

    def player_is_checked(self, board: list[list[Piece]], is_white: bool):
        king_cell = self.get_king_cell(board, is_white)
        if king_cell is None:
            return False

        for piece in self.get_pieces(board, not is_white):
            cell_x, cell_y = self.get_cell(piece.x, piece.y)
            movements = piece.get_valid_movements(board, cell_x, cell_y)
            movements = list(map(remove_code_modifiers, movements))
            if to_code(king_cell[0], king_cell[1]) in movements:
                return True
        return False

    def check_end_game(self):
        valid_movements = 0
        is_checkmate = self.player_is_checked(self.board, self.is_white_turn)
        for piece in self.get_pieces(self.board, self.is_white_turn):
            original_x, original_y = piece.x, piece.y
            cell_x, cell_y = self.get_cell(original_x, original_y)
            movements = piece.get_valid_movements(self.board, cell_x, cell_y)

            for movement in movements:
                (test_x, test_y), _, _ = from_code(movement)
                test_piece = self.board[test_y][test_x]
                
                self.board[cell_y][cell_x] = None
                self.board[test_y][test_x] = piece

                piece.x = self.cell_size * test_x + self.start_x
                piece.y = self.cell_size * test_y

                is_checked = self.player_is_checked(self.board, self.is_white_turn)
                valid_movements += int(not is_checked)
                is_checkmate = is_checkmate and is_checked
                self.board[test_y][test_x] = test_piece
            
            self.board[cell_y][cell_x] = piece
            piece.x = original_x
            piece.y = original_y

        self.stalemate = valid_movements == 0
        self.checkmate = is_checkmate

    def get_pieces(self, board: list[list[Piece]], is_white: bool) -> list[Piece]:
        pieces = []
        for row in board:
            for piece in row:
                if piece is not None and piece.is_white == is_white:
                    pieces.append(piece)
        return pieces

    def get_king_cell(self, board: list[list[Piece]], is_white: bool):
        for row in board:
            for piece in row:
                if piece is not None and piece.is_white == is_white and is_king(piece):
                    return self.get_cell(piece.x, piece.y)
        return None

    def get_cell(self, x: int, y: int):
        correct_x = x - self.start_x
        cell_x = round((correct_x - correct_x % self.cell_size) / self.cell_size)
        cell_y = round((y - y % self.cell_size) / self.cell_size)
        return (cell_x, cell_y)

    def draw(self, screen: pygame.Surface):
        self.draw_board(screen)
        self.draw_pieces(screen)
        self.draw_summary(screen)
        self.draw_eaten_pieces(screen)
        
    def draw_board(self, screen: pygame.Surface):
        for i in range(8):
            for j in range(8):
                if (i + j) % 2 == 0: color = self.white_color
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
            (movement_cell_x, movement_cell_y), will_eat, will_check = from_code(movement)
            
            if (movement_cell_x + movement_cell_y) % 2 == 0: color = self.highlighted_white_color
            else: color = self.highlighted_black_color

            if will_eat:
                color = self.eat_color

            x = movement_cell_x * self.cell_size + self.start_x
            y = movement_cell_y * self.cell_size
            pygame.draw.rect(
                screen,
                color, 
                (x, y, self.cell_size, self.cell_size))

    def draw_summary(self, screen: pygame.Surface):
        width, height = screen.get_width(), screen.get_height()

        pygame.draw.rect(
            screen,
            self.summary_color,
            (0, 0, self.start_x, height))

        pygame.draw.rect(
            screen,
            self.summary_color,
            (width - self.start_x, 0, self.start_x, height))

        self.draw_eaten_pieces(screen)

    def draw_eaten_pieces(self, screen: pygame.Surface):
        width, height = screen.get_width(), screen.get_height()

        white_x, white_y = 0, 0
        black_x, black_y = width - self.cell_size, height - self.cell_size
        for piece in self.eaten_pieces:
            if piece.is_white:
                piece.x = white_x
                piece.y = white_y
                white_y += self.cell_size
                if white_y + self.cell_size > height:
                    white_y = 0
                    white_x += self.cell_size
                piece.draw(screen)
            else:
                piece.x = black_x
                piece.y = black_y
                black_y -= self.cell_size
                if black_y < 0:
                    black_y = height - self.cell_size
                    black_x -= self.cell_size
                piece.draw(screen)
