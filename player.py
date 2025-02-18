import pygame

# Define constants
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600
CELL_SIZE = 40  # Each grid cell is 40x40 pixels
PLAYER_SIZE = CELL_SIZE - 10  # Player size slightly smaller than a cell
SPEED = CELL_SIZE  # Move by one cell at a time

# Define a simple dummy maze as a 2D grid (1 = wall, 0 = open path)
DUMMY_MAZE = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 0, 1, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
    [1, 1, 1, 1, 1, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# Convert the maze into a set of blocked positions
maze_walls = {
    (x * CELL_SIZE, y * CELL_SIZE)
    for y, row in enumerate(DUMMY_MAZE)
    for x, cell in enumerate(row) if cell == 1
}

class Player:
    def __init__(self, x, y):
        """Initializes the player at a given grid position."""
        self.x = x * CELL_SIZE
        self.y = y * CELL_SIZE
        self.size = PLAYER_SIZE
        self.speed = SPEED
        self.color = (0, 255, 0)  # Green player

    def move(self, dx, dy):
        """Moves the player, checking for collisions."""
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed

        if (new_x, new_y) not in maze_walls:  # Check collision
            self.x = new_x
            self.y = new_y

    def draw(self, screen):
        """Draws the player on the screen."""
        pygame.draw.rect(screen, self.color, (self.x + 5, self.y + 5, self.size, self.size))

def draw_maze(screen):
    """Draws the maze walls."""
    for wall in maze_walls:
        pygame.draw.rect(screen, (200, 200, 200), (wall[0], wall[1], CELL_SIZE, CELL_SIZE))

def game_loop():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    # Initialize player at an open path (1,1)
    player = Player(1, 1)

    running = True
    while running:
        screen.fill((0, 0, 0))  # Clear screen
        draw_maze(screen)  # Draw maze walls
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Movement handling
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: player.move(-1, 0)
        if keys[pygame.K_RIGHT]: player.move(1, 0)
        if keys[pygame.K_UP]: player.move(0, -1)
        if keys[pygame.K_DOWN]: player.move(0, 1)

        # Draw player
        player.draw(screen)
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    game_loop()
