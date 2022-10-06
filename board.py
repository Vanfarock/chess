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
        self.__internal_board: list[list[Piece]] = self.setup_board('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR')
        # Stalemate test
        # self.__internal_board: list[list[Piece]] = self.setup_board('2Q2bnr/4p1pq/5pkr/7p/2P4P/8/PP1PPPP1/RNB1KBNR')
        
        self.hanging_piece: Piece = None
        self.hanging_piece_pos: tuple[int, int] = None

        self.clicked_piece: Piece = None

        self.is_white_turn: bool = True
        self.is_checked: bool = False
        self.__eaten_pieces: list[Piece] = []
        self.checkmate: bool = False
        self.stalemate: bool = False

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

    def get(self):
        return self.__internal_board

    def at(self, cell: tuple[int, int]) -> Piece:
        x, y = cell
        if self.is_inside(x, y):
            return self.__internal_board[y][x]
        return None

    def set_piece_at(self, piece: Piece, cell: tuple[int, int]):
        x, y = cell
        if self.is_inside(x, y):
            self.__internal_board[y][x] = piece
            piece.move(self.get_screen_position(cell))

    def revert_eaten_piece(self, piece: Piece, cell : tuple[int, int]):
        if piece is None:
            return

        eaten_piece = self.__eaten_pieces.pop()
        if eaten_piece != piece:
            self.__eaten_pieces.append(eaten_piece)
        else:
            self.set_piece_at(piece, cell)

    def get_cell(self, x: int, y: int):
        correct_x = x - self.start_x
        cell_x = round((correct_x - correct_x % self.cell_size) / self.cell_size)
        cell_y = round((y - y % self.cell_size) / self.cell_size)
        return (cell_x, cell_y)

    def is_inside(self, x: int, y: int) -> bool:
        return is_inside_board(self.__internal_board, x, y)

    def get_screen_position(self, cell: tuple[int, int]) -> tuple[int, int]:
        x, y = cell
        return self.cell_size * x + self.start_x, self.cell_size * y

    def try_move_piece(self, piece: Piece, is_white_turn: bool, from_x: int, from_y: int, to_x: int, to_y: int):
        eaten_piece = self.__move_piece(piece, from_x, from_y, to_x, to_y)

        self.is_checked = self.player_is_checked(is_white_turn)
        if self.is_checked:
            return self.reject_move_piece(piece, eaten_piece, (from_x, from_y), (to_x, to_y))
        else:
            return self.confirm_move_piece(eaten_piece)

    def __move_piece(self, piece: Piece, from_x: int, from_y: int, to_x: int, to_y: int):
        self.__internal_board[from_y][from_x] = None
        eaten_piece = self.__internal_board[to_y][to_x]
        self.__internal_board[to_y][to_x] = piece
        self.set_piece_at(piece, (to_x, to_y))
        return eaten_piece

    def reject_move_piece(self, piece: Piece, eaten_piece: Piece, from_cell: tuple[int, int], to_cell: tuple[int, int]):
        if eaten_piece is not None:
            self.__eaten_pieces.append(eaten_piece)

        from_x, from_y = from_cell
        to_x, to_y = to_cell
        self.__internal_board[from_y][from_x] = piece
        self.__internal_board[to_y][to_x] = eaten_piece
        piece.x, piece.y = self.get_screen_position(from_cell)
        return False

    def confirm_move_piece(self, eaten_piece: Piece):
        if eaten_piece is not None:
            self.__eaten_pieces.append(eaten_piece)
        return True

    def player_is_checked(self, is_white: bool):
        king_cell = self.get_king_cell(self.__internal_board, is_white)
        if king_cell is None:
            return False

        for piece in self.get_pieces(not is_white):
            cell = self.get_cell(piece.x, piece.y)
            movements = piece.get_valid_movements(self.__internal_board, cell)
            movements = list(map(remove_code_modifiers, movements))
            if to_code(king_cell[0], king_cell[1]) in movements:
                return True
        return False

    def get_pieces(self, is_white: bool) -> list[Piece]:
        pieces = []
        for row in self.__internal_board:
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

    def check_game_result(self, is_white_turn: bool):
        valid_movements = 0
        is_checkmate = self.player_is_checked(is_white_turn)
        
        original_board = self.__internal_board
        original_eaten_pieces = self.__eaten_pieces
        self.__internal_board = original_board.copy()
        self.__eaten_pieces = original_eaten_pieces

        for piece in self.get_pieces(is_white_turn):
            cell_x, cell_y = self.get_cell(piece.x, piece.y)
            movements = piece.get_valid_movements(self.__internal_board, (cell_x, cell_y))

            for movement in movements:
                (test_x, test_y), _, _ = from_code(movement)
                possibly_eaten_piece = self.at((test_x, test_y))
                eaten_piece = self.__move_piece(piece, cell_x, cell_y, test_x, test_y)
                is_checked = self.player_is_checked(is_white_turn)
                self.reject_move_piece(piece, eaten_piece, (test_x, test_y), (cell_x, cell_y))
                
                is_checkmate = is_checkmate and is_checked
                valid_movements += int(not is_checked)
                # if not is_checked:
                #     is_checkmate = False
                #     valid_movements += 1
                    # self.try_move_piece(piece, is_white_turn, test_x, test_y, cell_x, cell_y)
                    # self.revert_eaten_piece(possibly_eaten_piece, (test_x, test_y))
            
            self.set_piece_at(piece, (cell_x, cell_y))

        self.stalemate = valid_movements == 0
        self.checkmate = is_checkmate

        self.__internal_board = original_board
        self.__eaten_pieces = original_eaten_pieces

    def draw(self, screen: pygame.Surface, clicked_piece: Piece):
        self.draw_board(screen)
        self.draw_pieces(screen, clicked_piece)
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

    def draw_pieces(self, screen: pygame.Surface, clicked_piece: Piece):
        self.draw_piece_valid_movements(screen, clicked_piece)

        for row in self.__internal_board:
            for piece in row:
                if piece is not None:
                    piece.draw(screen)

    def draw_piece_valid_movements(self, screen: pygame.Surface, clicked_piece: Piece):
        if clicked_piece is None:
            return

        cell = self.get_cell(clicked_piece.x, clicked_piece.y)
        movements = clicked_piece.get_valid_movements(self.__internal_board, cell)
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
        for piece in self.__eaten_pieces:
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
