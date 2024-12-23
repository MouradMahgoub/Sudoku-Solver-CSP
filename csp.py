import copy
import time

class SudokuCSP:
    def __init__(self, board):
        self.board = board
        self.variables = []
        self.domains = {}
        self.neighbours = {}
        self.generate_variables()
        self.generate_domains()
        self.generate_neighbours()
        
        
    def generate_variables(self):
        for i in range(9):
            for j in range(9):
                self.variables.append((i, j))
                
    def generate_domains(self):
        for var in self.variables:
            i, j = var
            if self.board[i][j] == 0:
                self.domains[var] = set(range(1, 10))
            else:
                self.domains[var] = {self.board[i][j]}
            
    def generate_neighbours(self):
        for var in self.variables:
            r, c = var
            self.neighbours[var] = []
            for i in range(9):
                if i != r:
                    self.neighbours[var].append((i, c))
            for j in range(9):
                if j != c:
                    self.neighbours[var].append((r, j))
            for i in range(3 * (r // 3), 3 * (r // 3) + 3):
                for j in range(3 * (c // 3), 3 * (c // 3) + 3):
                    if i != r and j != c:
                        self.neighbours[var].append((i, j))

    def is_consistent(self, x, y):
        return x != y
        
    def is_valid(self, var, value):
        i, j = var
        for k in range(9):
            if self.board[i][k] == value or self.board[k][j] == value:
                return False
        for r in range(3 * (i // 3), 3 * (i // 3) + 3):
            for c in range(3 * (j // 3), 3 * (j // 3) + 3):
                if self.board[r][c] == value:
                    return False
        return True
    
    def is_complete(self):
        return all(len(self.domains[var]) == 1 for var in self.variables)
    
    def ac3(self, Xj):
        queue = [(Xi, Xj) for Xi in self.neighbours[Xj]]
        while queue:
            Xi, Xj = queue.pop(0)
            if self.revise(Xi, Xj):
                if len(self.domains[Xi]) == 0:
                    return False
                for Xk in self.neighbours[Xi]:
                    if Xk != Xj:
                        queue.append((Xk, Xi))
        return True       
        
        
    def revise(self, Xi, Xj):
        revised = False
        to_remove = []
        
        for x in self.domains[Xi]:
            if not any(self.is_consistent(x, y) for y in self.domains[Xj]):
                to_remove.append(x)
                revised = True
                
        for x in to_remove:
            self.domains[Xi].remove(x)
            
        return revised
    
    def select_MRV_variable(self):
        return min((var for var in self.variables if len(self.domains[var]) > 1), key=lambda var: len(self.domains[var]))

    
    def backtrack(self):
        if self.is_complete():
            return True
        
        var = self.select_MRV_variable()
        i, j = var
        
        for value in self.domains[var]:
            if self.is_valid(var, value):
                
                original_domains = copy.deepcopy(self.domains)
                old_board = copy.deepcopy(self.board)
                
                # self.board[i][j] = value
                self.domains[var] = {value}
                
                if self.ac3(var):
                    self.update_board()
                    if self.backtrack():
                        return True
                    
                self.board = old_board
                self.domains = original_domains
                
        return False
    
    
    def update_board(self):
        for var in self.variables:
            if len(self.domains[var]) == 1:
                self.board[var[0]][var[1]] = list(self.domains[var])[0]
    
    def solve(self):
        for var in self.variables:
            if len(self.domains[var]) == 1:
                if not self.ac3(var):
                        return None
        
        self.update_board()
        
        if not self.backtrack():
            return None
        
        return self.board
    
    
    
    @staticmethod
    def solve_sudoku(board):
        csp = SudokuCSP(board)
        return csp.solve()
    
    
if __name__ == "__main__":
    
    empty_board = [[9, 6, 0, 0, 0, 0, 0, 1, 0],
                    [0, 0, 0, 0, 0, 0, 8, 7, 2],
                    [3, 0, 0, 0, 0, 0, 0, 9, 0],
                    [5, 0, 4, 0, 0, 6, 0, 0, 0],
                    [0, 0, 0, 0, 0, 1, 0, 0, 8],
                    [0, 0, 0, 9, 0, 0, 4, 0, 0],
                    [0, 7, 0, 0, 8, 0, 1, 0, 0],
                    [0, 2, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 9, 2, 7, 0, 0, 0, 0]]
    # [[0 for _ in range(9)] for _ in range(9)]
    start_time = time.time()
    sol = SudokuCSP.solve_sudoku(empty_board)
    print("Time taken to solvesjjsj sudoku:", time.time() - start_time)
    # print(sol)
    
    # board_5 = [ [0, 0, 0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 2, 0], [0, 3, 0, 7, 5, 1, 0, 0, 0], [0, 0, 0, 2, 0, 0, 6, 0, 0], [0, 9, 4, 0, 6, 0, 7, 0, 0], [0, 0, 6, 1, 0, 0, 0, 0, 0], [0, 0, 0, 3, 7, 2, 0, 5, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [4, 0, 0, 0, 0, 0, 0, 0, 0] ]
    
    # board = SudokuCSP.solve_sudoku(board_5)
    
    # for i in range(9):
    #     for j in range(9):
    #         for k in range(9):
    #             if board[i][k] == board[i][j] and k != j:
    #                 print("Fail")
    #                 break
    #             if board[k][j] == board[i][j] and k != i:
    #                 print("Fail")
    #                 break
    #         for r in range(3 * (i // 3), 3 * (i // 3) + 3):
    #             for c in range(3 * (j // 3), 3 * (j // 3) + 3):
    #                 if board[r][c] == board[i][j] and r != i and c != j:
    #                     print("Fail")
    #                     break
                    
    # print("Pass")
            
    # board1 = [
    #     [5, 3, 0, 0, 7, 0, 0, 0, 0],
    #     [6, 0, 0, 1, 9, 5, 0, 0, 0],
    #     [0, 9, 8, 0, 0, 0, 0, 6, 0],
    #     [8, 0, 0, 0, 6, 0, 0, 0, 3],
    #     [4, 0, 0, 8, 0, 3, 0, 0, 1],
    #     [7, 0, 0, 0, 2, 0, 0, 0, 6],
    #     [0, 6, 0, 0, 0, 0, 2, 8, 0],
    #     [0, 0, 0, 4, 1, 9, 0, 0, 5],
    #     [0, 0, 0, 0, 8, 0, 0, 7, 9]
    # ]
    
    
    # assert SudokuCSP.solve_sudoku(board1) == [
    #     [5, 3, 4, 6, 7, 8, 9, 1, 2],
    #     [6, 7, 2, 1, 9, 5, 3, 4, 8],
    #     [1, 9, 8, 3, 4, 2, 5, 6, 7],
    #     [8, 5, 9, 7, 6, 1, 4, 2, 3],
    #     [4, 2, 6, 8, 5, 3, 7, 9, 1],
    #     [7, 1, 3, 9, 2, 4, 8, 5, 6],
    #     [9, 6, 1, 5, 3, 7, 2, 8, 4],
    #     [2, 8, 7, 4, 1, 9, 6, 3, 5],
    #     [3, 4, 5, 2, 8, 6, 1, 7, 9]
    # ]
    # print("done")
    # # Test 2
    # board_2 = [ [0, 0, 3, 0, 2, 0, 6, 0, 0], [9, 0, 0, 3, 0, 5, 0, 0, 1], [0, 0, 1, 8, 0, 6, 4, 0, 0], [0, 0, 8, 1, 0, 2, 9, 0, 0], [7, 0, 0, 0, 0, 0, 0, 0, 8], [0, 0, 6, 7, 0, 8, 2, 0, 0], [0, 0, 2, 6, 0, 9, 5, 0, 0], [8, 0, 0, 2, 0, 3, 0, 0, 9], [0, 0, 5, 0, 1, 0, 3, 0, 0] ]
    # assert SudokuCSP.solve_sudoku(board_2) == [ [4, 8, 3, 9, 2, 1, 6, 5, 7], [9, 6, 7, 3, 4, 5, 8, 2, 1], [2, 5, 1, 8, 7, 6, 4, 9, 3], [5, 4, 8, 1, 3, 2, 9, 7, 6], [7, 2, 9, 5, 6, 4, 1, 3, 8], [1, 3, 6, 7, 9, 8, 2, 4, 5], [3, 7, 2, 6, 8, 9, 5, 1, 4], [8, 1, 4, 2, 5, 3, 7, 6, 9], [6, 9, 5, 4, 1, 7, 3, 8, 2] ]
    # print("done")
    
    # # Test 3
    # board_3 = [ [0, 2, 0, 6, 0, 8, 0, 0, 0], [5, 8, 0, 0, 0, 9, 7, 0, 0], [0, 0, 0, 0, 4, 0, 0, 0, 0], [3, 7, 0, 0, 0, 0, 5, 0, 0], [6, 0, 0, 0, 0, 0, 0, 0, 4], [0, 0, 8, 0, 0, 0, 0, 1, 3], [0, 0, 0, 0, 2, 0, 0, 0, 0], [0, 0, 9, 8, 0, 0, 0, 3, 6], [0, 0, 0, 3, 0, 6, 0, 9, 0] ]
    # assert SudokuCSP.solve_sudoku(board_3) == [ [1, 2, 3, 6, 7, 8, 9, 4, 5], [5, 8, 4, 2, 3, 9, 7, 6, 1], [9, 6, 7, 1, 4, 5, 3, 2, 8], [3, 7, 2, 4, 6, 1, 5, 8, 9], [6, 9, 1, 5, 8, 3, 2, 7, 4], [4, 5, 8, 7, 9, 2, 6, 1, 3], [8, 3, 6, 9, 2, 4, 1, 5, 7], [2, 1, 9, 8, 5, 7, 4, 3, 6], [7, 4, 5, 3, 1, 6, 8, 9, 2] ]
    # print("done")
    # board_4 = [ [0, 0, 0, 6, 0, 0, 4, 0, 0],
    #             [7, 0, 0, 0, 0, 3, 6, 0, 0], 
    #             [0, 0, 0, 0, 9, 1, 0, 8, 0], 
    #             [0, 0, 0, 0, 0, 0, 0, 0, 0], 
    #             [0, 5, 0, 1, 8, 0, 0, 0, 3], 
    #             [0, 0, 0, 3, 0, 6, 0, 4, 5], 
    #             [0, 4, 0, 2, 0, 0, 0, 6, 0],
    #             [9, 0, 3, 0, 0, 0, 0, 0, 0], 
    #             [0, 2, 0, 0, 0, 0, 1, 0, 0] ]
    # start_time = time.time()
    # sol = SudokuCSP.solve_sudoku(board_4)
    # if sol is None:
    #     print("No solution")
    # else:
    #     print("Solution found!")

    # print("Time taken: ", time.time() - start_time)
    # print(sol)
    
