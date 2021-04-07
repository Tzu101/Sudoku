import copy
import pygame
from SudokuSolver import SudokuSolver


class Line:

    def __init__(self, color, start, end, width):
        self.color = color
        self.start = start
        self.end = end
        self.width = width

    def update(self, surface):
        pygame.draw.line(surface, self.color, self.start, self.end, self.width)

class Box:
    
    def __init__(self, color, pos, size, border_width):
        
        self.lines = []

        size0 = size[0] - 1
        size1 = size[1] - 1
        offset1 = (border_width - 1) // 2
        offset2 = border_width // 2

        top_line = Line(color, (pos[0], pos[1] + offset1), (pos[0] + size0, pos[1] + offset1), border_width)
        self.lines.append(top_line)

        bottom_line = Line(color, (pos[0], pos[1] + size1 - offset2), (pos[0] + size0, pos[1] + size1 - offset2), border_width)
        self.lines.append(bottom_line)

        left_line = Line(color, (pos[0] + offset1, pos[1]), (pos[0] + offset1, pos[1] + size1), border_width)
        self.lines.append(left_line)

        right_line = Line(color, (pos[0] + size0 - offset2, pos[1]), (pos[0] + size0 - offset2, pos[1] + size1), border_width)
        self.lines.append(right_line)

    def update(self, surface):
        for line in self.lines:
            line.update(surface)

class SpriteSheet:

    def __init__(self, file):
        self.num_sheet = pygame.image.load(file).convert()

    def get_num(self, n):

        if 1 > n or n > 9:
            n = 0

        x = n % 5
        y = n // 5

        num = pygame.Surface((70, 70))
        num.set_colorkey((0, 0, 0))
        num.blit(self.num_sheet, (0, 0), (70*x, 70*y, 70, 70))

        return num

class SudokuTile:

    def __init__(self, pos, size, sprite):
        self.pos = pos
        self.size = size
        self.sprite = sprite

    def set_sprite(self, sprite):
        self.sprite = sprite

    def update(self, surface):
        surface.blit(self.sprite, (self.pos, self.size))
    
    def highlite(self, surface):

        highlite = pygame.Surface(self.size)
        highlite.set_alpha(128)
        highlite.fill((200,200,200))
        surface.blit(highlite, self.pos)

class Button:

    def __init__(self, pos, size, sprite, onclick):
        self.pos = pos
        self.size = size
        self.sprite = sprite
        self.onclick = onclick
        self.selected = False

    def calculate(self, mouse_pos):

        if (self.pos[0] <= mouse_pos[0] < self.pos[0] + self.size[0] 
        and self.pos[1] <= mouse_pos[1] < self.pos[1] + self.size[1]):
            self.selected = True
        else:
            self.selected = False

    def update(self, surface):

        if self.selected:
            highlite = pygame.Surface(self.size)
            highlite.set_alpha(128)
            highlite.fill((200,200,200))
            surface.blit(highlite, self.pos)

        surface.blit(self.sprite, self.pos)


def set_board(board):

    tiles = []

    for y in range(9):
        for x in range(9):
            tiles.append(SudokuTile((70*x, 70*y + 100), (70, 70), 
            numbers.get_num(board[y][x])))

    return tiles

def solve_board():

    global tiles
    global sudoku
    global board_num

    board_num = 0

    sudoku.solve()
                
    if len(sudoku.solved_boards) > 0:
        tiles = set_board(sudoku.solved_boards[0])

def reset_board():

    global tiles
    global sudoku

    sudoku.reset()
                
    tiles = set_board(sudoku.board)

def next_board():

    global tiles
    global board_num

    if len(sudoku.solved_boards)-1 > board_num and len(sudoku.solved_boards) > 0:
        board_num += 1
        tiles = set_board(sudoku.solved_boards[board_num])
    
def prev_board():

    global tiles
    global board_num

    if 0 < board_num and len(sudoku.solved_boards) > 0:
        board_num -= 1
        tiles = set_board(sudoku.solved_boards[board_num])


WIDTH = 630
HEIGHT = 730

pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption('Sudoku')
pygame.display.set_icon(pygame.Surface((32, 32)))

# Sudoku values
numbers = SpriteSheet("sudoku_numbers.png")
images = SpriteSheet("button_sprites.png")

sudoku = SudokuSolver()
board_num = 0
selected_tile = None

# Sudoku grid
buttons = []
buttons.append(Button((15, 15), (70, 70), images.get_num(3), prev_board))
buttons.append(Button((545, 15), (70, 70), images.get_num(2), next_board))

buttons.append(Button((175, 15), (70, 70), images.get_num(1), solve_board))
buttons.append(Button((630-175-70, 15), (70, 70), images.get_num(0), reset_board))

tiles = set_board(sudoku.board)

lines = []
for x in range(6):
    y = 170 + 70*x + 70*(x // 2)
    lines.append(Line((75, 75, 75), (0, y), (WIDTH, y), 1))

for y in range(6):
    x = 70 + 70*y + 70*(y // 2)
    lines.append(Line((75, 75, 75), (x, 100), (x, HEIGHT), 1))

boxes = []

boxes.append(Box((0, 0, 0), (0, 100), (WIDTH, HEIGHT-100), 3))

for x in range(3):
    for y in range(3):
        boxes.append(Box((0, 0, 0), (210 * x, 210 * y+100), (210, 210), 1))

running = True
while running:

    for event in pygame.event.get():

        if event.type == pygame.MOUSEMOTION:
            for button in buttons:
                button.calculate(pygame.mouse.get_pos())

        elif event.type == pygame.MOUSEBUTTONDOWN:

            mouse_x, mouse_y = pygame.mouse.get_pos()

            for button in buttons:
                if button.selected:
                    button.onclick()
                
            if mouse_y >= 100:
                tile_x = mouse_x // 70
                tile_y = (mouse_y - 100) // 70

                selected_tile = tiles[tile_y * 9 + tile_x]
            else:
                selected_tile = None

        elif event.type == pygame.KEYDOWN:                
                
            if 48 <= event.key <= 57 and selected_tile is not None:
                num = event.key - 48
                sudoku.board[(selected_tile.pos[1]-100) // 70][selected_tile.pos[0] // 70] = num
                selected_tile.set_sprite(numbers.get_num(num))

        elif event.type == pygame.QUIT:
            running = False

    window.fill((255, 255, 255))

    for button in buttons:
        button.update(window)

    if selected_tile is not None:
        selected_tile.highlite(window)

    for tile in tiles:
        tile.update(window)

    for line in lines:
        line.update(window)

    for box in boxes:
        box.update(window)
    
    pygame.display.flip()

pygame.quit()