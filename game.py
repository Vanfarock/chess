import pygame
from colors import Colors
from board import Board

MAX_FPS = 60

current_fps = MAX_FPS

class Game:
    def __init__(self, width: int, height: int):
        self.running = True
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        
        self.board = Board((self.width - self.height) / 2, self.height / 8)

        self.reset()

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

            self.board.handle_events(event)

    def draw(self):
        self.board.draw(self.screen)

    def reset(self):
        pass
