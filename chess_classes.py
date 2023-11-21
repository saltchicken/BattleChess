import pygame


# TODO: Need a better way to declare
WIDTH, HEIGHT = 800, 800  # Size of the window
ROWS, COLS = 8, 8  # Number of rows and columns
SQUARE_SIZE = WIDTH // COLS  # Size of each square

WHITE = (200, 255, 200)
BLACK = (0, 100, 0)



class ChessPiece:
    def __init__(self, image, row, column):
        self.image = image
        self.position = (column * SQUARE_SIZE, (row * SQUARE_SIZE)) # Position is a tuple (x, y)
        self.rect = pygame.Rect(self.position[0], self.position[1], SQUARE_SIZE, SQUARE_SIZE)
        self.row = row
        self.column = column

    def draw(self, screen):
        screen.blit(self.image, self.position)
    
    def move(self, new_position):
        self.position = new_position
        self.rect.x, self.rect.y = new_position

    def snap_to_grid(self, offset):
        # Calculate the center of the piece
        piece_center_x = self.position[0] + SQUARE_SIZE // 2
        piece_center_y = self.position[1] + SQUARE_SIZE // 2

        # Find the nearest square center
        nearest_col = round((piece_center_x + offset[0]) / SQUARE_SIZE)
        nearest_row = round((piece_center_y + offset[1]) / SQUARE_SIZE)

        # Calculate the new position to snap to the center of the nearest square
        new_x = nearest_col * SQUARE_SIZE
        new_y = nearest_row * SQUARE_SIZE

        self.move((new_x, new_y))

def chessboard_squares():
    files = 'abcdefgh'
    ranks = '12345678'

    for file in files:
        for rank in ranks:
            yield file + rank
            
class ChessBoard:
    def __init__(self, screen):
        self.screen = screen
        self.create_board()
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
                
class ChessSquare:
    def __init__(self, x, y, color, label):
        self.rect = pygame.Rect(x, y, SQUARE_SIZE, SQUARE_SIZE)
        self.color = color
        self.label = label
        self.occupied = None

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

                
