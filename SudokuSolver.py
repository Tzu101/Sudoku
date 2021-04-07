import copy

# Sudoku solving program
class SudokuSolver:

    empty_board = [ [0, 0, 0, 0, 0, 0, 0, 0, 0], 
                    [0, 0, 0, 0, 0, 0, 0, 0, 0], 
                    [0, 0, 0, 0, 0, 0, 0, 0, 0], 
                    [0, 0, 0, 0, 0, 0, 0, 0, 0], 
                    [0, 0, 0, 0, 0, 0, 0, 0, 0], 
                    [0, 0, 0, 0, 0, 0, 0, 0, 0], 
                    [0, 0, 0, 0, 0, 0, 0, 0, 0], 
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0]]

    # Initilizes variables
    def __init__(self):

        self.board = copy.deepcopy(SudokuSolver.empty_board)
        self.solutions = 0
        self.max_solutions = 10
        self.solved_boards = []

    # Resets values
    def reset(self):

        self.__init__()


    # Checks if a row fits sudoku rules
    def check_row(self, row):
        
        nums = []
        for num in self.board[row]:

            if num != 0:
                if num not in nums:
                    nums.append(num)
                else:
                    return False

        return True

    # Checks if a column fits sudoku rules
    def check_column(self, column):
        
        nums = []
        for n in range(9):

            num = self.board[n][column]

            if num != 0:
                if num not in nums:
                    nums.append(num)
                else:
                    return False

        return True

    # Checks if a grid fits sudoku rules
    def check_grid(self, gx, gy):
        
        nums = []
        for y in range(3):
            for x in range(3):

                num = self.board[gy * 3 + y][gx * 3 + x]

                if num != 0:
                    if num not in nums:
                        nums.append(num)
                    else:
                        return False

        return True

    # Checks if a newly added cell fits sudoku rules
    def check_cell(self, x, y):

        return self.check_row(y) and self.check_column(x) and self.check_grid(x // 3, y // 3)

    # Checks if the board fits sudoku rules
    def check_board(self):

        fits = True
        
        for row in range(9):
            fits = fits and self.check_row(row)

        for column in range(9):
            fits = fits and self.check_column(column)

        for y in range(3):
            for x in range(3):
                fits = fits and self.check_grid(x, y)

        return fits

    def count_empty(self):

        count = 0

        for y in range(9):
            for x in range(9):
                if self.board[y][x] == 0:
                    count += 1

        return count

    # Starts solving if the board is valid
    def solve(self):
        
        if not self.check_board() or self.count_empty() == 81:
            return
        else:
            self.solve_board()

    # Finds up to the specefied number of solutions
    def solve_board(self, start=0):

        for i in range(start, 81):

            x = i % 9
            y = i // 9

            if self.board[y][x] == 0:

                for n in range(1, 9+1):

                    self.board[y][x] = n
                    if self.check_cell(x, y):
                        if self.solve_board(start+1):
                            return True

                self.board[y][x] = 0
                return False
                
            elif x == 8 and y == 8:
                
                self.solutions += 1
                self.solved_boards.append(copy.deepcopy(self.board))
                if self.solutions >= self.max_solutions:
                    return True
                return False
