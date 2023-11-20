import pygame


# TODO: Need a better way to declare
WIDTH, HEIGHT = 800, 800  # Size of the window
ROWS, COLS = 8, 8  # Number of rows and columns
SQUARE_SIZE = WIDTH // COLS  # Size of each square


class ChessPiece:
    def __init__(self, image, position):
        self.image = image
        self.position = position  # Position is a tuple (x, y)
        self.rect = pygame.Rect(self.position[0], self.position[1], SQUARE_SIZE, SQUARE_SIZE)

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
