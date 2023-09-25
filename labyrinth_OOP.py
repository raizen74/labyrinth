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
        self.horizontal = True


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
    def __init__(self, state=((0, 0), (0, 1), (0, 2)), dist=0, horizontal=True):
        self.state = state
        self.dist = dist
        self.horizontal = horizontal


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
        combined_condition = (
            lambda x: x not in visited
            and x not in single_queue
            and self.is_valid_move(x)
        )  # Not visited & not in queue & valid move

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
            for new_state in zip(
                self.next_positions(rod.state[0]),
                self.next_positions(rod.state[1]),
                self.next_positions(rod.state[2]),
            ):
                if combined_condition(new_state):
                    queue.enqueue(Rod(new_state, rod.dist + 1, rod.horizontal))
                    single_queue.add(new_state)
            new_state = self.next_rotation(rod)
            if combined_condition(new_state):
                queue.enqueue(Rod(new_state, rod.dist + 1, not rod.horizontal))
                single_queue.add(new_state)

    def next_positions(self, cell: tuple) -> tuple[tuple]:
        """
        Returns the next 4 positions (down, up, right, left) of a given cell
        """
        if cell not in self.memo.keys():
            self.memo[cell] = (
                (cell[0] + 1, cell[1]),
                (cell[0] - 1, cell[1]),
                (cell[0], cell[1] + 1),
                (cell[0], cell[1] - 1),
            )

        return self.memo[cell]

    def next_rotation(self, rod):
        if rod.horizontal:
            up = rod.state[0][0] - 1
            down = rod.state[0][0] + 1
            col = rod.state[1][1]
            return (
                (up, col),
                rod.state[1],
                (down, col),
            )  # Returns vertically aligned state
        right = rod.state[0][1] + 1
        left = rod.state[0][1] - 1
        row = rod.state[1][0]
        return (
            (row, left),
            rod.state[1],
            (row, right),
        )  # Returns horizontally aligned state

    def is_valid_move(self, positions: tuple[tuple]) -> bool:
        for pos in positions:
            if not (
                0 <= pos[0] < self.ROWS and 0 <= pos[1] < self.COLS
            ):  # Cell in matrix
                return False

            if not self.grid[pos[0]][pos[1]] == self.CLEAR:  # Cell not blocked
                return False
        return True


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
