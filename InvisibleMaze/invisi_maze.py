import random

def generate_maze(size):
    # Generate a random maze grid of given size
    maze = []
    for _ in range(size):
        row = []
        for _ in range(size):
            row.append("#")  # Use "#" to represent walls in the maze
        maze.append(row)
    return maze

def print_maze(maze):
    # Print the maze grid
    for row in maze:
        print(" ".join(row))

def get_clue(maze, x, y):
    # Get a clue for the player's current position in the maze
    clue = 0
    if x > 0 and maze[x - 1][y] != "#":
        clue += 1  # up cell is not a wall
    if x < len(maze) - 1 and maze[x + 1][y] != "#":
        clue += 2  # down cell is not a wall
    if y > 0 and maze[x][y - 1] != "#":
        clue += 4  # left cell is not a wall
    if y < len(maze) - 1 and maze[x][y + 1] != "#":
        clue += 8  # right cell is not a wall
    return clue

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

def play_game(size):
    maze = generate_maze(size)
    maze[0][0] = "S"  # Start position
    maze[-1][-1] = "E"  # Exit position
    if solve_maze(maze, 0, 0):
        print("Welcome to the Invisible Maze Challenge!")
        print("Find your way to the exit using the provided clues.")
        #print("Legend: '#' represents walls, ' ' represents passages, 'S' is the start, 'E' is the exit.")
        print()
        #print_maze(maze)
        print()

        x, y = 0, 0  # Player's current position
        while maze[x][y] != "E":
            clue = get_clue(maze, x, y)
            #print("Current Position: ({}, {})".format(x, y))
            if maze[x][y] != "S":
                print("Clue: {}".format(clue))
            direction = input("Enter your move (left, right, up, down): ")
            if direction == "up" and clue & 1:
                x -= 1
            elif direction == "down" and clue & 2:
                x += 1
            elif direction == "left" and clue & 4:
                y -= 1
            elif direction == "right" and clue & 8:
                y += 1
            else:
                print("Invalid move! Try again.")
            #print()
            #print_maze(maze)
            #print()

        print("Congratulations! You have reached the exit.")
        print("\nThe Maze looks like this:")
        print_maze(maze)
    else:
        print("Failed to create solution for the maze.")

# Start the game
play_game(5)
