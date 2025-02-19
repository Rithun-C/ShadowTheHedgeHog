import pygame
from mazelib.mazelib import Maze
from mazelib.generate.Prims import Prims
from mazelib.transmute.Perturbation import Perturbation
import time
import random

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 800
CELL_SIZE = 60
PLAYER_SIZE = CELL_SIZE - 10
SPEED = CELL_SIZE

def generate_maze():
    m = Maze()
    m.generator = Prims(5, 5)
    m.generate()
    m.transmuters = [Perturbation(repeat=1, new_walls=3)]
    m.transmute()
    return m.grid

def create_maze_walls(maze):
    return {
        (x * CELL_SIZE, y * CELL_SIZE)
        for y, row in enumerate(maze)
        for x, cell in enumerate(row) if cell == 1
    }

def set_random_endpoint(maze):
    last_two_columns = [len(maze[0]) - 2, len(maze[0]) - 1]
    possible_endpoints = [(x, y) for y in range(len(maze)) for x in last_two_columns if maze[y][x] == 0]
    return random.choice(possible_endpoints) if possible_endpoints else (len(maze[0]) - 1, len(maze) - 1)

maze = generate_maze()
maze_walls = create_maze_walls(maze)
end_x, end_y = set_random_endpoint(maze)

character_img = pygame.image.load('images/Character.png')
wall_img = pygame.image.load('images/Wall.jpg')
path_img = pygame.image.load('images/Path.png')
end_img = pygame.image.load('images/Teleport.png')
restart_img = pygame.image.load('images/Restart.png')
exit_img = pygame.image.load('images/Exit.png')
idea_img = pygame.image.load('images/Idea.png')

character_img = pygame.transform.scale(character_img, (PLAYER_SIZE, PLAYER_SIZE))
wall_img = pygame.transform.scale(wall_img, (CELL_SIZE, CELL_SIZE))
path_img = pygame.transform.scale(path_img, (CELL_SIZE, CELL_SIZE))
end_img = pygame.transform.scale(end_img, (CELL_SIZE, CELL_SIZE))
restart_img = pygame.transform.scale(restart_img, (50, 50))
exit_img = pygame.transform.scale(exit_img, (50, 50))
idea_img = pygame.transform.scale(idea_img, (50, 50))

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

    def draw(self, screen):
        screen.blit(character_img, (self.x + 5, self.y + 5))

def draw_maze(screen, offset_x, offset_y):
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            cell_position = (x * CELL_SIZE + offset_x, y * CELL_SIZE + offset_y)
            if cell == 1:
                screen.blit(wall_img, cell_position)
            elif cell == 0:
                screen.blit(path_img, cell_position)
    end_position = (end_x * CELL_SIZE + offset_x, end_y * CELL_SIZE + offset_y)
    screen.blit(end_img, end_position)

def draw_buttons(screen):
    restart_button = pygame.Rect(735, 70, 150, 50)
    idea_button = pygame.Rect(735, 120, 150, 50)
    end_button = pygame.Rect(735, 20, 150, 50)

    screen.blit(restart_img, (735, 70))
    screen.blit(exit_img, (735, 20))
    screen.blit(idea_img, (735, 120))

    return restart_button, end_button, idea_button

def game_loop():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    global maze, maze_walls, end_x, end_y

    maze_width = len(maze[0]) * CELL_SIZE
    maze_height = len(maze) * CELL_SIZE
    offset_x = (SCREEN_WIDTH - maze_width) // 2
    offset_y = (SCREEN_HEIGHT - maze_height) // 2

    player = Player(1, 1, offset_x, offset_y)

    running = True
    while running:
        screen.fill((0, 0, 0))
        draw_maze(screen, offset_x, offset_y)
        restart_button, end_button, idea_button = draw_buttons(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if restart_button.collidepoint(mouse_pos):
                    player = Player(1, 1, offset_x, offset_y)
                if end_button.collidepoint(mouse_pos):
                    running = False
                if idea_button.collidepoint(mouse_pos):
                    print("Idea button clicked!")

        keys = pygame.key.get_pressed()
        time.sleep(0.1)
        if keys[pygame.K_LEFT]: player.move(-1, 0, offset_x, offset_y)
        if keys[pygame.K_RIGHT]: player.move(1, 0, offset_x, offset_y)
        if keys[pygame.K_UP]: player.move(0, -1, offset_x, offset_y)
        if keys[pygame.K_DOWN]: player.move(0, 1, offset_x, offset_y)

        player.draw(screen)

        if (player.x - offset_x) // CELL_SIZE == end_x and (player.y - offset_y) // CELL_SIZE == end_y:
            maze = generate_maze()
            maze_walls = create_maze_walls(maze)
            end_x, end_y = set_random_endpoint(maze)
            player = Player(1, 1, offset_x, offset_y)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    game_loop()
