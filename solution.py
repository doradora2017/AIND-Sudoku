from collections import Counter

assignments = []

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """
    Eliminate values using the naked twins strategy.
    go through all unit and find naked twins, if the number of boxes == the length of naked twins value, 
    eliminate other boxes using the digit in naked twins. 
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers
    for unit in unitlists:
        naked_twins_list = []
        counter = Counter([values[s] for s in unit])
        for v,cnt in counter.items():
            if cnt > 1 and len(v) == cnt:
                naked_twins_list.append([box for box in unit if values[box] == v])
        for n in naked_twins_list:
            peers = list(set(unit) - set(n))
            for p in peers:
                for digit in values[n[0]]:
                    value = values[p].replace(digit,'')
                    values = assign_value(values, p, value)
    return values

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [r + c for r in A for c in B]

#initiate units, peers, and unitlists.
rows = 'ABCDEFGHI'
cols = '123456789'
diag_units = []
boxes =  cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
col_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ['ABC', 'DEF', 'GHI'] for cs in ['123', '456', '789']]
diag_units.append([r + c for r, c in list(zip(rows, cols))])
diag_units.append([r + c for r, c in list(zip(rows, cols[::-1]))])
unitlists = row_units + col_units + square_units + diag_units
units = dict((s, [u for u in unitlists if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)


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
    digits = '123456789'
    chars = []
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81, 'The number of grid is wrong.'
    return dict(zip(boxes,chars))

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width) + ('|' if c in '36' else '') for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    """
    select the boxes which is solved, and then select the peer of every solved box, 
    eliminate the value of the peer by the value of solved box. 
    Args:A sudoku in dictionary form.
    Returns: The resulting sudoku in dictionary form.
    """
    solved_values = [box for box in boxes if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            value = values[peer].replace(digit, '') #if peer is solved_values, function return the input string
            values = assign_value(values, peer, value)
    return values
            
def only_choice(values):
    """
    go through all units, if the value is only choiced by one box in unit,
    then assign value to the box.
    Args: A sudoku in dictionary form.
    Returns: The resulting sudoku in dictionary form.
    """
    for unit in unitlists:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values = assign_value(values, dplaces[0], digit)
    return values
    
def reduce_puzzle(values):
    """
    Iterate eliminate() and only_choice()
    If at some box with on available values, return False.
    If after both function, the sudoku remain the same ,return the sudoku.
    Args:A sudoku in dictionary form.
    Returns: The resulting sudoku in dictionary form.
    """
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in boxes if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)
        solved_values_after = len([box for box in boxes if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in boxes if len(values[box]) == 0]):
            return False
    return values
    
def search(values):
    """
    Using depth-first search and propagation, create a search tree and solve the sudoku.
    if values is not available ,return False.
    Args:A sudoku in dictionary form.
    Returns: The resulting sudoku in dictionary form.
    """
    values = reduce_puzzle(values)
    if values is False:
        return False  #Failed 
    if all(len(values[box]) == 1 for box in boxes):
        return values #Solved!
    #Choose one of the unfilled box with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    #use recurrence
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)  #recurrence!
        if attempt:  # maybe False None True
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    #transfer grid from string to dict
    values = grid_values(grid)
    values = search(values)
    if values:
        return values
    else:
        print("no solution exists!")


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
