import pygame, os
from chess_pieces import ChessPiece, ChessSquare

# TODO: Better way to declare this
WIDTH, HEIGHT = 800, 800  # Size of the window
ROWS, COLS = 8, 8  # Number of rows and columns
SQUARE_SIZE = WIDTH // COLS

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def chessboard_squares():
    files = 'abcdefgh'
    ranks = '12345678'

    for file in files:
        for rank in ranks:
            yield file + rank

class GameEngine:
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Chess Board")
        self.running = True
        self.create_board()
        self.images = {}
        self.load_pieces()
        self.selected_piece = None
        self.offset_x = 0
        self.offset_y = 0
        
    def load_pieces(self) -> None:
        pieces = ["b_rook", "w_rook"]
        for piece in pieces:
            self.images[piece] = pygame.transform.scale(pygame.image.load(os.path.join("images", piece + ".png")), (SQUARE_SIZE, SQUARE_SIZE))
        self.pieces = {
        'b_rook': ChessPiece(self.images['b_rook'], (4 * SQUARE_SIZE, 0)),
        'w_rook': ChessPiece(self.images['w_rook'], (4 * SQUARE_SIZE, 7 * SQUARE_SIZE))
    }
        
    def create_board(self):
        self.board = []
        chessboard_gen = chessboard_squares()
        for row in range(ROWS):
            board_row = []
            for col in range(COLS):
                x = col * SQUARE_SIZE
                y = row * SQUARE_SIZE
                color = WHITE if (row + col) % 2 == 0 else BLACK
                board_row.append(ChessSquare(x, y, color, next(chessboard_gen)))
            self.board.append(board_row)
        
    def draw_board(self):
        for row in self.board:
            for square in row:
                square.draw(self.screen)
                
    def draw_pieces(self):
        for piece_obj in self.pieces.values():
            piece_obj.draw(self.screen)
            
    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                for row in self.board:
                    for square in row:
                        if square.rect.collidepoint(x, y):
                            print(square.label) 
                for piece, piece_obj in self.pieces.items():
                    if piece_obj.rect.collidepoint(event.pos):
                        self.selected_piece = piece_obj
                        self.offset_x = piece_obj.position[0] - x
                        self.offset_y = piece_obj.position[1] - y
                        break
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.selected_piece:
                    self.selected_piece.snap_to_grid((self.offset_x, self.offset_y))
                    self.selected_piece = None
            elif event.type == pygame.MOUSEMOTION:
                if self.selected_piece:
                    mouse_x, mouse_y = event.pos
                    self.selected_piece.move((mouse_x + self.offset_x, mouse_y + self.offset_y))
            