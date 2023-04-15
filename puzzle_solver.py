##############################################################################
# FILE: puzzle_solver.py
# WRITERS: Dana Aviran, 211326608, dana.av
# EXERCISE: Intro2cs2 ex8 2021-2022
# DESCRIPTION: A Puzzle Board Game - solutions using backtracking
##############################################################################

from typing import List, Tuple, Set, Optional

# We define the types of a partial picture and a constraint (for type
# checking). (I did not use them - was optional)
Picture = List[List[int]]
Constraint = Tuple[int, int, int]


def tuples_to_list(constrains):
    # this function gets a list of tuples and creates a new list that every
    # tuple is appended to it as a sub list (in order to make life easier
    # with working with the constraints)
    new_lst = []
    length = len(constrains)
    for i in range(length):
        new_lst.append([])
        new_lst[i].append(constrains[i][0])
        new_lst[i].append(constrains[i][1])
        new_lst[i].append(constrains[i][2])
    return new_lst


def set_to_list(set: Set[Constraint]) -> list:
    # this function gets a set and turns it to a list
    lst = []
    for i in set:
        lst.append(i)
    return lst


def make_board(n: int, m: int):
    # this function gets two value makes a new board - a two dimensional list
    # and inserts the value -1 to each cell
    board = []
    for i in range(n):
        board.append([])
        for j in range(m):
            board[i].append(-1)
    return board


def is_done(board):
    # this function returns True if the board is filled - has only the values
    # one and zero, and False if it has a cell that has the value -1
    height = len(board)
    width = len(board[0])
    boolean = True
    for i in range(height):
        for j in range(width):
            if board[i][j] == -1:
                boolean = False
                break
    return boolean


def normalize_board(board):
    # this function gets a board - a list of lists, and returns a new board
    # with "normalized" values - if the value is 11, replaces it with 1,
    # and if the value is 10, replaces it with 0
    height = len(board)
    width = len(board[0])
    new_board = make_board(height, width)
    for i in range(height):
        for j in range(width):
            if board[i][j] == 10:
                new_board[i][j] = 0
            elif board[i][j] == 11:
                new_board[i][j] = 1
            else:
                new_board[i][j] = board[i][j]
    return new_board


def max_seen_cells(picture: Picture, row: int, col: int) -> int:
    # this function gets a board and values of row and column, and returns the
    # number of maximum seen cells. cells with value -1 are considered as seen
    if picture[row][col] == 0:
        return 0
    else:
        height = len(picture)
        width = len(picture[0])
        counter = 1
        for i in range(row - 1, -1, -1):
            if picture[i][col] == 1 or picture[i][col] == -1:
                counter += 1
            else:
                break
        for i in range(row + 1, height):
            if picture[i][col] == 1 or picture[i][col] == -1:
                counter += 1
            else:
                break
        for i in range(col - 1, -1, -1):
            if picture[row][i] == 1 or picture[row][i] == -1:
                counter += 1
            else:
                break
        for i in range(col + 1, width):
            if picture[row][i] == 1 or picture[row][i] == -1:
                counter += 1
            else:
                break
        return counter


def min_seen_cells(picture: Picture, row: int, col: int) -> int:
    # this function gets a board and values of row and column, and returns the
    # number of minimum seen cells. cells with value -1 are considered not seen
    if picture[row][col] == 0 or picture[row][col] == -1:
        return 0
    else:
        height = len(picture)
        width = len(picture[0])
        counter = 1
        for i in range(row - 1, -1, -1):
            if picture[i][col] == 1:
                counter += 1
            else:
                break
        for i in range(row + 1, height):
            if picture[i][col] == 1:
                counter += 1
            else:
                break
        for i in range(col - 1, -1, -1):
            if picture[row][i] == 1:
                counter += 1
            else:
                break
        for i in range(col + 1, width):
            if picture[row][i] == 1:
                counter += 1
            else:
                break
        return counter


def check_constraints(picture: Picture,
                      constraints_set: Set[Constraint]) -> int:
    # this function gets a board and a set of constraints and returns 0 if the
    # constrains are not met, 1 if they are met, and 2 if they are partly met,
    # as elaborated in it
    # we turn the set of tuples to a list of lists so it will be easier
    # to work with
    constraints_list = set_to_list(constraints_set)
    constraints_num = len(constraints_list)
    height = len(picture)
    width = len(picture[0])
    boolean = True
    # we loop and check each constrain separately
    for j in range(constraints_num):
        row = constraints_list[j][0]
        col = constraints_list[j][1]
        constraint = constraints_list[j][2]
        counter = 0
        counter_empty = 0
        value = picture[row][col]
        if value == 0:
            continue
        # if the constraint is not met, we return 0
        if min_seen_cells(picture, row, col) > constraint or \
                max_seen_cells(picture, row, col) < constraint:
            return 0
        if min_seen_cells(picture, row, col) == max_seen_cells(picture, row,
                                                               col):
            continue
        # otherwise, we count the number of cells that this cell sees
        else:
            i = row - 1
            while i > -1:
                if picture[i][col] == 1:
                    counter += 1
                elif picture[i][col] == -1:
                    boolean = False
                elif picture[i][col] == 0:
                    break
                i -= 1
            for i in range(row + 1, height):
                if picture[i][col] == 1:
                    counter += 1
                elif picture[i][col] == -1:
                    boolean = False
                elif picture[i][col] == 0:
                    break
            i = col - 1
            while i > -1:
                if picture[row][i] == 1:
                    counter += 1
                elif picture[row][i] == -1:
                    boolean = False
                elif picture[row][i] == 0:
                    break
                i -= 1
            for i in range(col + 1, width):
                if picture[row][i] == 1:
                    counter += 1
                elif picture[row][i] == -1:
                    boolean = False
                elif picture[row][i] == 0:
                    break
        # if the value of cell is -1, we check:
        if value == -1:
            # if the constraint equals to the number of seen cells
            if constraint == counter:
                boolean = False  # the boolean is False, but we continue
                continue
            elif min_seen_cells(picture, row,
                                col) <= counter <= max_seen_cells(picture, row,
                                                                  col):
                boolean = False  # the boolean is False, but we continue
        # if the constraint equals to the number of seen cells
        elif value == 1:
            if constraint == counter + 1:
                continue
            elif min_seen_cells(picture, row,
                                col) <= counter + 1 <= max_seen_cells(picture,
                                                                      row,
                                                                      col):
                boolean = False  # the boolean is False, but we continue
            else:
                return 0  # else, we return 0
    if boolean:  # if boolean is True
        return 1
    else:
        return 2


def necessary_board(board, constraint_lst):
    # this function gets a board - a list of lists and a constrain list, and it
    # fills the board with the constraints that are obligatory - constrains
    # that there is only one way to implement them. these constraints are
    # zero, one and a value of maximum cells that is possible
    n = len(board)
    m = len(board[0])
    length = len(constraint_lst)
    for i in range(length):
        row = constraint_lst[i][0]
        col = constraint_lst[i][1]
        # if the constraint is 1, we insert the value 11 to the cell and insert
        # the value 10 to the cells surrounding it
        if constraint_lst[i][2] == 1:
            board[row][col] = 11
            if row != 0:
                board[row - 1][col] = 10
            if row != n - 1:
                board[row + 1][col] = 10
            if col != 0:
                board[row][col - 1] = 10
            if col != m - 1:
                board[row][col + 1] = 10
        # if the constraint is 0, we insert the value 10 to the cell
        elif constraint_lst[i][2] == 0:
            board[row][col] = 10
        else:
            # if the constraint is not one or zero, we firstly insert 11 in
            # that current cell
            board[row][col] = 11
            # and if the constraint is equal to the maximum seen cells, we
            # insert the value 11 to all cells in it's same row and column
            if constraint_lst[i][2] == max_seen_cells(normalize_board(board),
                                                      row, col):
                j = row - 1
                while j > -1:
                    if board[j][col] != 10:
                        board[j][col] = 11
                    else:
                        break
                    j -= 1
                j = row + 1
                while j < n:
                    if board[j][col] != 10:
                        board[j][col] = 11
                    else:
                        break
                    j += 1
                j = col - 1
                while j > -1:
                    if board[row][j] != 10:
                        board[row][j] = 11
                    else:
                        break
                    j -= 1
                j = col + 1
                while j < m:
                    if board[row][j] != 10:
                        board[row][j] = 11
                    else:
                        break
                    j += 1
    return board


def solve_puzzle_helper(constraints_list, board, i=0, j=0):
    # this function gets the constrain list, the board, and the starting index
    # of the first cell in the board. it will use backtracking to find a
    # possible solution to the game, while changing the board accordingly.
    # when it finds a solution, it returns the value True to the main function
    boolean = False
    # if the value of the cell is not a necessary value (has several options)
    if board[i][j] != 11 and board[i][j] != 10:
        # we loop with the value one and zero
        for k in range(0, 2):
            if boolean:
                return boolean
            # if the boolean is True, we return it
            # otherwise, we insert the value to the cell
            board[i][j] = k
            # if there aren't any cells that equal the value -1
            normalized = normalize_board(board)
            if is_done(normalized):
                # we check if the constrains are met and if they are we
                # change the value of the boolean to True and return it
                if check_constraints(normalized, constraints_list) == 1:
                    boolean = True
                    return boolean
                # if we are not in the last column, we call the function
                # and we refer in the call to the next cell of the row,
                # while the counter counts all the values to come
            if j < len(board[0]) - 1:
                boolean = solve_puzzle_helper(constraints_list, board,
                                              i, j + 1)
            # if we are not in the last row, we call the function and
            # we refer in the call to the first cell of the next row,
            # while the counter counts all the values to come
            elif i < len(board) - 1:
                boolean = solve_puzzle_helper(constraints_list, board,i + 1, 0)
        # we initialize the value of the cell to be -1 after we finished the
        # loop, so we can refer to it again the next calls
        if not boolean:
            board[i][j] = -1
    else:
        # same function calls
        if j < len(board[0]) - 1:
            boolean = solve_puzzle_helper(constraints_list, board, i, j + 1)
        elif i < len(board) - 1:
            boolean = solve_puzzle_helper(constraints_list, board, i + 1, 0)
    return boolean


def solve_puzzle(constraints_set: Set[Constraint], n: int, m: int) -> Optional[
    Picture]:
    # this function gets a set of constrains, a value of height and a value of
    # width of the game board and returns one possible solution to the game
    # we turn the set of tuples to a list of lists so it will be easier
    # to work with
    constraints_list = set_to_list(constraints_set)
    constraints_list = tuples_to_list(constraints_list)
    # we make the new board
    board = make_board(n, m)
    # we call the function make_necessary_constrains_list that makes a new
    # list of every constrain that there is just one option to implement -
    # the ones that the constrain is 0 or 1
    necessary_constraints = make_necessary_constrains_list(constraints_list,
                                                           board)
    # we firstly call the necessary_board function, that fills the board
    # with the "necessary constrains" and than call it with the rest of
    # constrains, because some of them might be also obligatory, for
    # instance if the maximum seen cells equals the constrain of the cell
    board = necessary_board(board, necessary_constraints)
    board = necessary_board(board, constraints_list)
    # we check if the board is completely full - doesn't have a cell that equal
    # zero, and if so, if it is the solution, and if it is, we return the board
    normalized = normalize_board(board)
    if is_done(normalized):
        if check_constraints(normalized, constraints_list) == 1:
            return normalized
    # otherwise,
    # we call the backtracking function - that will actually solve the game
    # and will return a True value if there is a possible solution, and change
    # the board accordingly
    boolean = solve_puzzle_helper(constraints_list, board)
    if boolean:
        return normalize_board(board)


def make_necessary_constrains_list(constraints_list, board):
    # this function gets a list of lists and a board and if the value of the
    # constrain is zero or one, it will be added to the "necessary list",
    # a list of constrains that are obligatory - that there is just one way of
    # implementing. This function also inserts the values 10 and 11 in the
    # board, equal to 0 and 1, but will be used as obligatory values in the
    # rest of the functions, to lessen the running time in case of big inputs
    necessary_list = []
    i = 0
    while i < len(constraints_list):
        if constraints_list[i][2] == 1:
            board[constraints_list[i][0]][constraints_list[i][1]] = 11
            necessary_list.append(constraints_list[i])
            constraints_list.pop(i)
            i -= 1
        elif constraints_list[i][2] == 0:
            board[constraints_list[i][0]][constraints_list[i][1]] = 10
            necessary_list.append(constraints_list[i])
            constraints_list.pop(i)
            i -= 1
        i += 1
    return necessary_list


def how_many_solutions_helper(constraints_list, board, i=0, j=0):
    # this is the helper function of the main function - it backtracks every
    # possible solution to the board and counts the number of those possible
    # solutions
    counter = 0
    # if the value of the cell is not a necessary value (has several options)
    if board[i][j] != 11 and board[i][j] != 10:
        # we loop with the value one and zero
        for k in range(0, 2):
            # and insert the value to the cell
            board[i][j] = k
            # we normalize our board
            normalized = normalize_board(board)
            # we call the is_done function that checks if there aren't any left
            # cells that equal to -1
            if is_done(normalized):
                # we check if the constrains are met, and if they do we add one
                # to the counter
                if check_constraints(normalized, constraints_list) == 1:
                    counter += 1
            # if our board is not done, and there are more values to determine
            else:
                # if we are not in the last column, we call the function and
                # we refer in the call to the next cell of the row, while the
                # counter counts all the values to come
                if j < len(board[0]) - 1:
                    counter += how_many_solutions_helper(constraints_list,
                                                         board, i, j + 1)
                # if we are not in the last row, we call the function and
                # we refer in the call to the first cell of the next row,
                # while the counter counts all the values to come
                elif i < len(board) - 1:
                    counter += how_many_solutions_helper(constraints_list,
                                                         board, i + 1, 0)
        # we initialize the value of the cell to be -1 after we finished the
        # loop, so we can refer to it again the next calls
        board[i][j] = -1
    else:
        # calling the function in the same way if the value of the cell is
        # necessary
        if j < len(board[0]) - 1:
            counter += how_many_solutions_helper(constraints_list, board, i,
                                                 j + 1)
        elif i < len(board) - 1:
            counter += how_many_solutions_helper(constraints_list, board,
                                                 i + 1, 0)
    # finally we return the counter
    return counter


def how_many_solutions(constraints_set: Set[Constraint], n: int,
                       m: int) -> int:
    # this function returns the number of solutions there are to the game
    board = make_board(n, m)
    if constraints_set:
        # we turn the set of tuples to a list of lists so it will be easier
        # to work with
        constraints_list = set_to_list(constraints_set)
        constraints_list = tuples_to_list(constraints_list)
        # we call the function make_necessary_constrains_list that makes a new
        # list of every constrain that there is just one option to implement -
        # the ones that the constrain is 0 or 1
        necessary_constraints = make_necessary_constrains_list(
            constraints_list, board)
        # we firstly call the necessary_board function, that fills the board
        # with the "necessary constrains" and than call it with the rest of
        # constrains, because some of them might be also obligatory, for
        # instance if the maximum seen cells equals the constrain of the cell
        board = necessary_board(board, necessary_constraints)
        board = necessary_board(board, constraints_list)
        # now, we call our helper backtracking function, with the new board
        num_of_solutions = how_many_solutions_helper(constraints_list, board)
    else:
        # if the constrain set is empty
        num_of_solutions = how_many_solutions_helper([], board)
    # if solved is not None, we return it - the number of solutions to the game
    if num_of_solutions:
        return num_of_solutions
    else:
        # if there is just one solution
        if solve_puzzle(constraints_set, n, m):
            return 1
        # if there aren't any
        else:
            return 0


def generate_puzzle(picture: Picture) -> Set[Constraint]:
    ...

