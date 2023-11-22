import pygame, os
import chess
from PIL import Image, ImageFilter
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
                    # pil_blured = Image.open(os.path.join("images", piece + "_.png")).filter(ImageFilter.GaussianBlur(radius=6))
                    # pygame_image = pygame.image.fromstring(pil_blured.tostring("raw", 'RGBA'), (SQUARE_SIZE, SQUARE_SIZE), 'RGBA')

                    self.images[piece] = pygame.transform.scale(pygame.image.load(os.path.join("images", piece + "_.png")), (SQUARE_SIZE, SQUARE_SIZE))
                else:
                    self.images[piece] = pygame.transform.scale(pygame.image.load(os.path.join("images", piece + ".png")), (SQUARE_SIZE, SQUARE_SIZE))
                row = index // 16
                column = (index // 2) % 8
                piece_obj = ChessPiece(self.images[piece], row, column)
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
                            self.selected_square = square
                            if square.occupied:
                                self.selected_piece = square.occupied
                                self.selected_piece.move((x - SQUARE_SIZE // 2, y - SQUARE_SIZE // 2)) 
                                # self.offset_x = square.occupied.position[0] - x
                                # self.offset_y = square.occupied.position[1] - y
            elif event.type == pygame.MOUSEBUTTONUP:
                x, y = event.pos
                if self.selected_piece:
                    for row in self.chessboard.board:
                        for square in row:
                            if square.rect.collidepoint(x, y):
                                if square == self.selected_square:
                                    print('huh')
                                    self.selected_piece.move((self.selected_piece.column * SQUARE_SIZE, self.selected_piece.row * SQUARE_SIZE))
                                    break
                                if square.occupied:
                                    self.selected_piece.move((self.selected_piece.column * SQUARE_SIZE, self.selected_piece.row * SQUARE_SIZE))
                                    # Additional logic for captures
                                else:
                                    new_x, new_y = self.selected_piece.snap_to_grid(x, y)
                                    print(self.selected_piece.row)
                                    self.selected_piece.row = new_x
                                    print(new_x)
                                    self.selected_piece.column = new_y
                                    square.occupied = self.selected_piece
                                    self.selected_square.occupied = None
                                    # change chess module
                    self.selected_piece = None
                    self.selected_square = None
            elif event.type == pygame.MOUSEMOTION:
                if self.selected_piece:
                    mouse_x, mouse_y = event.pos
                    self.selected_piece.move((mouse_x - SQUARE_SIZE // 2, mouse_y - SQUARE_SIZE // 2)) 