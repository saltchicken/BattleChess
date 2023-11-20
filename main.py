import pygame
from game_engine import GameEngine

pygame.init()

def main():
    clock = pygame.time.Clock()
    game_engine = GameEngine()

    selected_piece = None
    offset_x = offset_y = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for piece, piece_obj in game_engine.pieces.items():
                    if piece_obj.rect.collidepoint(event.pos):
                        selected_piece = piece_obj
                        offset_x = piece_obj.position[0] - event.pos[0]
                        offset_y = piece_obj.position[1] - event.pos[1]
                        break
            elif event.type == pygame.MOUSEBUTTONUP:
                if selected_piece:
                    selected_piece.snap_to_grid((offset_x, offset_y))
                    selected_piece = None
            elif event.type == pygame.MOUSEMOTION:
                if selected_piece:
                    mouse_x, mouse_y = event.pos
                    selected_piece.move((mouse_x + offset_x, mouse_y + offset_y))

        game_engine.draw_board()
        game_engine.draw_pieces()
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
