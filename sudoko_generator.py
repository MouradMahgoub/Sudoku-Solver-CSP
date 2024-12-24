import random
from csp import SudokuCSP

GRID_SIZE = 9


class SudokuGenerator:
    @staticmethod
    def generate_unique_solvable_sudoku(level='easy'):
        generator = SudokuGenerator()
        print("the grid is: ")
    
        grid = [[0] * 9 for _ in range(9)]
        
        generator.solve(grid)
        
        
        cells_to_remove = {
            'easy': 35,
            'medium': 45,
            'hard': 50
        }[level]
        
        generator.remove_cells(grid, cells_to_remove)
        for row in grid:
            print(row)
        return grid
    
    def is_unique_solution(self, grid):
        temp_grid = [row[:] for row in grid]
        def solve_and_count(temp_grid, count=0):
            for row in range(9):
                for col in range(9):
                    if temp_grid[row][col] == 0:
                        for num in range(1, 10):
                            if self.is_valid(temp_grid, row, col, num):
                                temp_grid[row][col] = num
                                count = solve_and_count(temp_grid, count)
                                if count > 1: return count
                                temp_grid[row][col] = 0
                        return count
            return count + 1
        return solve_and_count(temp_grid) == 1

    def remove_cells(self, grid, nums_to_remove):
        positions = [(r, c) for r in range(9) for c in range(9)]
        random.shuffle(positions)
        removed_positions = set()

        while len(removed_positions) < nums_to_remove and positions:
            pos = positions.pop()
            if pos not in removed_positions:
                r, c = pos
                number = grid[r][c]
                grid[r][c] = 0
                removed_positions.add(pos)

                if not self.is_unique_solution(grid):
                    grid[r][c] = number
                    removed_positions.remove(pos)

    def is_valid(self, grid, row, col, num):
        for x in range(9):
            if grid[row][x] == num or grid[x][col] == num:
                return False

        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for r in range(start_row, start_row + 3):
            for c in range(start_col, start_col + 3):
                if grid[r][c] == num:
                    return False
        return True

    def solve(self, grid):
        for row in range(9):
            for col in range(9):
                if grid[row][col] == 0:
                    for num in range(1, 10):
                        if self.is_valid(grid, row, col, num):
                            grid[row][col] = num
                            if self.solve(grid):
                                return True
                            grid[row][col] = 0
                    return False
        return True