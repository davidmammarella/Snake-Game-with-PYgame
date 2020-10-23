import pygame   # package that prvoides the framework to display and play games like this using python
import sys
import random


screen_width = 480      # size of screen (x axis)
screen_height = 480     # size of screen (y axis)

gridsize = 20
grid_width = screen_width/gridsize
grid_height = screen_height/gridsize

# directions the snake can move
up = (0,-1)
down = (0,1)
left = (-1,0)
right = (1,0)

# the snake spawns in the middle of the screen, this is approximately the grid that the walls will not spawn in
outside_safe_grid_x = [(0, grid_width /2  - 4) , (0, grid_width), (grid_height/2 + 4, grid_height), (0, grid_width)]
outside_safe_grid_y = [(0 , grid_height), (0, grid_width /2  - 4), (0 , grid_height), (grid_height/2 + 4, grid_height)]

num_walls = 8       # number of randomized walls to be spawned at beginning of game

def random_wall_positions(num_walls): 
    r'''
    Randomly determines the start position of each wall.

    Parameters:
        num_walls (int): Value that says approximately how many walls will be placed on the display screen.

    Returns:
        (vert_wall_pos, horz_wall_pos) (tuple): Tuple of dictionaries, the dictionaries are the starting positions of the vertical and horizontal walls.
    '''
    horz_wall_pos = {}
    vert_wall_pos = {}
    horz_wall_list = []
    vert_wall_list = []
    for i in range(0, num_walls//2):
        horz_wall_pos['W'+str(i)] = (random.randint(outside_safe_grid_x[i][0], outside_safe_grid_x[i][1])*gridsize, random.randint(outside_safe_grid_y[i][0], outside_safe_grid_x[i][1])*gridsize)
        # horz_wall_list.append(horz_wall_pos['W'+str(i)])
        vert_wall_pos['W'+str(i)] = (random.randint(outside_safe_grid_x[i][0], outside_safe_grid_x[i][1])*gridsize, random.randint(outside_safe_grid_y[i][0], outside_safe_grid_x[i][1])*gridsize)
        # vert_wall_list.append(vert_wall_pos['W'+str(i)])
    return (vert_wall_pos, horz_wall_pos) #, (vert_wall_list, horz_wall_list)

wall_pos = random_wall_positions(num_walls)  

def get_wall_coordinates(wall_pos):
    r'''
    Takes a the dictionary of wall starting positions and define every position on the display screen a wall piece will be on. These positions will each be appended into a list.
    
    Parameters:
        wall_pos (tuple): Tuple of dictionaries of staring positions of vertical and horizontal walls.

    Returns:
        wall_pos_list (list): List of all places on display screen a wall piece will be.  
    '''
    vert_wall_coords = {}
    horz_wall_coords = {}
    wall_pos_list = []
    for i in range(0, len(wall_pos[0])):     # these are the vertical walls, dimensions are (gridsize, gridsize*5)
        vert_wall_coords['W'+str(i)] = [wall_pos[0]['W'+str(i)], (wall_pos[0]['W'+str(i)][0], wall_pos[0]['W'+str(i)][1] + gridsize), (wall_pos[0]['W'+str(i)][0],wall_pos[0]['W'+str(i)][1] + gridsize*2), (wall_pos[0]['W'+str(i)][0],wall_pos[0]['W'+str(i)][1] + gridsize*3), (wall_pos[0]['W'+str(i)][0],wall_pos[0]['W'+str(i)][1] + gridsize*4)]  
    for i in range(0, len(wall_pos[1])):     # these are the vertical walls, dimensions are (gridsize*5, gridsize)
        horz_wall_coords['W'+str(i)] = [wall_pos[1]['W'+str(i)], (wall_pos[1]['W'+str(i)][0] + gridsize, wall_pos[1]['W'+str(i)][1]), (wall_pos[1]['W'+str(i)][0] + gridsize*2, wall_pos[1]['W'+str(i)][1]), (wall_pos[1]['W'+str(i)][0] + gridsize*3, wall_pos[1]['W'+str(i)][1]), (wall_pos[1]['W'+str(i)][0] + gridsize*4, wall_pos[1]['W'+str(i)][1])]
    for i in vert_wall_coords:
        for j in vert_wall_coords[i]:
            wall_pos_list.append(j)
    for i in horz_wall_coords:
        for j in horz_wall_coords[i]:
            wall_pos_list.append(j)

    return wall_pos_list

wall_pos_list = get_wall_coordinates(wall_pos)   

class Snake():
    r'''
    This is the snake that can be controlled by the up, down, right, left controll keys.

    Attributes:
    ----------
        length (int): the length of the snake a given time, updated as the snake eats a piece of food. Initialized to 1.
        positions (list): list of positions of where the snake moves to on the display board.
        direction (tuple): Direction the snake is going. Intialized to a random choice between up, down, left ,right.
        colour (tuple): Colour of the snake. Neon green.
        score (int): Score to be displayed in the left hand corner.

    Methods:
    ----------
        get_head_position: Get the position of the head of the snake at a given frame.  
        turn: How the snake turns on the display screen.
        move: How the snake traverses around the display screen.
        reset_game: Resets the game, snake goes back to the middle and to length 1. Score goes back to 1.
        draw_snake: Draws snake on the screen. 
        handle_keys: Allows snake to be controlled with up, down, left, right keys. 
    '''
    def __init__(self):
        self.length = 1
        self.positions = [((screen_width/2), (screen_height/2))]
        self.direction = random.choice([up, down, left, right])
        self.colour = (29, 197, 3)
        self.score = 0

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        if self.length > 1 and (point[0]*-1, point[1]*-1) == self.direction:
            return
        else:
            self.direction = point

    def move(self):
        cur = self.get_head_position()
        x,y = self.direction
        new = (((cur[0]+(x*gridsize))%screen_width), (cur[1]+(y*gridsize))%screen_height)
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.reset_game()
        elif cur in wall_pos_list:
            self.reset_game()
        else:
            self.positions.insert(0,new)
            if len(self.positions) > self.length:
                self.positions.pop()

    def reset_game(self):
        self.length = 1
        self.positions = [((screen_width/2), (screen_height/2))]
        self.direction = random.choice([up, down, left, right])
        self.score = 0

    def draw_snake(self,surface):
        for p in self.positions:
            r = pygame.Rect((p[0], p[1]), (gridsize,gridsize))
            pygame.draw.rect(surface, self.colour, r)
            pygame.draw.rect(surface, (93,216, 228), r, 1)

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(up)
                elif event.key == pygame.K_DOWN:
                    self.turn(down)
                elif event.key == pygame.K_LEFT:
                    self.turn(left)
                elif event.key == pygame.K_RIGHT:
                    self.turn(right)

class Food():
    r'''
    This is the food that will be randomly spawned on the display board.
    
    Attributes:
    ----------
        position (int): Position of the food at a given time. 
        colour (tuple): Colour of the food. Yellow.

    Methods:
    ----------
        randomize_position: Randomize position of the food on the display screen. Coded so that the food does not land on the same grid spot as a wall.
    '''
    def __init__(self):
        self.position = (0,0)
        self.colour = (223, 163, 49)
        self.randomize_position()

    def randomize_position(self):
        # make it so food does not land in walls
        not_in_walls = True 
        while not_in_walls == True:
            self.position = (random.randint(0, grid_width-1)*gridsize, random.randint(0, grid_height-1)*gridsize)
            if self.position not in wall_pos_list:
                not_in_walls = False
        
        


    def draw(self, surface):
        r = pygame.Rect((self.position[0], self.position[1]), (gridsize, gridsize))
        pygame.draw.rect(surface, self.colour, r)
        pygame.draw.rect(surface, (93, 216, 228), r, 1)


class Walls():
    r'''
    Randomly places vertical and horizontal walls on the display screen.

    Attributes:
    ----------
        num_walls (int): Number of walls to be placed.
        colour (tuple): Colour of the walls. Black.
        horz_wall_pos (dictionary): Starting positions of the horizontal walls to be placed on the display screen.
        vert_wall_pos (dictionary): Starting positions of the vertical walls to be placed on the display screen.

    Methods:
    ----------
        draw_vertical: Draw the vertical walls based on vert_wall_pos.
        draw_horzitonal: Draw the horzitonal walls based on horz_wall_pos.
    '''
    def __init__(self):
        self.num_walls = 8 # must change length of safe_grid_x and y if you want to change number of walls in this game
        self.colour = (0, 0, 0)
        self.horz_wall_pos = wall_pos[1]
        self.vert_wall_pos = wall_pos[0]


    def draw_vertical(self, surface):
        for i in range(0, self.num_walls//2):
            vert = pygame.Rect(self.vert_wall_pos['W'+str(i)], (gridsize, gridsize*5)) 
            pygame.draw.rect(surface, self.colour, vert)
            pygame.draw.rect(surface, (93, 216, 228), vert, 1)


    def draw_horzitonal(self, surface):
        for i in range(0, self.num_walls//2):
            horz = pygame.Rect(self.horz_wall_pos['W'+str(i)], (gridsize*5, gridsize))
            pygame.draw.rect(surface, self.colour, horz)
            pygame.draw.rect(surface, (93,216,228), horz, 1)
    

def drawGrid(surface):
    '''
    Draws the background checkerboard grid.

    Parameters:
        surface (pygame varaible): Surface class objects will be placed on.
 
    '''
    for y in range(0, int(grid_height)):
        for x in range(0, int(grid_width)):
            if (x+y)%2 == 0:
                r = pygame.Rect((x*gridsize, y*gridsize), (gridsize,gridsize))
                pygame.draw.rect(surface,(85,109,169), r) 
            else:
                rr = pygame.Rect((x*gridsize, y*gridsize), (gridsize,gridsize))
                pygame.draw.rect(surface, (87, 150, 218), rr) 

def main():
    pygame.init()

    pygame.display.set_caption('Snake Walls by waveydavey')
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((screen_width, screen_height), 0, 32)

    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    drawGrid(surface)

    snake = Snake()
    food = Food()
    wall = Walls()

    myfont = pygame.font.SysFont("monospace",16)

    while (True):
        clock.tick(8)
        snake.handle_keys()
        drawGrid(surface)
        snake.move()
        if snake.get_head_position() == food.position:
            snake.length += 1
            snake.score += 1
            food.randomize_position()
        snake.draw_snake(surface)
        food.draw(surface)
        wall.draw_vertical(surface)
        wall.draw_horzitonal(surface)
        screen.blit(surface, (0,0))
        text = myfont.render("Score {0}".format(snake.score), 1, (255,255,255))
        screen.blit(text, (5,10))
        pygame.display.update()

main()
 
