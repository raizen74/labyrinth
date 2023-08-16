'''
Labyrinth: The goal is to carry the rod from the top left corner of the labyrinth to the bottom
right corner. 
Find the minimal number of moves required to carry the rod through the labyrinth.
The labyrinth can be represented as a rectangular matrix, some cells of which are
marked as blocked, and the rod can be represented as a 1 × 3 rectangle. The rod
can't collide with the blocked cells or the walls, so it's impossible to move it into a
position in which one of its cells coincides with the blocked cell or the wall. The goal
is thus to move the rod into position in which one of its cells is in the bottom right
cell of the labyrinth.
There are 5 types of moves that the participant can perform: move the rod one cell
down or up, to the right or to the left, or to change its orientation from vertical to
horizontal and vice versa. The rod can only be rotated about its center, and only if the
3 × 3 area surrounding it is clear from the obstacles or the walls.
The rod is initially positioned horizontally, and its left cell lies in [0, 0].

Author: David Galera
'''
def is_valid_move(grid, positions):
    """
    Check if positions is possible

    This function checks whether the provided grid and positions meet
    compatibility criteria. The grid should have List[List[str]] format, and
    positions should be an iterable of iterables, each containing 2 integers.
    Compatibility is determined based on the lengths, structure and values of the inputs.
    
    Parameters:
    grid (List[List[str]]): A list of lists containing the grid structure,
    strings in the sublists must be '.' or '#' and all sublists must be the same length.
    positions (iterable of iterables of 2 integers each):
        An iterable containing sub-iterables, each with 2 integers.
    
    Returns:
    bool: True if the grid and positions are compatible, False otherwise.

    Example:
    >>> grid = [
    ...     [".",".","."],
    ...     [".",".","."],
    ...     [".",".","."]
    ... ]
    >>> positions = ((0, 0), (1, 0), (2, 0))
    >>> is_valid_move(grid, positions)
    True
    >>> wrong_positions = ((1, 0), (2, 0), (3, 0))
    >>> is_valid_move(grid, wrong_positions)
    False
    """
        
    rows = len(grid)
    cols = len(grid[0])

    for pos in positions:
        if not (0 <= pos[0] < rows and 0 <= pos[1] < cols and grid[pos[0]][pos[1]] == "."): #Cell in matrix and not blocked
                return False
    return True 


def rotate(grid, rod):
    """
    Change the orientation of the rod by its centered cell from horizontal to vertical
    and viceversa, when possible.

    This function rotates a given rod by 90 degrees around its central cell,
    but only if compatibility criteria are met. The grid should have List[List[str]]
    format, and the rod should be an iterable of 3 iterables, each containing
    2 integers. If compatibility criteria are met, the rod rotated by 90 degrees
    around its central cell is returned; otherwise, returns None.

    Parameters:
    grid (List[List[str]]): A list of lists containing the grid structure,
    strings in the sublists must be '.' or '#' and all sublists must be the same length.
    rod (iterable of 3 iterables of 2 integers each):
        An iterable containing three sub-iterables, each with 2 integers.
    
    Returns:
    tuple of tuples or None: The rotated rod if compatible, otherwise None.

    Example:
    >>> grid = [
    ...     [".",".","."],
    ...     [".",".","."],
    ...     [".",".","."]
    ... ]
    >>> rod = ((1, 0), (1, 1), (1, 2))
    >>> rotate(grid, rod)
    ((0, 1), (1, 1), (2, 1))
    >>> incompatible_rod = ((0, 0), (0, 1), (0, 2))
    >>> rotate(grid, incompatible_rod)
    None
    """
    rows = len(grid)
    cols = len(grid[0])

    rows_ = [cell[0] for cell in rod]
    cols_ = [cell[1] for cell in rod]

    if (rows_[1] in range(1,rows-1)) and (cols_[1] in range(1,cols-1)): # check if the central cell is not next to the wall
        if len(set(rows_)) == 1: #check if rod is horizontal
            if (grid[rows_[0]+1][cols_[0]] == ".") and (grid[rows_[1]+1][cols_[1]] == ".") and \
            (grid[rows_[2]+1][cols_[2]] == ".") and (grid[rows_[0]-1][cols_[0]] == ".") and \
            (grid[rows_[1]-1][cols_[1]] == ".") and (grid[rows_[2]-1][cols_[2]] == "."): #check if cells above and under are not blocked

                return ((rod[1][0]-1, rod[1][1]), rod[1], (rod[1][0]+1, rod[1][1])) #returns the vertically aligned rod
    
        else: #rod is vertical
            if (grid[rows_[0]][cols_[0]+1] == ".") and (grid[rows_[1]][cols_[1]+1] == ".") and \
            (grid[rows_[2]][cols_[2]+1] == ".") and (grid[rows_[0]][cols_[0]-1] == ".") and \
            (grid[rows_[1]][cols_[1]-1] == ".") and (grid[rows_[2]][cols_[2]-1] == "."): #check if cells to the right and to the left are not blocked

                return ((rod[1][0], rod[1][1]-1), rod[1], (rod[1][0], rod[1][1]+1)) #returns the horizontally aligned rod

def solution(grid):
    """
    Perform a breadth-first search on a given grid.

    This function returns the minimal number of moves required to carry the rod through the labyrinth
    from the top left corner to the bottom right corner, if a solution exists.
    It performs a breadth-first search (BFS) traversal on a grid. The BFS algorithm scans
    all possible moves that the rod can perform given its current position and keeps
    track of them in a queue, scanning all possible moves from a layer before
    scanning possible moves from subsequent layers.

    Parameters:
    grid (List[List[str]]): A list of sublists containing the grid structure,
    strings in the sublists must be '.' or '#' and all sublists must be the same length.

    Returns:
    int or -1: An integer indicating the minimum number of moves or -1 if no solution is found.

    Raises:
    ValueError: If the input grid doesn't have the expected format.

    Example:
    >>> grid = [
    ...     [".",".","."],
    ...     [".",".","."],
    ...     [".",".","."],
    ... ]
    >>> solution(grid)
    2
    >>> no_solution_grid = [
    ...     [".",".","."],
    ...     [".",".","."],
    ...     ["#",".","."],
    ... ]
    >>> solution(no_solution_grid)
    -1
    """
    #Check correct grid type
    if not isinstance(grid, list):
        raise ValueError("Input grid must be a list of sublists of strings.")

    for sublist in grid:
        if not len(sublist) == len(grid[0]):
            raise ValueError("Each element in grid must have the same length.")

        if not isinstance(sublist, list):
            raise ValueError("Each element in grid must be a list of strings.")
        
        if not all(item in ('.','#') for item in sublist):
            raise ValueError("Each element in the sublists must be a '.' or '#'.")
    
    rows = len(grid)
    cols = len(grid[0])
    
    queue = [((0, 0), (0, 1), (0, 2), 0)]  # list of tuples [((row1, col1), (row2, col2), (row3, col3), distance)]
    visited = set()

    while queue: #breadth first search
        pos1, pos2, pos3, distance = queue.pop(0) #returns the first element of the list and is removed from the list
        visited.add((pos1, pos2, pos3)) #add rod position to visited
        if pos1 == (rows - 1, cols - 1) or pos2 == (rows - 1, cols - 1) or pos3 == (rows - 1, cols - 1): #if some cell is at lower right corner
            return distance
        
        # Generate next possible positions (movement) 
        next_positions = [
            ((pos[0] + 1, pos[1]) for pos in (pos1, pos2, pos3)), #generator, all cell rows +1(down)
            ((pos[0] - 1, pos[1]) for pos in (pos1, pos2, pos3)), #generator, all cell rows -1(up)
            ((pos[0], pos[1] + 1) for pos in (pos1, pos2, pos3)), #generator, all cell columns +1(right)
            ((pos[0], pos[1] - 1) for pos in (pos1, pos2, pos3)), #generator, all cell columns -1(left)
        ]
        
        # Append cells next positions to the queue IF: they are valid, they are not already in the queue and haven't been visited.
        for move in next_positions:
            state = (*move, distance + 1)
            position = state[:-1]
            if state not in queue and position not in visited and is_valid_move(grid, position): #valid position and not in queue and not visited
                queue.append(state)
        
        # IF rod can rotate and the rotation is not already in the queue and hasn't been visited, append rotation to the queue.
        rotation = rotate(grid, (pos1, pos2, pos3))
        if rotation is not None: #check valid rotation
            if ((*rotation, distance + 1) not in queue) and rotation not in visited: #new rotation not visited and not in queue
                queue.append((*rotation, distance + 1))
    
    return -1  # No valid path found
