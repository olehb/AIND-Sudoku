from copy import copy
import random

rows = 'ABCDEFGHI'
cols = '123456789'


def cross(a, b):
    return [s + t for s in a for t in b]


boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diagonals = [[rows[i] + cols[i] for i in range(len(cols))], [rows[i]+cols[-(i+1)] for i in range(len(cols))]]
unitlist = row_units + column_units + square_units + diagonals
assignments = []

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def eliminate_twins(composite_value, unit, values):
    for box in unit:
        if values[box] != composite_value:
            for value in composite_value:
                values[box] = values[box].replace(value, '')
    return values


def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    for unit in unitlist:
        unit_values = [''.join(sorted(v)) for b, v in values.items() if b in unit]
        for uv in unit_values:
            # Supports any number of identical possible values per unit, not only twins
            # TODO: Do not eliminate same value multiple times.
            if unit_values.count(uv) == len(uv) and len(uv) > 1:
                values = eliminate_twins(uv, unit, values)
    return values


def cross(A, B):
    return [a + b for a in A for b in B]

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    default_value = '123456789'
    return {boxes[i]: grid[i] if grid[i] != '.' else default_value for i in range(len(grid))}

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    if not values:
        print("False")
        return

    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)

def eliminate(values):
    copy_values = copy(values)
    for box, value in values.items():
        if len(value) == 1:
            for unit in get_peers(box):
                for peer in unit:
                    if peer != box and len(copy_values[peer]) > 1:
                        copy_values[peer] = copy_values[peer].replace(value, '')
    return copy_values

def only_choice(values):
    copy_values = copy(values)
    for box, value in values.items():
        for unit in get_peers(box):
            peers_unique_values = {uv for uv in ''.join([copy_values[b] for b in unit if box in unit and b != box])}
            residue = set(value) - peers_unique_values
            if len(residue) == 1:
                copy_values[box] = list(residue)[0]
    return copy_values

def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        el_values = eliminate(values)
        values = only_choice(el_values)

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def get_peers(box):
    return [unit for unit in unitlist if box in unit]

def find_min_boxes(values):
    min_boxes_length = len(cols)
    min_boxes = []
    for box, value in values.items():
        if 1 < len(value) < min_boxes_length:
            min_boxes = [box]
            min_boxes_length = len(value)
        elif len(value) == min_boxes_length:
            min_boxes.append(box)
    return min_boxes

def is_solved(values):
    return values and all(len(v) == 1 for v in values.values())

def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    values = reduce_puzzle(values)
    if not values:
        return False
    if is_solved(values):
        return values
    min_boxes = find_min_boxes(values)
    probe_box = random.choice(min_boxes)
    for probe_value in values[probe_box]:
        values[probe_box] = probe_value
        probe_values = search(values)
        if is_solved(probe_values):
            return probe_values
    return False

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    return search(values)

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
