import matplotlib.pyplot as plt
import random

def create_base_grid():
    base = 3
    side = base * base

    # Pattern for a baseline valid Sudoku solution
    def pattern(r, c):
        return (base * (r % base) + r // base + c) % side

    # Randomize rows, columns and numbers (of valid base pattern)
    def shuffle(s):
        return random.sample(s, len(s))

    rBase = range(base)
    rows = [g * base + r for g in shuffle(rBase) for r in shuffle(rBase)]
    cols = [g * base + c for g in shuffle(rBase) for c in shuffle(rBase)]
    nums = shuffle(range(1, base * base + 1))

    # Produce board using randomized baseline pattern
    board = [[nums[pattern(r, c)] for c in cols] for r in rows]
    return board

# --- Solver to check uniqueness ---
def solve_check(board):
    """
    Returns the number of solutions (stops if > 1).
    """
    find = find_empty(board)
    if not find:
        return 1
    row, col = find

    count = 0
    for i in range(1, 10):
        if is_valid(board, i, (row, col)):
            board[row][col] = i
            count += solve_check(board)
            board[row][col] = 0  # Backtrack
            if count > 1: 
                return 2  # Ambiguous puzzle
    return count

def is_valid(board, num, pos):
    # Row check
    if num in board[pos[0]]:
        return False
    # Column check
    if num in [board[i][pos[1]] for i in range(len(board))]:
        return False
    # Box check
    box_x = pos[1] // 3
    box_y = pos[0] // 3
    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x*3, box_x*3 + 3):
            if board[i][j] == num:
                return False
    return True

def find_empty(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)
    return None

def mask_grid(board):
    puzzle = [row[:] for row in board]
    side = 9
    
    # Shuffle cell coordinates to remove numbers randomly
    coords = [(r, c) for r in range(side) for c in range(side)]
    random.shuffle(coords)
    
    for r, c in coords:
        original_val = puzzle[r][c]
        puzzle[r][c] = 0  # Remove
        
        # Test if still unique
        board_copy = [row[:] for row in puzzle]
        if solve_check(board_copy) != 1:
            puzzle[r][c] = original_val  # Put back if solution not unique
            
    return puzzle

def save_sudoku_image(puzzle, filename):
    fig, ax = plt.subplots(figsize=(7, 7))

    # Draw grid lines
    for i in range(10):
        linewidth = 2.5 if i % 3 == 0 else 1.0
        # Using dark grey instead of pure black for a softer look
        ax.plot([0, 9], [i, i], color='#333333', linewidth=linewidth)
        ax.plot([i, i], [0, 9], color='#333333', linewidth=linewidth)

    # Fill numbers
    clue_count = 0
    for r in range(9):
        for c in range(9):
            val = puzzle[r][c]
            if val != 0:
                clue_count += 1
                # Text is now 'navy' blue to look like a printed puzzle clue
                ax.text(c + 0.5, 8.5 - r, str(val),
                        va='center', ha='center', fontsize=22,
                        weight='bold', family='sans-serif', color='navy')

    ax.set_xlim(0, 9)
    ax.set_ylim(0, 9)
    ax.set_aspect('equal')
    ax.axis('off')

    plt.savefig(filename, bbox_inches='tight', dpi=200, pad_inches=0.2)
    plt.close()
    return clue_count

# --- Main Execution ---
full_solution = create_base_grid()
puzzle_state = mask_grid(full_solution)

print("GTFA FULL SOLUTION GRID:")
for row in full_solution:
    print(row)

print("\nGENERATED PUZZLE GRID (0 = empty):")
for row in puzzle_state:
    print(row)

# Save the image and print stats
filename = "sudoku_variant_blue.png"
count = save_sudoku_image(puzzle_state, filename)

print(f"\nPuzzle saved to {filename}")
print(f"Clues remaining: {count}/81")
