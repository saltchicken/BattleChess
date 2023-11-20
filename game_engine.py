import pygame, os
from chess_pieces import ChessPiece

# TODO: Better way to declare this
WIDTH, HEIGHT = 800, 800  # Size of the window
ROWS, COLS = 8, 8  # Number of rows and columns
SQUARE_SIZE = WIDTH // COLS

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class GameEngine:
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Chess Board")
        self.images = {}
        self.load_pieces()
        
    def load_pieces(self) -> None:
        pieces = ["b_rook", "w_rook"]
        for piece in pieces:
            self.images[piece] = pygame.transform.scale(pygame.image.load(os.path.join("images", piece + ".png")), (SQUARE_SIZE, SQUARE_SIZE))
        self.pieces = {
        'b_rook': ChessPiece(self.images['b_rook'], (4 * SQUARE_SIZE, 0)),
        'w_rook': ChessPiece(self.images['w_rook'], (4 * SQUARE_SIZE, 7 * SQUARE_SIZE))
    }
        
    def draw_board(self):
        self.screen.fill(WHITE)
        for row in range(ROWS):
            for col in range(row % 2, ROWS, 2):
                pygame.draw.rect(self.screen, BLACK, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                
    def draw_pieces(self):
        for piece_obj in self.pieces.values():
            piece_obj.draw(self.screen)
            