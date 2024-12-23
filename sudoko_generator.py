import random
from csp import SudokuCSP

GRID_SIZE = 9


def cells_to_remove(level):
    if level == 'easy':
        return 35
    elif level == 'medium':
        return 45
    elif level == 'hard':
        return 50


def is_unique_solution(grid):
    temp_grid = [row[:] for row in grid]

    def solve_and_count(temp_grid, count=0):
        for row in range(9):
            for col in range(9):
                if temp_grid[row][col] == 0:
                    for num in range(1, 10):
                        if is_valid(temp_grid, row, col, num):
                            temp_grid[row][col] = num
                            count = solve_and_count(temp_grid, count)
                            if count > 1:
                                return count
                            temp_grid[row][col] = 0
                    return count
        return count + 1

    return solve_and_count(temp_grid) == 1


def remove_cells(grid, nums_to_remove):
    positions = [(r, c) for r in range(9) for c in range(9)]
    random.shuffle(positions)
    removed_positions = set()

    while len(removed_positions) < nums_to_remove and positions:
        pos = positions.pop()
        if pos not in removed_positions:
            r = pos[0]
            c = pos[1]
            number = grid[r][c]
            grid[r][c] = 0
            removed_positions.add(pos)

            if not is_unique_solution(grid):
                grid[r][c] = number
                removed_positions.remove(pos)


def is_valid(grid, row, col, num):
    for c in range(GRID_SIZE):
        if grid[row][c] == num:
            return False

    for r in range(GRID_SIZE):
        if grid[r][col] == num:
            return False

    subgrid_row_start = (row // 3) * 3
    subgrid_col_start = (col // 3) * 3
    for r in range(subgrid_row_start, subgrid_row_start + 3):
        for c in range(subgrid_col_start, subgrid_col_start + 3):
            if grid[r][c] == num:
                return False

    return True


def solve(grid):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if grid[row][col] == 0:
                numbers = list(range(1, 10))
                random.shuffle(numbers)

                for num in numbers:
                    if is_valid(grid, row, col, num):
                        grid[row][col] = num
                        if solve(grid):
                            return True
                        grid[row][col] = 0  # backtrack

                return False
    return True


def generate_unique_solvable_sudoku(level='easy'):
    grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
    solve(grid)  # generate a solved sudoku grid

    no_of_removed_cells = cells_to_remove(level)
    remove_cells(grid, no_of_removed_cells)

    return grid


grid = generate_unique_solvable_sudoku('hard')
for row in grid:
    print(row)

print(is_unique_solution(grid))
print(solve(grid))

flag = True

csp = SudokuCSP(grid)
sol = csp.solve()
# check sol
for i in range(9):
    for j in range(9):
        for k in range(9):
            if sol[i][k] == sol[i][j] and k != j:
                print("Fail")
                flag = False
                break
            if sol[k][j] == sol[i][j] and k != i:
                print("Fail")
                flag = False
                break
        for r in range(3 * (i // 3), 3 * (i // 3) + 3):
            for c in range(3 * (j // 3), 3 * (j // 3) + 3):
                if sol[r][c] == sol[i][j] and r != i and c != j:
                    print("Fail")
                    flag = False
                    break

for row in sol:
    print(row)

if flag:
    print("Pass")
