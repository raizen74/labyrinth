import random
import time

from labyrinth import solution  # 29s
from labyrinth_OOP import Solution  # 28.5s

# TESTING
# Create a list of 1000 sublists, each containing 1000 binary elements
binary_data = [["." for _ in range(1000)] for i in range(1000)]

# Print the first few elements of the first few sublists for demonstration
# for i in range(10):
#     print(binary_data[i][:10])

# solution(binary_data)


impute_probability = 0
for sublist in binary_data:
    for col, _ in enumerate(sublist):
        if random.random() < impute_probability:
            # random_index = random.randint(0, len(sublist) - 1)
            sublist[col] = "#"

# Print the first few elements of the first few sublists for demonstration
for i in range(10):
    print(binary_data[i][:10])

s = Solution(binary_data)
start_time = time.time()
# print(f"Start time: {start_time:.6f}")

print(f"Shortest path distance: {s.bfs()}")  # OOP
# print(f"Shortest path distance: {solution(binary_data)}")
end_time = time.time()

execution_time = end_time - start_time
# print(f"End time: {end_time:.6f}")
print(f"Function execution time: {execution_time:.6f} seconds")
