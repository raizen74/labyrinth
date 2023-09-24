"""
Coded with OOP

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


# Implementation of a FIFO Queue using a linked list
class Node:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next


class FIFOQueue:
    def __init__(self):
        self._head = None
        self._tail = None
        # self._size = 0

    def enqueue(self, item):
        if not self._head:
            self._tail = self._head = Node(
                value=item
            )  # If the queue is empty, initialize.
        # If queue is not empty, append node at the end
        else:
            self._tail.next = Node(value=item)  # Change attr of the tail
            self._tail = self._tail.next  # Refresh the tail node

        # self._size += 1

    def dequeue(self):
        if not self._head:
            raise IndexError  # Removing an item from empty queue: ERROR
        value = self._head.value  # Get the front node
        self._head = self._head.next  # Set the next node in front as head

        # self._size -= 1

        return value


class Rod:
    def __init__(self, state=((0, 0), (0, 1), (0, 2)), dist=0):
        self.state = state
        self.dist = dist


class Solution:
    def __init__(self, grid):
        self.grid = grid
        self.rod = Rod()
        self.memo = {}
        self.CLEAR = "."
        self.ROWS = len(self.grid)
        self.COLS = len(self.grid[0])
        self.GOAL = (self.ROWS - 1, self.COLS - 1)

    def valid_grid(self):
        if self.COLS < 2 | self.ROWS < 1:
            return -1
        if any(
            [self.grid[0][0] == "#", self.grid[0][1] == "#", self.grid[0][2] == "#"]
        ):
            return -1

    def bfs(self):  # Breadth First Search
        if self.valid_grid() == -1:
            return -1
        queue = FIFOQueue()
        queue.enqueue(self.rod)
        single_queue = {self.rod.state}
        visited = set()
        while True:
            try:
                rod = queue.dequeue()  # FIFO queue
            except IndexError:
                return -1

            single_queue.discard(rod.state)
            visited.add(rod.state)
            if any(
                [
                    rod.state[0] == self.GOAL,
                    rod.state[1] == self.GOAL,
                    rod.state[2] == self.GOAL,
                ]
            ):  # If any rod cell is at lower right corner
                return rod.dist
            for move in zip(
                self.next_positions(rod.state[0]),
                self.next_positions(rod.state[1]),
                self.next_positions(rod.state[2]),
            ):
                if all(
                    [
                        move not in visited,  # Membership check in a set
                        move not in single_queue,  # Membership check in a set
                        self.is_valid_move(move),  # Check if move is valid
                    ]
                ):
                    queue.enqueue(Rod(move, rod.dist + 1))
                    single_queue.add(move)
            if rotation := self.rotate(rod.state):
                if all(
                    [rotation not in visited, rotation not in single_queue]
                ):  # Not visited & not in queue
                    queue.enqueue(Rod(rotation, rod.dist + 1))
                    single_queue.add(rotation)

    def next_positions(self, cell: tuple) -> tuple[tuple]:
        """
        Returns the next 4 positions (down, up, right, left) of a given cell
        """
        if not self.memo.get(cell):
            self.memo[cell] = (
                (cell[0] + 1, cell[1]),
                (cell[0] - 1, cell[1]),
                (cell[0], cell[1] + 1),
                (cell[0], cell[1] - 1),
            )

        return self.memo[cell]

    def is_valid_move(self, positions: tuple[tuple]) -> bool:
        for pos in positions:
            if not all(
                [0 <= pos[0] < self.ROWS, 0 <= pos[1] < self.COLS]
            ):  # Cell in matrix
                return False

            if not self.grid[pos[0]][pos[1]] == self.CLEAR:  # Cell not blocked
                return False
        return True

    def rotate(self, state) -> tuple | None:
        rows_, cols_ = list(zip(*(state)))

        if not all(
            ([0 < rows_[1] < self.GOAL[0], 0 < cols_[1] < self.GOAL[1]])
        ):  # Check if the central cell is not next to the wall
            return

        if len(set(rows_)) == 1:  # check if rod is horizontal
            up = rows_[1] + 1
            down = rows_[1] - 1
            if all(
                self.grid[up][col] == self.grid[down][col] == self.CLEAR
                for col in cols_
            ):
                return (
                    (down, cols_[1]),
                    state[1],
                    (up, cols_[1]),
                )  # Returns vertically aligned state
            return

        right = cols_[1] + 1
        left = cols_[1] - 1

        if all(
            self.grid[row][right] == self.grid[row][left] == self.CLEAR for row in rows_
        ):
            return (
                (rows_[1], left),
                state[1],
                (rows_[1], right),
            )  # Returns horizontally aligned state


if __name__ == "__main__":
    print(f"Running {__name__}")
    test1 = [
        [".", ".", ".", ".", ".", ".", ".", ".", "."],
        ["#", ".", ".", ".", "#", ".", ".", ".", "."],
        [".", ".", ".", ".", "#", ".", ".", ".", "."],
        [".", "#", ".", ".", ".", ".", ".", "#", "."],
        [".", "#", ".", ".", ".", ".", ".", "#", "."],
    ]
    s = Solution(test1)
    print(f"Shortest path distance: {s.bfs()}")  # 11
