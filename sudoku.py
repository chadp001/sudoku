import os
from sys import platform
import random

def instructions():
    print("Welcome to the Sudoku game!\n")
    print("To make a move, enter the row, column, and number to input separated by spaces.")
    print("For example, to enter the number 5 in row 2 column 3, type: 2 3 5\n")
    print("To solve a board type 'solve'")
    print("To quit the game type 'quit'") 


def is_valid_move(board, guess, position):
    """Check if a given number can be placed in a specific position on the board.

    Args:
        board (list): A 9x9 list representing the Sudoku board.
        guess (int): The number to check.
        position (tuple): A tuple containing the row and column indices of the position to check.

    Returns:
        bool: True if the guess is valid in the given position, False otherwise.
    """
    # Check row for duplicates
    for i in range(len(board[0])):
        if board[position[0]][i] == guess and position[1] != i:
            return False

    # Check column for duplicates
    for i in range(len(board)):
        if board[i][position[1]] == guess and position[0] != i:
            return False

    # Check 3x3 box for duplicates
    box_x = position[1] // 3
    box_y = position[0] // 3

    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if board[i][j] == guess and (i, j) != position:
                return False

    # Guess is valid if no duplicates found
    return True


def find_empty_cell(board):
    """
    Finds the next empty cell in the Sudoku board.
    Returns the row and column indices of the empty cell as a tuple, or None if no empty cells remain.
    """
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                # Return the row and column indices of an empty space
                return i, j

    # If no empty spaces remain, return None
    return None


def solve_sudoku(board):
    """
    Solve the Sudoku puzzle using a recursive backtracking algorithm.
    Returns True if a solution is found, False otherwise.
    """
    find = find_empty_cell(board)
    if not find:
        # If there are no empty spaces left, the board is solved
        return True
    else:
        row, col = find

    for guess in range(1, 10):
        if is_valid_move(board, guess, (row, col)):
            # If the guessed number is valid, make the move and continue to solve the board
            make_move(board, row, col, guess)

            if solve_sudoku(board):
                # If the board is solved, return True to end the recursive call stack
                return True
            # If the guess does not lead to a solution, backtrack and try a new guess
            make_move(board, row, col, 0)

    # If no valid guess leads to a solution, the board is unsolvable
    return False


def convert(split_data, grid_template):
    """
    Convert a list of split data into a 2D grid of integers based on a given grid template.

    Args:
    - split_data (list of str): The list of split data to be converted.
    - grid_template (list of int): The grid template that specifies the length of each row in the 2D grid.
    """
    i = 0
    for var_len in grid_template:
        yield split_data[i: i + var_len]
        i += var_len


def open_board(filename):
    """
    Opens the 'board.txt' file and reads the contents.
    Converts the contents of the file into a list of integers.
    """
    with open(filename, 'r') as file:
        # Read the contents of the file and split it into a list of strings
        board = file.read().split()

        # Convert each string in the list to an integer
        for i in range(0, len(board)):
            board[i] = int(board[i])

        # Create a grid template to be used for converting the list into a 2D grid
        grid_template = [9, 9, 9, 9, 9, 9, 9, 9, 9]

        # Convert the list of integers into a 2D grid using the grid template
        grid_data = list(convert(board, grid_template))

    # Return the converted 2D grid
    return grid_data


def make_move(grid_data, col, row, number):
    """
    Updates the value of the given cell on the board with the given number.

    Parameters:
        grid_data (list): A 2D list representing the Sudoku board.
        col (int): The column index of the cell to be updated (0-8).
        row (int): The row index of the cell to be updated (0-8).
        number (int): The number to be placed in the cell.

    Returns:
        None
    """
    grid_data[col][row] = number

    # Clear the terminal window and print the updated board
    if platform == "linux" or platform == "linux2":
        os.system('clear')
        print_board(grid_data, col, row)
        os.system('sleep 0.25')
    elif platform == "win32":
        os.system('cls')
        print_board(grid_data, col, row)
    elif platform == "darwin":
        print_board(grid_data, col, row)


def print_board(grid_data, col, row):
    """
    Prints the Sudoku board with the current state of the game.

    Args:
        grid_data (list): A 2D list of integers representing the game board.
        col (int): The column of the most recently input value.
        row (int): The row of the most recently input value.

    Returns:
        None
    """

    board_size = 13  # The size of the board including borders and dividers.
    i = 0  # Counter for the rows of the game board.
    o = -1  # Counter for the columns of the game board.
    
    for x in range(board_size):
        for y in range(board_size):
            
            if x in [0, 4, 8, 12, board_size - 1]:
                # Print a horizontal border.
                print('-', end=' ')
            elif y in [0, 4, 8, board_size - 1]:
                # Print a vertical divider.
                print('|', end=' ')
            else:
                # Print a cell value or an empty space for the cell.
                o += 1
                
                if 3 < i <= 7:
                    # Print a value for a cell in a middle box.
                    if i - 1 == col and o == row:
                        print(f'{grid_data[i - 2][o]}', end=' ')
                    else:
                        print(f'{grid_data[i - 2][o]}', end=' ')
                elif i > 7:
                    # Print a value for a cell in the bottom box.
                    if i - 2 == col and o == row:
                        print(f'{grid_data[i - 3][o]}', end=' ')
                    else:
                        print(f'{grid_data[i - 3][o]}', end=' ')
                else:
                    # Print a value for a cell in the top box.
                    if i - 1 == col and o == row:
                        print(f'{grid_data[i - 1][o]}', end=' ')
                    else:
                        print(f'{grid_data[i - 1][o]}', end=' ')
        i += 1
        o = -1
        print()
        

def generate_puzzle():
    """
    Generates a solvable Sudoku puzzle by first filling in the diagonals of the board with random valid numbers,
    then using a backtracking algorithm to fill in the rest of the board, and finally removing some numbers from
    the board to create a puzzle.

    Returns:
        list: A 9x9 list representing the Sudoku puzzle board.
    """
    # Initialize a blank board
    board = [[0 for i in range(9)] for j in range(9)]

    # Fill in the diagonals of the board with random valid numbers
    for i in range(0, 9, 3):
        nums = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        random.shuffle(nums)
        for j in range(3):
            for k in range(3):
                board[i + j][i + k] = nums.pop()

    # Use backtracking algorithm to fill in the rest of the board
    solve_sudoku(board)

    # Remove some numbers from the board to create a puzzle
    num_cells = random.randint(30, 50)
    cells_removed = 0
    while cells_removed < num_cells:
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        if board[row][col] != 0:
            board[row][col] = 0
            cells_removed += 1

    return board


def save_board(board, filename):
    """
    Save a sudoku board to a text file
    """
    with open(filename, 'w') as f:
        for row in board:
            for num in row:
                f.write(str(num) + ' ')
            f.write('\n')


def run_game():
    """
    The main function that runs the Sudoku game.
    """
    while True:
        # Display game instructions
        instructions()

        # Get user input
        user_input = input()

        if user_input.lower() == 'quit':
            break

        elif user_input.lower() == 'solve':
            # Ask user for board name or use default name
            user_input = input("\nInput the name of the Board to save(Enter blank to use default): ")
            if user_input:
                try:
                    board = open_board(user_input)
                except FileNotFoundError:
                    print("Error: Board file not found.")
                    continue
            else:
                board = open_board("board.txt")
                
            # Solve the Sudoku board
            solve_sudoku(board)
            
        elif user_input.lower() == 'play':
            # Ask user for board name or use default name
            user_input = input("\nInput the name of the Board to play(Enter blank to use default): ")
            if user_input:
                try:
                    board = open_board(user_input)
                except FileNotFoundError:
                    print("Error: Board file not found.")
                    continue
            else:
                board = open_board("board.txt")
            # Display the board and start the game
            print_board(board, 0, 0)
            while True:
                # Get user input for column, row, and number
                try:
                    col = int(input("Column: "))
                    row = int(input("Row: "))
                    number = int(input("Choose number to input: "))
                except ValueError:
                    print("Error: Invalid input. Please enter a number.")
                    continue

                # Check if the move is valid and make the move
                if is_valid_move(board, number, (row-1, col-1)):
                    make_move(board, row-1, col-1, number)
                    # print_board(board, row-1, col-1)
                else:
                    print("Invalid move, try again.")
                    
        elif user_input.lower() == 'gen':
            # Generate a new puzzle and save it to a file
            board = generate_puzzle()
            user_input = input('Name the board: ')
            if user_input:
                save_board(board, user_input)
            else:
                print("Error: Invalid board name.")
        else:
            print("Invalid input, try again.")


if __name__ == "__main__":
    run_game()