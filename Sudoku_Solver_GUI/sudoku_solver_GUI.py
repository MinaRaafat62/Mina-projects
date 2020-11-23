import pygame,sys
from solver import solve, valid

# In execution every cube is going to be solved seperately when you hit space




pygame.font.init()
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREY = (128,128,128)

class Settings():
    """A class to store all settings for Sudoku GUI"""
    def __init__(self):
        """Initialize the game's settings"""
        # Screen settings
        self.screen_width = 540
        self.screen_height = 600
        self.bg_color = (255, 255, 255)

    def update_screen(self,screen,board):
        
        clock = pygame.time.Clock()
        """Update images on the screen and flip to the new screen."""
        # Redraw the screen through each pass through the loop
        screen.fill(self.bg_color)
        
        board.draw_grid(screen)
       
        fnt = pygame.font.SysFont("comicsans", 40)

        # Draw Strikes
        text = fnt.render(str(strikes) +"X", 1, RED)
        screen.blit(text, (20, 560))
        
        
        board.update_model()

        # Make the most recently drawn screen visible.
        pygame.display.update()
        clock.tick(100)

    

        

class Grid:

    my_board =  [ [ 0, 0, 4,   0, 0, 0,   0, 6, 7 ],
                 [ 3, 0, 0,   4, 7, 0,   0, 0, 5 ],
                 [ 1, 5, 0,   8, 2, 0,   0, 0, 3 ],

                 [ 0, 0, 6,   0, 0, 0,   0, 3, 1 ],
                 [ 8, 0, 2,   1, 0, 5,   6, 0, 4 ],
                 [ 4, 1, 0,   0, 0, 0,   9, 0, 0 ],
                            
                 [ 7, 0, 0,   0, 8, 0,   0, 4, 6 ],
                 [ 6, 0, 0,   0, 1, 2,   0, 0, 0 ],
                 [ 9, 3, 0,   0, 0, 0,   7, 1, 0 ] ]

    def __init__(self, rows, cols, width, height):
        self.rows = rows
        self.cols = cols
        self.cubes = [[Cube(self.my_board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.width = width
        self.height = height
        self.model = None
        self.selected = None
    
    def update_model(self):
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]
    
    def place(self, val):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set(val)
            self.update_model()

            if valid(self.model, val, (row,col)) and solve(self.model):
                return True
            else:
                self.cubes[row][col].set(0)
                self.cubes[row][col].set_temp(0)
                self.update_model()
                return False

            


    def sketch(self, val):
        row, col = self.selected
        self.cubes[row][col].set_temp(val)

    def draw_grid(self, screen):
        gap = self.width / 9
        for i in range (self.rows+1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(screen, BLACK, (0, i*gap), (self.width, i*gap), thick)
            pygame.draw.line(screen, BLACK, (i * gap, 0), (i * gap, self.height), thick)

        # Drawing cubes
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw_cube(screen)

    def select(self, row, col):
            # Reset all other
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False

        self.cubes[row][col].selected = True
        self.selected = (row, col)
           
    def clear(self):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set_temp(0)

    def click(self, pos):
        """
        :param: pos
        :return: (row, col)
        """
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return (int(y),int(x))
        else:
            return None

    def is_finished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value == 0:
                    return False
        return True

class Cube:
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width ,height):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False

    def draw_cube(self, screen):
        fnt = pygame.font.SysFont("comicsans", 40)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        if self.temp != 0 and self.value == 0:
            text = fnt.render(str(self.temp), 1, GREY)
            screen.blit(text, (x+5, y+5))
        elif not(self.value == 0):
            text = fnt.render(str(self.value), 1, BLACK)
            screen.blit(text, (x + (gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/2)))

        if self.selected:
            pygame.draw.rect(screen, RED, (x,y, gap ,gap), 3)

    def set(self, val):
        self.value = val

    def set_temp(self, val):
        self.temp = val


# game functions

def solve_game(board):
    for i in range(board.rows):
        for j in range (board.cols):
            board.place(board.cubes[i][j].value)


def main():
    global active, strikes, keys
    pygame.init()
    ss_settings = Settings()
    board = Grid(9, 9, 540, 540)
    screen = pygame.display.set_mode((ss_settings.screen_width,ss_settings.screen_height))
    pygame.display.set_caption("Sudoku")
    active = True
    strikes = 0
    key = None
    
    
    

    while active:
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                active = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_RETURN:
                    i, j = board.selected
                    if board.cubes[i][j].temp != 0:
                        if board.place(board.cubes[i][j].temp):
                            print("Success")
                        else:
                            print("Wrong")
                            strikes += 1
                        key = None

                        if board.is_finished():
                            print("Game over")
                            active = False

                if event.key == pygame.K_SPACE:
                    solve_game(board)
                    
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None

        if board.selected and key != None:
                board.sketch(key)
            
        ss_settings.update_screen(screen,board)
        pygame.display.update()
 


main()
