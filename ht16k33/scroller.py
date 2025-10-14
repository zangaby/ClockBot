from .font import font
from time import sleep
import math

class Scroller():
    def __init__(self, matrix, num_rows=8, num_cols=8):
        self.matrix = matrix
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.offset = 0
        self.gap = 0
        self.brightness = 1.0

    def clear(self):
        for col in range(self.num_cols):
            for row in range(self.num_rows):
                self.matrix.pixel(col, row, 0)

    def display_character(self, character, pos):
        for row_idx, row in enumerate(character):
            for col_idx, pixel_value in enumerate(row):
                x = self.num_rows - row_idx - 1
                y = self.num_cols - (col_idx + self.offset + pos) - 1

                if 0 <= x < self.num_rows and 0 <= y < self.num_cols:
                    self.matrix.reverse_pixel(x, y, int(pixel_value))

        self.offset += len(character[0]) + self.gap

    def show_message(self, message, position):
        for character in message:
            self.display_character(font.get(character), position)

        self.offset = 0
