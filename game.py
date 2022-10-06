import pygame
from board import Board
from pieces.piece import Piece
from util.colors import Colors

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
        self.board = Board((self.width - self.height) / 2, self.height / 8)

        self.is_white_turn = True

        self.clicked_piece: Piece = None

    def run(self):
        pygame.init()

        while self.running:
            self.clock.tick(MAX_FPS)
            
            self.screen.fill(Colors.BLACK)
            
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

        clicked_cell = self.board.get_cell(self.clicked_piece.x, self.clicked_piece.y)
        if self.clicked_piece.is_valid_movement(self.board.get(), clicked_cell, x, y):
            self.move_piece(self.clicked_piece, clicked_cell[0], clicked_cell[1], x, y)
            self.clicked_piece = None

    def move_piece(self, piece: Piece, from_x: int, from_y: int, to_x: int, to_y: int):
        success = self.board.try_move_piece(piece, self.is_white_turn, from_x, from_y, to_x, to_y)
        if success:
            piece.moved()
            self.is_white_turn = not self.is_white_turn
            self.check_game_result()

    def draw(self):
        self.board.draw(self.screen, self.clicked_piece)

    def check_game_result(self):
        self.board.check_game_result(self.is_white_turn)
        for row in self.board.get():
            for i in row:
                print(i, end=' ')
            print()
        # if self.checkmate:
        #     print('Checkmate')
        #     self.reset()
        # elif self.stalemate:
        #     print('Stalemate')
        #     self.reset()