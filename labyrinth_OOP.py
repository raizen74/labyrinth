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


# class Rod:
#     def __init__(self, state=((0, 0), (0, 1), (0, 2)), dist=0, horizontal=True):
#         self.state = state
#         self.dist = dist
#         self.h = horizontal


class Solution:
    def __init__(self, grid):
        self.grid = grid
        self.queue = FIFOQueue()
        self.queue.enqueue((((0, 0), (0, 1), (0, 2)), 0, True))  # FIFO queue
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
                state, distance, horizontal = self.queue.dequeue()
            except:
                return -1
            self.states_queue.discard(state)
            self.visited.add(state)
            for cell in state:  # Memoize possible next cells
                if not self.memo.get(cell):
                    self.memo[cell] = (
                        (cell[0] + 1, cell[1]),  # Down
                        (cell[0] - 1, cell[1]),  # Up
                        (cell[0], cell[1] + 1),  # Right
                        (cell[0], cell[1] - 1),  # Left
                    )
            distance += 1
            # Linear movements
            for new_state in zip(*[self.memo[cell] for cell in state]):
                if (
                    new_state not in self.visited
                    and new_state not in self.states_queue
                    and self.valid_state(new_state, horizontal)
                ):  # Not visited & not in queue & valid move
                    self.states_queue.add(new_state)
                    self.queue.enqueue((new_state, distance, horizontal))
                    if new_state[2] == self.GOAL:  # Only reachable by last cell
                        return distance
            # Change orientation
            new_state = (
                (self.memo[state[1]][1], state[1], self.memo[state[1]][0])
                if horizontal  # (Up, Central, Down) vertical
                else (self.memo[state[1]][3], state[1], self.memo[state[1]][2])
            )  # (Left, Central, Right) horizontal
            if new_state not in self.visited and self.valid_rotation(state, horizontal):
                self.states_queue.add(new_state)
                self.queue.enqueue((new_state, distance, not horizontal))

    def valid_state(self, state, horizontal):
        """
        Returns True if state is valid, else None
        """
        if horizontal:
            if 0 <= state[2][0] <= self.GOAL[0] and 2 <= state[2][1] <= self.GOAL[1]:
                return all(self.grid[cell[0]][cell[1]] == self.CLEAR for cell in state)
        else:
            if 2 <= state[2][0] <= self.GOAL[0] and 0 <= state[2][1] <= self.GOAL[1]:
                return all(self.grid[cell[0]][cell[1]] == self.CLEAR for cell in state)

    def valid_rotation(self, state, horizontal):
        """
        Returns True if rotation is valid, else None
        """
        # Rod must not be in the border
        if 1 <= state[1][0] < self.GOAL[0] and 1 <= state[1][1] < self.GOAL[1]:
            return (
                all(
                    self.grid[self.memo[cell][u_d][0]][self.memo[cell][u_d][1]]
                    == self.CLEAR
                    for cell in state
                    for u_d in range(2)
                )  # Down and Up are 0 and 1 in memo
                if horizontal
                else all(
                    self.grid[self.memo[cell][r_l][0]][self.memo[cell][r_l][1]]
                    == self.CLEAR
                    for cell in state
                    for r_l in range(2, 4)
                )  # Right and left are 2 and 3 in memo
            )

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
    print(f"Shortest path distance: {s.bfs()}")  # 10
