import pygame
from mazelib.mazelib import Maze
from mazelib.generate.Prims import Prims
from mazelib.transmute.Perturbation import Perturbation
import time

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 800
CELL_SIZE = 60
PLAYER_SIZE = CELL_SIZE - 10
SPEED = CELL_SIZE

m = Maze()
m.generator = Prims(5, 5)
m.generate()

m.transmuters = [Perturbation(repeat=1, new_walls=3)]
m.transmute()

maze = m.grid
maze_walls = {
    (x * CELL_SIZE, y * CELL_SIZE)
    for y, row in enumerate(maze)
    for x, cell in enumerate(row) if cell == 1
}

character_img = pygame.image.load('images/Character.png')
wall_img = pygame.image.load('images/Wall.jpg')
path_img = pygame.image.load('images/Path.png')

character_img = pygame.transform.scale(character_img, (PLAYER_SIZE, PLAYER_SIZE))
wall_img = pygame.transform.scale(wall_img, (CELL_SIZE, CELL_SIZE))
path_img = pygame.transform.scale(path_img, (CELL_SIZE, CELL_SIZE))

class Player:
    def __init__(self, x, y, offset_x, offset_y):
        self.x = x * CELL_SIZE + offset_x
        self.y = y * CELL_SIZE + offset_y
        self.size = PLAYER_SIZE
        self.speed = SPEED

    def move(self, dx, dy, offset_x, offset_y):
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed
        if (new_x - offset_x, new_y - offset_y) not in maze_walls:
            self.x = new_x
            self.y = new_y

    def draw(self, screen, offset_x, offset_y):
        screen.blit(character_img, (self.x + 5, self.y + 5))

def draw_maze(screen, offset_x, offset_y):
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            cell_position = (x * CELL_SIZE + offset_x, y * CELL_SIZE + offset_y)
            if cell == 1:
                screen.blit(wall_img, cell_position)
            elif cell == 0:
                screen.blit(path_img, cell_position)

def game_loop():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    maze_width = len(maze[0]) * CELL_SIZE
    maze_height = len(maze) * CELL_SIZE

    offset_x = (SCREEN_WIDTH - maze_width) // 2
    offset_y = (SCREEN_HEIGHT - maze_height) // 2

    player = Player(1, 1, offset_x, offset_y)

    running = True
    while running:
        screen.fill((0, 0, 0))
        draw_maze(screen, offset_x, offset_y)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        time.sleep(0.1)
        if keys[pygame.K_LEFT]: player.move(-1, 0, offset_x, offset_y)
        if keys[pygame.K_RIGHT]: player.move(1, 0, offset_x, offset_y)
        if keys[pygame.K_UP]: player.move(0, -1, offset_x, offset_y)
        if keys[pygame.K_DOWN]: player.move(0, 1, offset_x, offset_y)
        player.draw(screen, offset_x, offset_y)
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    game_loop()
