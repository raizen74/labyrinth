"""
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
"""


def next_positions(cell: tuple, memo={}) -> tuple[tuple]:
    """
    Returns the next 4 positions (down, up, right, left) of a given cell
    """
    if not memo.get(cell):
        memo[cell] = (
            (cell[0] + 1, cell[1]),
            (cell[0] - 1, cell[1]),
            (cell[0], cell[1] + 1),
            (cell[0], cell[1] - 1),
        )

    return memo[cell]


def is_valid_move(
    grid: list[list[str]], positions: tuple[tuple], rows: int, cols: int
) -> bool:
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
    for pos in positions:
        if not all([0 <= pos[0] < rows, 0 <= pos[1] < cols]):  # Cell in matrix
            return False

        elif not grid[pos[0]][pos[1]] == ".":  # Cell not blocked
            return False
    return True


def rotate(
    grid: list[list[str]], rod: tuple[tuple], rows: int, cols: int
) -> tuple | None:
    """
    Change the orientation of the rod by its centered cell from horizontal to vertical
    and vice versa, when possible.

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

    rows_ = [cell[0] for cell in rod]
    cols_ = [cell[1] for cell in rod]

    if all(
        (
            (rows_[1] in range(1, rows - 1)),
            (cols_[1] in range(1, cols - 1)),
        )
    ):  # check if the central cell is not next to the wall
        if len(set(rows_)) == 1:  # check if rod is horizontal
            if all(
                (
                    (grid[rows_[0] + 1][cols_[0]] == "."),
                    (grid[rows_[1] + 1][cols_[1]] == "."),
                    (grid[rows_[2] + 1][cols_[2]] == "."),
                    (grid[rows_[0] - 1][cols_[0]] == "."),
                    (grid[rows_[1] - 1][cols_[1]] == "."),
                    (grid[rows_[2] - 1][cols_[2]] == "."),
                )
            ):  # check if cells above and under are not blocked
                return (
                    (rod[1][0] - 1, rod[1][1]),
                    rod[1],
                    (rod[1][0] + 1, rod[1][1]),
                )  # returns the vertically aligned rod

        else:  # rod is vertical
            if all(
                (
                    (grid[rows_[0]][cols_[0] + 1] == "."),
                    (grid[rows_[1]][cols_[1] + 1] == "."),
                    (grid[rows_[2]][cols_[2] + 1] == "."),
                    (grid[rows_[0]][cols_[0] - 1] == "."),
                    (grid[rows_[1]][cols_[1] - 1] == "."),
                    (grid[rows_[2]][cols_[2] - 1] == "."),
                )
            ):  # check if cells to the right and to the left are not blocked
                return (
                    (rod[1][0], rod[1][1] - 1),
                    rod[1],
                    (rod[1][0], rod[1][1] + 1),
                )  # returns the horizontally aligned rod


def solution(grid: list[list[str]]) -> int:
    """
    Perform a breadth-first search on a given grid.

    This function returns the minimal number of moves required to carry the rod through
    the labyrinth from the top left corner to the bottom right corner, if a solution exists.
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
    >>> solution(graph)
    2
    >>> no_solution_grid = [
    ...     [".",".","."],
    ...     [".",".","."],
    ...     ["#",".","."],
    ... ]
    >>> solution(no_solution_graph)
    -1
    """
    # Check correct grid type
    if not isinstance(grid, list):
        raise ValueError("Input grid must be a list of sublists of strings.")

    for sublist in grid:
        if not len(sublist) == len(grid[0]):
            raise ValueError("Each element in grid must have the same length.")

        if not isinstance(sublist, list):
            raise ValueError("Each element in grid must be a list of strings.")

        if not all(item in (".", "#") for item in sublist):
            raise ValueError("Each element in the sublists must be a '.' or '#'.")

    rows = len(grid)
    cols = len(grid[0])

    if cols < 2 | rows < 1:
        return -1
    elif any([grid[0][0] == "#", grid[0][1] == "#", grid[0][2] == "#"]):
        return -1

    queue = [((0, 0), (0, 1), (0, 2), 0)]  # [(state, distance),...]
    single_queue = {((0, 0), (0, 1), (0, 2))}  # {states in queue}
    visited = set()  # {visited states}

    while queue:  # breadth first search
        pos1, pos2, pos3, distance = queue.pop(0)  # FIFO queue
        single_queue.discard((pos1, pos2, pos3))
        visited.add((pos1, pos2, pos3))  # add rod state to visited
        if any(
            [
                pos1 == (rows - 1, cols - 1),
                pos2 == (rows - 1, cols - 1),
                pos3 == (rows - 1, cols - 1),
            ]
        ):  # if any rod cell is at lower right corner
            return distance

        # Append cells next positions to the queue IF: they are valid,
        # they are not already in the queue and haven't been visited.
        for move in zip(
            next_positions(pos1), next_positions(pos2), next_positions(pos3)
        ):
            if all(
                [
                    move not in visited,  # membership check in a set
                    move not in single_queue,  # membership check in a set
                    is_valid_move(grid, move, rows, cols),  # check if move is valid
                ]
            ):  # not visited & not in queue & valid position
                queue.append(move + (distance + 1,)), single_queue.add(move)

        if rotation := rotate(
            grid, (pos1, pos2, pos3), rows, cols
        ):  # check if rod can rotate
            if all(
                (rotation not in visited, rotation not in single_queue)
            ):  # new rotation not visited and not in queue
                queue.append((*rotation, distance + 1)), single_queue.add(rotation)

    return -1  # No valid path found


# print("Running labyrinth")
# test1 = [
#     [".", ".", ".", ".", ".", ".", ".", ".", "."],
#     ["#", ".", ".", ".", "#", ".", ".", ".", "."],
#     [".", ".", ".", ".", "#", ".", ".", ".", "."],
#     [".", "#", ".", ".", ".", ".", ".", "#", "."],
#     [".", "#", ".", ".", ".", ".", ".", "#", "."],
# ]

# print(f"Shortest path distance: {solution(test1)}")  # 11
