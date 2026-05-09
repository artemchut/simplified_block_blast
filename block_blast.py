import pygame
from pygame.locals import *
import sys
import random
import time


"""--------------------------------------------
   | DRAG THE PIECE WITH YOUR LMC AND DROP IT |
   |    WHEREVER YOU WANT WITHIN THE GRID     |
   --------------------------------------------
"""

print("""   --------------------------------------------
   | DRAG THE PIECE WITH YOUR LMC AND DROP IT |
   |    WHEREVER YOU WANT WITHIN THE GRID     |
   --------------------------------------------
""")



pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((960,640))

score_font = pygame.font.SysFont("Comic Sans MS", 30)
large_font = pygame.font.SysFont("Comic Sans MS", 60)


map = [[1,1,1,1,1,1,1,1,1,1],
        [1,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,1],
        [1,1,1,1,1,1,1,1,1,1]]
pieces = [
    [[2],[2],[2]], #cube
    [[2,2,2],[0,2,0],[0,2,0]], # T looking one
    [[2],[2],[2]], # l looking one
    [[2,2],[2,2]], # cube
    [[2],[2],[2],[2]], # | looking one
    [[0,2],[2,0]], # .^ looking one
    [[0,2],[0,2],[2,2]], # |_ looking one
    [[2,2,0],[0,2,2]], # -_ looking one
    [[0,2,2],[2,2,0]], # _- looking one
    [[0,2,0],[2,2,2]], # _l_ looking one
    [[2,2,2],[0,0,2],[0,0,2]], # massive ¬ looking one
    [[2,2],[2,2],[2,2]], # triple stacked ◼◼ looking one
    [[2,2,2],[2,2,2],[2,2,2]], # triple stacked ◼◼◼ looking one
    [[2]], # ◼ one
]


def draw_map():
    for i,piece in enumerate(map):
        for k,pixel in enumerate(piece):
            if pixel == 1:
                pygame.draw.rect(screen, "#BCE6F6", (k*64,i*64, 64,64))
            elif pixel == 0:
                pygame.draw.rect(screen, "#AFAFAF", (k*64,i*64, 64,64),1)
            elif pixel == 3:
                pygame.draw.rect(screen, "yellow", (k*64,i*64, 64,64))
    pygame.draw.rect(screen, "#BCE6F6", (640,0, screen.get_width()-640,screen.get_height()))
draw_map()

class Piece:
    pieces = []
    def __init__(self):
        self.size = 32
        self.colour = "green"
        self.x = (screen.get_width()-(screen.get_width()-640-32))
        self.y = 100+len(Piece.pieces)*196
        self.random_piece = random.choice(pieces)
        Piece.pieces.append(self)

    def draw(self):
        for i,row in enumerate(self.random_piece):
            for k,column in enumerate(row):
                if column == 2:
                    pygame.draw.rect(screen, self.colour, (self.x+k*self.size,self.y+i*self.size, self.size,self.size))
    def find_piece(self):
        global mouse_y

        piece_i = 0

        for y in range(screen.get_height()):
            for x in range(screen.get_width()-self.size):
                if screen.get_at((x,y)) == (0,255,0): # finding borders of the piece
                    for piece in Piece.pieces:
                        if mouse_y >= piece.y and mouse_y <= piece.y+len(self.random_piece)*self.size+self.size:
                            return piece_i
                        piece_i += 1
                piece_i = 0
        return None

    def move_piece(self):
        if self.colour == "green":
            self.size = 64

            self.y = mouse_y-(len(Piece.pieces[piece_i].random_piece)*64//2)
            self.x = mouse_x-(len(Piece.pieces[piece_i].random_piece[0])*64//2)


def piece_placed():
    global score
    placed = False

    # IF WITHIN THE GRID
    # value 33 and 543 are min & max numbers that will be rounded % 64 to make the piece stick to the grid
    if Piece.pieces[piece_i].x >= 33 and Piece.pieces[piece_i].x+(len(Piece.pieces[piece_i].random_piece[0])-1)*64 <= 543:
        if Piece.pieces[piece_i].y >= 33 and Piece.pieces[piece_i].y+(len(Piece.pieces[piece_i].random_piece)-1)*64 <= 543:
            if Piece.pieces[piece_i].y % 64 <= 32 or Piece.pieces[piece_i].y+len(Piece.pieces[piece_i].random_piece)*64 >= len(map)*64-64: # checkng which side's the closest(left or right)
                Piece.pieces[piece_i].y -= Piece.pieces[piece_i].y % 64 # finding the closest point(snapping)
            else:
                Piece.pieces[piece_i].y += 64 - Piece.pieces[piece_i].y % 64
            if Piece.pieces[piece_i].x % 64 <= 32 or Piece.pieces[piece_i].x+len(Piece.pieces[piece_i].random_piece[0])*64 >= len(map[0])*64-64:
                Piece.pieces[piece_i].x -= Piece.pieces[piece_i].x % 64
            else:
                Piece.pieces[piece_i].x += 64 - Piece.pieces[piece_i].x % 64
            Piece.pieces[piece_i].colour = "blue"
            placed = True
            
            # checking whether it collides with any other pieces when being placed
            for y, row in enumerate(Piece.pieces[piece_i].random_piece):
                for x, column in enumerate(row):
                    if column == 2:
                        if map[Piece.pieces[piece_i].y//64+y][Piece.pieces[piece_i].x//64+x] == 3:
                            placed = False
            if placed: # if doesn't collide then...
                for y, row in enumerate(Piece.pieces[piece_i].random_piece):
                    for x, column in enumerate(row):
                        if column == 2: # change all 2s to 3s to indicate the those pieces have already been placed
                            map[Piece.pieces[piece_i].y//64+y][Piece.pieces[piece_i].x//64+x] = 3
                Piece.pieces.pop(piece_i)

                score += 100

    if not placed:
        Piece.pieces[piece_i].size = 32
        Piece.pieces[piece_i].colour = "green"
        # move back to the start
        for piece in range(len(Piece.pieces)):
            Piece.pieces[piece].y = 100+(piece)*196
            Piece.pieces[piece].x = (screen.get_width()-(screen.get_width()-640-32))

def check_rows_columns_completed():
    global score,multiplier
    pixels_completed = 0

    # checking if any rows are complete
    rows_completed = []
    for y in range(len(map)):
        for x in range(len(map[y])):
            if map[y][x] == 3:
                pixels_completed += 1
        if pixels_completed == 8:
            rows_completed.append(y)
        pixels_completed = 0
    # checking if any columns are complete
    columns_completed = []
    for x in range(len(map)):
        for y in range(len(map[x])):
            if map[y][x] == 3:
                pixels_completed += 1
        if pixels_completed == 8:
            columns_completed.append(x)
        pixels_completed = 0

    # deleting all the rows complete
    for row in rows_completed:
        for i in range(len(map[row])):
            if map[row][i] == 3:
                map[row][i] = 0
    # deleting all the columns complete
    for column in columns_completed:
        for i in range(len(map[column])):
            if map[i][column] == 3:
                map[i][column] = 0
    
    if len(rows_completed)+len(columns_completed) > 0:
        for completed_line in range(len(rows_completed)+len(columns_completed)):
            score += 400*multiplier
            multiplier += 1
        return 1,1
    else:
        return 0,1
    
def check_possibilities():
    pieces_fit = 0
    for piece in Piece.pieces:
        can_fit = False 
        for row in range(len(map)):
            for column in range(len(map[row])):
                fit = True
                for y in range(len(piece.random_piece)):
                    for x in range(len(piece.random_piece[y])):
                        if piece.random_piece[y][x] == 2:
                            # bounds check
                            if row+y >= len(map) or column+x >= len(map[0]):
                                fit = False
                                break
                            # collision check
                            if map[row+y][column+x] != 0:
                                fit = False
                                break
                    if not fit:
                        break
                if fit:
                    can_fit = True
                    break
            if can_fit:
                break
        if can_fit:
            pieces_fit += 1

    if pieces_fit == 0:
        return True
    else:
        return False
        



# SPAWNING EVERYTHING AT THE VERY START OF THE GAME
for i in range(3):
    Piece().draw()

# VARIABLES
dragging = False
score = 0
multiplier = 1
lines_completed = 0
pieces_placed = 0


while True:
    screen.fill("black")

    # RE DRAWING EVERYTHING
    draw_map()
    for piece in Piece.pieces:
        piece.draw()
    # displaying the score
    score_text = score_font.render(f"Your score is : {int(score)}", False, (0,0,0))
    screen.blit(score_text, (140, 12))

    lost = check_possibilities() # checking whether there are any free spaces left in the grid
    if lost:
        lost_text = large_font.render(f"You lost", False, (255,255,255))
        screen.blit(lost_text, (screen.get_width()//2-100, screen.get_height()//2-28))
        pygame.display.update()
        time.sleep(3)
        pygame.quit()
        sys.exit()


    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
            pygame.quit()
        if event.type == MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if screen.get_at((mouse_x, mouse_y)) == (0,255,0):
                piece_i = Piece.pieces[0].find_piece()
                if event.button == 1:
                    dragging = True
        elif event.type == MOUSEBUTTONUP:
            try:
                piece_placed()
            except:pass

            _,__ = check_rows_columns_completed()
            lines_completed += _
            pieces_placed += __
            if pieces_placed == 3:
                if lines_completed == 0:
                    multiplier = 1
                lines_completed = 0
                pieces_placed = 0
            if len(Piece.pieces) == 0:
                for i in range(3): #spawning new pieces
                    Piece().draw()
            dragging = False

    
    if dragging:
        mouse_x, mouse_y = pygame.mouse.get_pos() 
        try: # if piece_i wasn't found
            Piece.pieces[piece_i].move_piece()
        except:pass
    


    pygame.display.update()
    pygame.time.Clock().tick(60)
