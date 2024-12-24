import tkinter as tk
from tkinter import ttk, messagebox
import random
import time
from queue import Queue
import copy
from csp import SudokuCSP
from sudoko_generator import SudokuGenerator

class SudokuGUI:
    def __init__(self, root):   
        self.root = root
        self.root.title("Sudoku Solver")
        self.cells = {}
        self.mode = tk.StringVar(value="1")
        self.difficulty = tk.StringVar(value="easy")  # Add difficulty variable
        self.is_solving = False
        self.is_generating = False
        self.current_board = [[0]*9 for _ in range(9)]
        
        # Create main frame
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create left and right frames for better organization
        left_frame = ttk.Frame(self.main_frame)
        left_frame.grid(row=0, column=0, padx=10)
        
        right_frame = ttk.Frame(self.main_frame)
        right_frame.grid(row=0, column=1, padx=10, sticky=(tk.N))
        
        # Mode selection in left frame
        mode_frame = ttk.LabelFrame(left_frame, text="Mode")
        mode_frame.grid(row=0, column=0, pady=5, sticky=(tk.W, tk.E))
        
        ttk.Radiobutton(mode_frame, text="AI Solver", variable=self.mode, 
                       value="1", command=self.change_mode).grid(row=0, column=0, padx=5)
        ttk.Radiobutton(mode_frame, text="User Input", variable=self.mode,
                       value="2", command=self.change_mode).grid(row=0, column=1, padx=5)
        ttk.Radiobutton(mode_frame, text="Generate Puzzle", variable=self.mode,
                        value="3", command=self.change_mode).grid(row=0, column=2, padx=5)
        
        # Create the grid in left frame
        self.create_grid_frame(left_frame)
        
        # Buttons in left frame
        button_frame = ttk.Frame(left_frame)
        button_frame.grid(row=3, column=0, pady=10)
        
        ttk.Button(button_frame, text="Generate Puzzle", 
                  command=self.generate_puzzle).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Solve", 
                  command=self.solve).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Clear", 
                  command=self.clear_board).grid(row=0, column=2, padx=5)
        
        # Arc consistency visualization in left frame
        self.arc_frame = ttk.LabelFrame(left_frame, text="Arc Consistency Steps")
        self.arc_frame.grid(row=4, column=0, pady=10)
        self.arc_text = tk.Text(self.arc_frame, height=6, width=50)
        self.arc_text.grid(row=0, column=0, padx=5, pady=5)
        
        # Difficulty selection in right frame
        difficulty_frame = ttk.LabelFrame(right_frame, text="Difficulty Level")
        difficulty_frame.grid(row=0, column=0, pady=5, sticky=(tk.W, tk.E, tk.N))
        
        difficulties = [("Easy", "easy"), ("Medium", "medium"), ("Hard", "hard")]
        for i, (text, value) in enumerate(difficulties):
            ttk.Radiobutton(difficulty_frame, text=text, variable=self.difficulty,
                          value=value).grid(row=i, column=0, padx=10, pady=5, sticky=tk.W)

    def create_grid_frame(self, parent):
        grid_frame = ttk.Frame(parent)
        grid_frame.grid(row=1, column=0, pady=10)
    
        for i in range(9):
            for j in range(9):
                cell_frame = ttk.Frame(
                    grid_frame,
                    borderwidth=1,
                    relief="solid"
                )
                cell_frame.grid(row=i, column=j, padx=1, pady=1)
                cell = ttk.Entry(
                    cell_frame,
                    width=2,
                    justify='center',
                    font=('Arial', 18)
                )
                cell.grid(padx=2, pady=2)
                self.cells[(i, j)] = cell
                
                # Add thicker borders for 3x3 boxes
                if i % 3 == 0 and i != 0:
                    cell_frame.grid(pady=(3, 1))
                if j % 3 == 0 and j != 0:
                    cell_frame.grid(padx=(3, 1))
                
                # Bind validation for user input mode
                cell.bind('<KeyRelease>', lambda e, i=i, j=j: self.validate_input(e, i, j))


    def create_grid(self):
        grid_frame = ttk.Frame(self.main_frame)
        grid_frame.grid(row=1, column=0, columnspan=3, pady=10)
    
        for i in range(9):
            for j in range(9):
                cell_frame = ttk.Frame(
                    grid_frame,
                    borderwidth=1,
                    relief="solid"
                )
                cell_frame.grid(row=i, column=j, padx=1, pady=1)
                cell = ttk.Entry(
                    cell_frame,
                    width=2,
                    justify='center',
                    font=('Arial', 18)
                )
                cell.grid(padx=2, pady=2)
                self.cells[(i, j)] = cell
                
                # Add thicker borders for 3x3 boxes
                if i % 3 == 0 and i != 0:
                    cell_frame.grid(pady=(3, 1))
                if j % 3 == 0 and j != 0:
                    cell_frame.grid(padx=(3, 1))
                
                # Bind validation for user input mode
                cell.bind('<KeyRelease>', lambda e, i=i, j=j: self.validate_input(e, i, j))
    
    def validate_input(self, event, i, j):
        if self.mode.get() == "1":
            return
        if self.mode.get() == "2" or self.mode.get() == "3":
            cell = self.cells[(i, j)]
            value = cell.get()
            
            # Clear invalid input
            if value and (not value.isdigit() or int(value) < 1 or int(value) > 9):
                cell.delete(0, tk.END)
                return
            
            if value:
                # Check if the move is valid
                if not self.is_valid_move(i, j, int(value)):
                    cell.delete(0, tk.END)
                    messagebox.showwarning("Invalid Move", 
                        "This number violates Sudoku constraints!")
        if self.mode.get() == "3":
            #get the changed cell from GUI and compare with the current board in the same position
            #If equal, continue, else, clear the cell and generate error
            cell = self.cells[(i, j)]
            value = cell.get()
            if value:
                if self.is_complete():
                    messagebox.showwarning("Congratulations!", "you solved the puzzle Please clear the board to generate new puzzle")

                if int(value) != self.current_board[i][j]:
                    cell.delete(0, tk.END)
                    messagebox.showwarning("Not correct","This move will not lead to a solution")
            
    def is_complete(self):
        for i in range(9):
            for j in range(9):
                if self.cells[(i, j)].get() == '':
                    return False
        return True
    
    def is_valid_move(self, row, col, num):
        # Check row
        for j in range(9):
            if j != col:
                cell_value = self.cells[(row, j)].get()
                if cell_value and int(cell_value) == num:
                    return False
        
        # Check column
        for i in range(9):
            if i != row:
                cell_value = self.cells[(i, col)].get()
                if cell_value and int(cell_value) == num:
                    return False
        
        # Check 3x3 box
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if (i, j) != (row, col):
                    cell_value = self.cells[(i, j)].get()
                    if cell_value and int(cell_value) == num:
                        return False
        
        return True
    
    def change_mode(self):
        self.clear_board()
    
    def generate_puzzle(self):
        if self.is_generating:
            return
        if self.mode.get() == "2":
            return
        
        self.is_generating = True
        self.clear_board()
        
        # Update GUI with selected difficulty
        self.current_board = SudokuGenerator.generate_unique_solvable_sudoku(self.difficulty.get())
        self.update_gui_from_board()
        self.is_generating = False
        if self.mode.get() == "3":
            self.solve()
    
    def solve(self):

        if self.is_solving:
            return
            
        self.is_solving = True
        self.arc_text.delete(1.0, tk.END)
        
        # Get current board state
        board = self.get_board_from_gui()
        print("Current board:")
        for row in board:
            print(row) 

        board = SudokuCSP.solve_sudoku(board)
        if board is None:
            messagebox.showwarning("No Solution", "This Sudoku puzzle has no solution!")
            self.is_solving = False
            return
        print("Solved board:")
        for row in board:
            print(row) 
        if self.mode.get() == "3":
            self.current_board = board
        else:
            self.update_gui_from_board(board)
        self.is_solving = False

    
    
    def initialize_domains(self, board):
        domains = {}
        for i in range(9):
            for j in range(9):
                pos = (i, j)
                if board[i][j] != 0:
                    domains[pos] = {board[i][j]}
                else:
                    domains[pos] = set(range(1, 10))
        return domains
    
    def initialize_arc_queue(self):
        queue = Queue()
        for i in range(9):
            for j in range(9):
                neighbors = self.get_neighbors((i, j))
                for neighbor in neighbors:
                    queue.put(((i, j), neighbor))
        return queue
    
    def get_neighbors(self, pos):
        i, j = pos
        neighbors = set()
        
        # Row neighbors
        for col in range(9):
            if col != j:
                neighbors.add((i, col))
        
        # Column neighbors
        for row in range(9):
            if row != i:
                neighbors.add((row, j))
        
        # 3x3 box neighbors
        box_row, box_col = 3 * (i // 3), 3 * (j // 3)
        for row in range(box_row, box_row + 3):
            for col in range(box_col, box_col + 3):
                if (row, col) != pos:
                    neighbors.add((row, col))
        
        return neighbors
    
    def get_board_from_gui(self):
        board = [[0]*9 for _ in range(9)]
        for i in range(9):
            for j in range(9):
                value = self.cells[(i, j)].get()
                board[i][j] = int(value) if value else 0
        return board
    
    def update_gui_from_board(self, board=None):
        if board is None:
            board = self.current_board
        for i in range(9):
            for j in range(9):
                self.cells[(i, j)].delete(0, tk.END)
                if board[i][j] != 0:
                    self.cells[(i, j)].insert(0, str(board[i][j]))
    
    def clear_board(self):

        for cell in self.cells.values():
            cell.delete(0, tk.END)
        self.current_board = [[0]*9 for _ in range(9)]
        self.arc_text.delete(1.0, tk.END)

    def get_current_board(self):
        board = [[0 for _ in range(9)] for _ in range(9)]
        for i in range(9):
            for j in range(9):
                value = self.cells[(i, j)].get()
                board[i][j] = int(value) if value.isdigit() else 0
        return board

if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuGUI(root)
    root.mainloop()
    