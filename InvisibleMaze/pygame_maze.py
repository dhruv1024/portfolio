import pygame
import random

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Initialize Pygame
pygame.init()

# Set the dimensions of the game window
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
CELL_SIZE = 40

# Set the maze size
MAZE_SIZE = 15

# Set up the game window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("The Invisible Maze Challenge")

clock = pygame.time.Clock()
font = pygame.font.Font(None, 24)

def generate_maze(size):
    # Generate a random maze grid of given size
    maze = []
    for _ in range(size):
        row = []
        for _ in range(size):
            row.append("#")  # Use "#" to represent walls in the maze
        maze.append(row)
    return maze

def solve_maze(maze, x, y):
    # Solve the maze recursively using a depth-first search algorithm
    if x < 0 or x >= len(maze) or y < 0 or y >= len(maze[0]) or maze[x][y] == ".":
        return False  # Out of bounds or already visited cell

    if maze[x][y] == "E":  # Reached the exit
        return True
    
    #print("Current position : {},{} : {}".format(x,y,maze[x][y]))
    #print_maze(maze)

    if maze[x][y] != "S":
        maze[x][y] = "."  # Mark current position as visited

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up
    random.shuffle(directions)  # Randomize the order of directions

    for dx, dy in directions:
        if solve_maze(maze, x + dx, y + dy):
            return True

    #maze[x][y] = "X"  # Dead end, mark current position as empty space
    return False

def draw_maze(maze, visibility):
    window.fill(BLACK)
    for i in range(MAZE_SIZE):
        for j in range(MAZE_SIZE):
            if maze[i][j] == "#":
                pygame.draw.rect(window, BLUE, (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            elif maze[i][j] == "S":
                pygame.draw.rect(window, GREEN, (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            elif maze[i][j] == "E":
                pygame.draw.rect(window, RED, (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            elif visibility[i][j]:
                pygame.draw.rect(window, WHITE, (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE))

"""def display_prompt(prompt):
    text = font.render(prompt, True, WHITE)
    text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 30))
    window.blit(text, text_rect)"""

def play_game():
    maze = generate_maze(MAZE_SIZE)
    maze[0][0] = "S"  # Start position
    maze[-1][-1] = "E"  # Exit position
    solve_maze(maze, 0, 0)

    visibility = [[False] * MAZE_SIZE for _ in range(MAZE_SIZE)]

    print("Welcome to the Invisible Maze Challenge!")
    print("Find your way to the exit using the provided clues.")
    print("Legend: '#' represents walls, ' ' represents passages, 'S' is the start, 'E' is the exit.")

    running = True
    visibility_revealed = False

    row, col = 0, 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if row > 0 and maze[row - 1][col] != "#":
                        visibility[row - 1][col] = True
                        check_event(row - 1, col)
                        row -= 1
                elif event.key == pygame.K_DOWN:
                    if row < MAZE_SIZE - 1 and maze[row + 1][col] != "#":
                        visibility[row + 1][col] = True
                        check_event(row + 1, col)
                        row += 1
                elif event.key == pygame.K_LEFT:
                    if col > 0 and maze[row][col - 1] != "#":
                        visibility[row][col - 1] = True
                        check_event(row, col - 1)
                        col -= 1
                elif event.key == pygame.K_RIGHT:
                    if col < MAZE_SIZE - 1 and maze[row][col + 1] != "#":
                        visibility[row][col + 1] = True
                        check_event(row, col + 1)
                        col +=1

        draw_maze(maze, visibility)
        pygame.display.flip()

        #if not visibility_revealed:
        #    pygame.time.wait(2000)  # Wait for 2 seconds to reveal the maze
        #    visibility_revealed = True

        if maze[row][col] == "E":
            print("Congratulations! You have reached the exit.")
            running = False

        clock.tick(60)

    pygame.quit()

def check_event(row, col):
    event = random.choice(["story", "enemy", "treasure"])

    if event == "story":
        print("You discover an ancient scroll that reveals a hidden clue about the maze.")
    elif event == "enemy":
        print("A fearsome enemy appears! You must defeat it to continue.")
    elif event == "treasure":
        print("You stumble upon a hidden treasure chest. What lies inside?")

# Start the game
play_game()