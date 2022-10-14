import pygame
from board import Board
from pieces.piece import Piece
from pieces.piece_code import PieceCode
from pieces.piece_factory import PieceFactory
from util.colors import Colors
import random as rd

from util.utils import from_code, is_king, is_pawn

MAX_FPS = 60

current_fps = MAX_FPS

class Game:
    def __init__(self, width: int, height: int):
        self.running: bool = True
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        
        self.reset()

    def reset(self):
        self.cell_size = self.height / 8
        self.board = Board((self.width - self.height) / 2, self.cell_size)

        self.is_white_turn = True

        self.clicked_piece: Piece = None

    def run(self):
        pygame.init()

        while self.running:
            self.clock.tick(MAX_FPS)
            
            self.screen.fill(Colors.BLACK)
            
            self.check_events()

            self.draw()

            self.play_ai()

            pygame.display.flip()

        pygame.quit()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.handle_mouse_click()

    def handle_mouse_click(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        x, y = self.board.get_cell(mouse_x, mouse_y)

        if not self.board.is_inside(x, y):
            return
        if self.clicked_piece is not None:
            self.handle_move_by_click(x, y)
        
        piece = self.board.at((x, y))
        if piece is None or piece.is_white != self.is_white_turn:
            self.clicked_piece = None
            return

        self.clicked_piece = piece

    def handle_move_by_click(self, x: int, y: int):
        if self.clicked_piece is None:
            return

        clicked_cell = self.board.get_piece_cell(self.clicked_piece)
        if self.clicked_piece.is_valid_movement(self.board.get(), clicked_cell, x, y):
            self.move_piece(self.clicked_piece, clicked_cell, (x, y))
            self.clicked_piece = None

    def move_piece(self, piece: Piece, from_pos: 'tuple[int, int]', to_pos: 'tuple[int, int]'):
        movement = piece.get_movement(self.board.get(), from_pos, to_pos)
        success = self.board.try_move_piece(piece, self.is_white_turn, from_pos, to_pos)
        if success:
            self.check_special_movements(piece, movement)

            piece.moved()
            self.is_white_turn = not self.is_white_turn
            self.check_game_result()
        return success

    def check_special_movements(self, piece: Piece, movement: str):
        if is_king(piece) or is_pawn(piece):
            cell, _,  will_castle, will_promote = from_code(movement)
            print(will_promote)
            if will_castle:
                self.castle(cell)
            elif will_promote:
                self.promote(cell)

    def castle(self, cell: 'tuple[int, int]'):
        x, y = cell
        if x > 4:
            rookie_pos = (7, y)
            rookie = self.board.at(rookie_pos)
            if self.is_white_turn:
                self.move_piece(rookie, rookie_pos, (x - 1, y))
            else:
                self.move_piece(rookie, rookie_pos, (x - 2, y))
        else:
            rookie_pos = (0, y)
            rookie = self.board.at(rookie_pos)
            if self.is_white_turn:
                self.move_piece(rookie, rookie_pos, (x + 1, y))
            else:
                self.move_piece(rookie, rookie_pos, (x + 2, y))

    def promote(self, cell: 'tuple[int, int]'):
        print('Hello')
        fen_code = PieceCode.QUEEN
        if not self.is_white_turn:
            fen_code = fen_code.lower()

        self.board.set_piece_at(PieceFactory.create(fen_code, self.cell_size), cell)

    def check_game_result(self):
        is_checkmate, is_stalemate = self.board.check_game_result(self.is_white_turn)
        if is_checkmate:
            print('Checkmate')
            self.reset()
        elif is_stalemate:
            print('Stalemate')
            self.reset()

    def draw(self):
        self.board.draw(self.screen, self.clicked_piece)

    def play_ai(self):
        if not self.is_white_turn:
            while True:
                pieces = self.board.get_pieces(self.is_white_turn)
                chosen_piece, piece_cell = rd.choice(pieces)

                movements = chosen_piece.get_valid_movements(self.board.get(), piece_cell)
                if len(movements) > 0:
                    chosen_move = rd.choice(movements)
                    movement_cell, _, _, _ = from_code(chosen_move)
                    if chosen_piece.is_valid_movement(self.board.get(), piece_cell, movement_cell[0], movement_cell[1]):
                        success = self.move_piece(chosen_piece, piece_cell, movement_cell)
                        if success:
                            break
