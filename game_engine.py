import pygame, os
import chess
from chess_classes import ChessPiece, ChessBoard

# TODO: Better way to declare this
WIDTH, HEIGHT = 800, 800  # Size of the window
ROWS, COLS = 8, 8  # Number of rows and columns
SQUARE_SIZE = WIDTH // COLS

class GameEngine:
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Chess Board")
        self.running = True
        self.chessboard = ChessBoard(self.screen)
        self.images = {}
        self.pieces = []
        self.load_pieces()
        self.selected_piece = None
        self.offset_x = 0
        self.offset_y = 0
        
    def load_pieces(self) -> None:
        board = chess.Board()
        # TODO Consider using board.piece_map()
        for index, piece in enumerate(board.__str__()):
            if piece.isalpha():
                if piece.islower():
                    self.images[piece] = pygame.transform.scale(pygame.image.load(os.path.join("images", piece + "_.png")), (SQUARE_SIZE, SQUARE_SIZE))
                else:
                    self.images[piece] = pygame.transform.scale(pygame.image.load(os.path.join("images", piece + ".png")), (SQUARE_SIZE, SQUARE_SIZE))
                row = index // 16
                column = (index // 2) % 8
                piece_obj = ChessPiece(self.images[piece], (column * SQUARE_SIZE, (row * SQUARE_SIZE)))
                self.pieces.append(piece_obj)
                self.chessboard.board[row][column].occupied = piece_obj
        
                
    def draw_pieces(self):
        for piece_obj in self.pieces:
            piece_obj.draw(self.screen)
            
    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                for row in self.chessboard.board:
                    for square in row:
                        if square.rect.collidepoint(x, y):
                            print(square.label)
                            print(square.occupied)
                for piece_obj in self.pieces:
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