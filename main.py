import pygame
from game_engine import GameEngine

pygame.init()

def main():
    clock = pygame.time.Clock()
    game_engine = GameEngine()
    while game_engine.running:
        game_engine.event_loop()
        game_engine.chessboard.draw_board()
        game_engine.draw_pieces()
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
