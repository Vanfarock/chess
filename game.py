import pygame
import random as rd
from board import Board
from pieces.piece import Piece
from pieces.piece_code import PieceCode
from pieces.piece_factory import PieceFactory
from util.colors import Colors

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
        self.is_checkmate = False
        self.is_stalemate = False

    def run(self):
        pygame.init()

        while self.running:
            self.clock.tick(MAX_FPS)
            
            self.screen.fill(Colors.BLACK)
            
            self.show_game_result()
            
            self.play_ai()
            self.play_ai2()
            
            self.check_events()
            
            self.draw()

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
        self.is_white_turn = not self.is_white_turn

    def promote(self, cell: 'tuple[int, int]'):
        fen_code = PieceCode.QUEEN
        if not self.is_white_turn:
            fen_code = fen_code.lower()

        self.board.set_piece_at(PieceFactory.create(fen_code, self.cell_size), cell)

    def check_game_result(self):
        self.is_checkmate, self.is_stalemate = self.board.check_game_result(self.is_white_turn)

    def show_game_result(self):
        if self.is_checkmate:
            if self.is_white_turn:
                print('Checkmate Black Wins')
            else:
                print('Checkmate Wins Wins')
            input('Press Enter to Reset...')
            self.reset()
        elif self.is_stalemate:
            print('Stalemate')
            input('Press Enter to Reset...')
            self.reset()

    def draw(self):
        self.board.draw(self.screen, self.clicked_piece)

    def play_ai(self):
        if not self.is_white_turn and not self.is_game_over():
            piece, move, score = self.maxi(4, self.is_white_turn, float('-inf'), float('inf'))
            if move is None:
                # print('Got here')
                # self.check_game_result()
                return

            move_cell, _, _, _ = from_code(move)
            self.move_piece(piece, self.board.get_piece_cell(piece), move_cell)
            print(score)
            
    def maxi(
        self,
        depth: int,
        is_white: bool,
        alpha: int,
        beta: int,
    ) -> 'tuple[Piece, str, int]':
        if depth == 0:
            return None, None, self.board.evaluate()

        best_piece = None
        best_move = None
        best_score = float('-inf')

        all_possible_moves = []
        for piece, piece_cell in self.board.get_pieces(is_white):
            for move in piece.get_valid_movements(self.board.get(), piece_cell):
                all_possible_moves.append((piece, piece_cell, move))
        
        for piece, piece_cell, move in all_possible_moves:
            move_cell, _, _, _ = from_code(move)

            piece_was_moved = piece.was_moved

            eaten_piece = self.board.move_piece(piece, piece_cell, move_cell)
            is_checked = self.board.player_is_checked(is_white)
            if not is_checked:
                piece.moved()
                _, _, score = self.mini(depth-1, not is_white, alpha, beta)
                if score > best_score:
                    best_piece = piece
                    best_move = move
                    best_score = score
                alpha = max(alpha, score)
            self.board.reject_move_piece(piece, eaten_piece, piece_cell, move_cell)
            piece.was_moved = piece_was_moved

            if beta <= alpha:
                break
        return best_piece, best_move, best_score

    def mini(
        self,
        depth: int,
        is_white: bool,
        alpha: int,
        beta: int,
    ) -> 'tuple[Piece, str, int]':
        if depth == 0:
            return None, None, self.board.evaluate()

        worst_piece = None
        worst_move = None
        worst_score = float('inf')

        all_possible_moves = []
        for piece, piece_cell in self.board.get_pieces(is_white):
            for move in piece.get_valid_movements(self.board.get(), piece_cell):
                all_possible_moves.append((piece, piece_cell, move))
        
        for piece, piece_cell, move in all_possible_moves:
            move_cell, _, _, _ = from_code(move)

            piece_was_moved = piece.was_moved

            eaten_piece = self.board.move_piece(piece, piece_cell, move_cell)
            is_checked = self.board.player_is_checked(is_white)
            if not is_checked:
                piece.moved()
                _, _, score = self.maxi(depth-1, not is_white, alpha, beta)
                if score < worst_score:
                    worst_piece = piece
                    worst_move = move
                    worst_score = score
                beta = min(beta, score)
            self.board.reject_move_piece(piece, eaten_piece, piece_cell, move_cell)
            piece.was_moved = piece_was_moved

            if beta <= alpha:
                break
        return worst_piece, worst_move, worst_score
        
    def play_ai2(self):
        if self.is_white_turn and not self.is_game_over():
            pieces = self.board.get_pieces(self.is_white_turn)
            while True:
                chosen_piece, piece_cell = rd.choice(pieces)

                movements = chosen_piece.get_valid_movements(self.board.get(), piece_cell)
                if len(movements) > 0:
                    chosen_move = rd.choice(movements)
                    movement_cell, _, _, _ = from_code(chosen_move)
                    if chosen_piece.is_valid_movement(self.board.get(), piece_cell, movement_cell[0], movement_cell[1]):
                        success = self.move_piece(chosen_piece, piece_cell, movement_cell)
                        if success:
                            break

    def is_game_over(self):
        return self.is_checkmate or self.is_stalemate