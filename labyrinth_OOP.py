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
        self.h = horizontal


class Solution:
    def __init__(self, grid):
        self.grid = grid
        self.queue = FIFOQueue()
        self.queue.enqueue(Rod())  # FIFO queue
        self.states_queue = {((0, 0), (0, 1), (0, 2))}
        self.visited = set()
        self.memo = {}
        self.CLEAR = "."
        self.ROWS = len(self.grid)
        self.COLS = len(self.grid[0])
        self.GOAL = (self.ROWS - 1, self.COLS - 1)

    def bfs(self):  # Breadth First Search
        if self.invalid_grid():
            return -1
        while True:
            try:
                rod = self.queue.dequeue()
            except:
                return -1
            self.states_queue.discard(rod.state)
            self.visited.add(rod.state)
            for cell in rod.state:  # Memoize possible next cells
                if not self.memo.get(cell):
                    self.memo[cell] = (
                        (cell[0] + 1, cell[1]),  # Down
                        (cell[0], cell[1] + 1),  # Right
                        (cell[0] - 1, cell[1]),  # Up
                        (cell[0], cell[1] - 1),  # Left
                    )
            rod.dist += 1
            # Linear movements
            for new_state in zip(*[self.memo[state] for state in rod.state]):
                if self.valid_state(
                    new_state
                ):  # Not visited & not in queue & valid move
                    self.states_queue.add(new_state)
                    self.queue.enqueue(Rod(new_state, rod.dist, rod.h))
                    if new_state[2] == self.GOAL: # Only last cell can reach
                        return rod.dist
            # Change orientation
            new_state = (
                (self.memo[rod.state[1]][2], rod.state[1], self.memo[rod.state[1]][0])
                if rod.h  # (Up, Central, Down) vertical
                else (self.memo[rod.state[1]][3], rod.state[1], self.memo[rod.state[1]][1])
            )  # (Left, Central, Right) horizontal
            if self.valid_state(new_state) and self.valid_rotation(rod):
                self.states_queue.add(new_state)
                self.queue.enqueue(Rod(new_state, rod.dist, not rod.h))

    def valid_state(self, state):
        """
        Returns True if state is visitable, else False
        """
        if state in self.visited or state in self.states_queue:
            return
        for row, col in state:
            if (
                not (-1 < row < self.ROWS and -1 < col < self.COLS)
                or not self.grid[row][col] == self.CLEAR
            ):  # If some condition is not met return False
                return
        return True

    def valid_rotation(self, rod):
        """
        Return True if borders are CLEAR
        """
        if rod.h:
            for i in range(0, 3, 2):  # Left and Right cells in rod.state
                for j in range(0, 3, 2):  # Down and Up are 0 and 2 in memo
                    row, col = self.memo[rod.state[i]][j]
                    if self.grid[row][col] != self.CLEAR:
                        return
        else:
            for i in range(0, 3, 2):  # Up and Down cells in rod.state
                for j in range(1, 4, 2):  # Right and left are 1 and 2 in memo
                    row, col = self.memo[rod.state[i]][j]
                    if self.grid[row][col] != self.CLEAR:
                        return
        return True

    def invalid_grid(self):
        """
        Return True if grid is invalid, else None
        """
        if self.COLS < 3 or self.ROWS < 1:
            return True
        if any(
            [self.grid[0][0] == "#", self.grid[0][1] == "#", self.grid[0][2] == "#"]
        ):
            return True


if __name__ == "__main__":
    print(f"Running {__name__}")
    test1 = [
        [".", ".", ".", ".", ".", ".", ".", ".", "."],
        ["#", ".", ".", ".", "#", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "#", "#"],
        [".", "#", ".", ".", ".", ".", ".", ".", "."],
        [".", "#", ".", ".", ".", ".", ".", ".", "."],
    ]
    s = Solution(test1)
    print(f"Shortest path distance: {s.bfs()}")  # 11
