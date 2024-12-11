import random

# Initialize the grid and ship positions
GRID_SIZE = 5
player_grid = [['~'] * GRID_SIZE for _ in range(GRID_SIZE)]
ai_grid = [['~'] * GRID_SIZE for _ in range(GRID_SIZE)]
player_attack_grid = [['~'] * GRID_SIZE for _ in range(GRID_SIZE)]
ships = [(3, 'Carrier'), (2, 'Destroyer')]

# Function to place ships randomly on a grid
def place_ships(grid):
    for ship_length, name in ships:
        placed = False
        while not placed:
            direction = random.choice(['H', 'V'])
            if direction == 'H':
                row, col = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - ship_length)
                if all(grid[row][col + i] == '~' for i in range(ship_length)):
                    for i in range(ship_length):
                        grid[row][col + i] = name[0]
                    placed = True
            else:
                row, col = random.randint(0, GRID_SIZE - ship_length), random.randint(0, GRID_SIZE - 1)
                if all(grid[row + i][col] == '~' for i in range(ship_length)):
                    for i in range(ship_length):
                        grid[row + i][col] = name[0]
                    placed = True

# Function to display the grid
def display_grid(grid, title):
    print(f"\n{title}")
    print("  " + " ".join(str(i) for i in range(GRID_SIZE)))
    for i, row in enumerate(grid):
        print(f"{i} " + " ".join(row))

# AI tracking for hits and potential targets
ai_hits_stack = []  # Stack to track potential targets
current_hits = []   # List to track current hits of a ship

def ai_move(player_grid):
    global ai_hits_stack, current_hits

    # Process the stack if there are potential targets
    if ai_hits_stack:
        row, col = ai_hits_stack.pop()
        if player_grid[row][col] not in ('O', 'X'):  # Valid target
            return row, col

    # Random move as a fallback
    while True:
        row, col = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
        if player_grid[row][col] not in ('O', 'X'):  # Valid target
            return row, col

def handle_ai_hit(row, col, player_grid):
    global ai_hits_stack, current_hits

    # Add the current hit to the list
    current_hits.append((row, col))

    # If only one hit so far, add adjacent cells as potential targets
    if len(current_hits) == 1:
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE and player_grid[r][c] not in ('O', 'X'):
                ai_hits_stack.append((r, c))

    # If two hits, deduce the direction and focus on it
    elif len(current_hits) == 2:
        r1, c1 = current_hits[0]
        r2, c2 = current_hits[1]
        if r1 == r2:  # Horizontal alignment
            focus_direction = [(0, -1), (0, 1)]  # Left and right
        elif c1 == c2:  # Vertical alignment
            focus_direction = [(-1, 0), (1, 0)]  # Up and down
        else:
            return  # No clear direction yet

        # Add potential targets in the deduced direction
        for r, c in current_hits:
            for dr, dc in focus_direction:
                nr, nc = r + dr, c + dc
                if 0 <= nr < GRID_SIZE and 0 <= nc < GRID_SIZE and player_grid[nr][nc] not in ('O', 'X'):
                    ai_hits_stack.append((nr, nc))

    # If all cells in current_hits are processed, reset it
    if len(ai_hits_stack) == 0:
        current_hits.clear()

# Play the game
def play_game():
    place_ships(player_grid)
    place_ships(ai_grid)
    player_hits = 0
    ai_hits = 0
    total_ship_cells = sum(ship[0] for ship in ships)

    print("\nWelcome to Battleship!")
    while player_hits < total_ship_cells and ai_hits < total_ship_cells:
        # Display grids
        display_grid(player_grid, "Player's Grid (Your ships and AI's hits/misses)")
        display_grid(player_attack_grid, "Your Attacks on AI's Grid")

        # Player's turn
        try:
            row, col = map(int, input("Enter your attack coordinates (row col): ").split())
            if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
                if player_attack_grid[row][col] == '~':
                    if ai_grid[row][col] != '~':
                        print("You hit a ship!")
                        player_attack_grid[row][col] = 'X'  # Mark the hit
                        player_hits += 1
                    else:
                        print("You missed.")
                        player_attack_grid[row][col] = 'O'  # Mark the miss
                else:
                    print("You already attacked this spot.")
                    continue
            else:
                print("Invalid coordinates. Try again.")
                continue
        except ValueError:
            print("Please enter valid coordinates.")
            continue

        # AI's turn
        ai_row, ai_col = ai_move(player_grid)
        if player_grid[ai_row][ai_col] != '~':
            print(f"AI hits at ({ai_row}, {ai_col})!")
            player_grid[ai_row][ai_col] = 'X'  # Mark AI's hit on player's grid
            ai_hits += 1
            handle_ai_hit(ai_row, ai_col, player_grid)  # Queue potential targets
        else:
            print(f"AI misses at ({ai_row}, {ai_col}).")
            if player_grid[ai_row][ai_col] == '~':
                player_grid[ai_row][ai_col] = 'O'  # Mark AI's miss on player's grid

    # Determine the winner
    if player_hits >= total_ship_cells:
        print("Congratulations! You sunk all the AI's ships!")
    else:
        print("Game Over. The AI sunk all your ships.")

# Start the game
play_game()