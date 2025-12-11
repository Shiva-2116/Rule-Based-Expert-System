import math

import heapq

from typing import List, Tuple, Optional



Grid = List[List[int]]

Point = Tuple[int, int]



def heuristic(a: Point, b: Point, mode: str = "Manhattan") -> float:

    (x1, y1), (x2, y2) = a, b

    if mode == "Euclidean":

        return math.hypot(x2 - x1, y2 - y1)

    # default: Manhattan

    return abs(x1 - x2) + abs(y1 - y2)



def neighbors(pt: Point, grid: Grid) -> List[Point]:

    rows, cols = len(grid), len(grid[0])

    r, c = pt

    neigh = []

    for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:  # up, down, left, right

        nr, nc = r + dr, c + dc

        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 0:

            neigh.append((nr, nc))

    return neigh



def reconstruct_path(came_from: dict, current: Point) -> List[Point]:

    path = [current]

    while current in came_from:

        current = came_from[current]

        path.append(current)

    path.reverse()

    return path



def a_star(grid: Grid, start: Point, goal: Point, heuristic_mode: str = "Manhattan") -> Optional[List[Point]]:

    if grid[start[0]][start[1]] == 1 or grid[goal[0]][goal[1]] == 1:

        return None  # start or goal is a wall



    open_set = []

    heapq.heappush(open_set, (0 + heuristic(start, goal, heuristic_mode), 0, start))

    came_from = {}

    gscore = {start: 0}

    closed = set()



    while open_set:

        f, g, current = heapq.heappop(open_set)

        if current == goal:

            return reconstruct_path(came_from, current)

        if current in closed:

            continue

        closed.add(current)



        for nb in neighbors(current, grid):

            tentative_g = gscore[current] + 1  # cost between neighbors = 1

            if nb in gscore and tentative_g >= gscore[nb]:

                continue

            # better path found

            came_from[nb] = current

            gscore[nb] = tentative_g

            fscore = tentative_g + heuristic(nb, goal, heuristic_mode)

            heapq.heappush(open_set, (fscore, tentative_g, nb))



    return None



def visualize(grid: Grid, path: Optional[List[Point]], start: Point, goal: Point):

    try:

        import matplotlib.pyplot as plt

    except Exception as e:

        print("matplotlib not available — can't visualize. Install with pip install matplotlib")

        return



    rows, cols = len(grid), len(grid[0])

    img = [[0.8 if grid[r][c] == 1 else 1.0 for c in range(cols)] for r in range(rows)]

    fig, ax = plt.subplots(figsize=(cols*0.5, rows*0.5))

    ax.imshow(img, cmap="gray", origin="upper")



    # draw path

    if path:

        pr = [p[0] for p in path]; pc = [p[1] for p in path]

        ax.plot(pc, pr, linewidth=2.5, marker='o')



    # start (green) and goal (red)

    ax.scatter([start[1]], [start[0]], c='green', s=120, marker='s', label='start')

    ax.scatter([goal[1]], [goal[0]], c='red', s=120, marker='s', label='goal')



    ax.set_xticks([])

    ax.set_yticks([])

    ax.set_title("Maze A* Visualization")

    ax.legend()

    plt.gca().invert_yaxis()  # match grid row indexing

    plt.show()



def print_path_on_grid(grid: Grid, path: Optional[List[Point]], start: Point, goal: Point):

    display = [row[:] for row in grid]

    if path:

        for (r, c) in path:

            if (r, c) != start and (r, c) != goal:

                display[r][c] = 2  # path marker

    chars = {0: '.', 1: '#', 2: 'o'}

    for r in range(len(display)):

        print("".join(chars.get(display[r][c], '?') for c in range(len(display[0]))))

    print(f"Start: {start}, Goal: {goal}")

    if path:

        print("Path length:", len(path)-1)

    else:

        print("No path found (unreachable).")



def demo_example():

    # 0 = free space, 1 = wall

    grid = [

        [0,0,0,0,0,0,0],

        [0,1,1,0,1,1,0],

        [0,1,0,0,0,1,0],

        [0,1,0,1,0,1,0],

        [0,0,0,1,0,0,0],

        [0,1,0,0,0,1,0],

        [0,0,0,1,0,0,0],

    ]

    start = (0, 0)

    goal  = (6, 6)



    print("Choose heuristic: 1 = Manhattan (fast, grid), 2 = Euclidean")

choice = input("Enter 1 or 2 (default 1): ").strip()

mode = "Euclidean" if choice == "2" else "Manhattan"



# 0 = free space, 1 = wall

grid = [

    [0,0,0,0,0,0,0],

    [0,1,1,0,1,1,0],

    [0,1,0,0,0,1,0],

    [0,1,0,1,0,1,0],

    [0,0,0,1,0,0,0],

    [0,1,0,0,0,1,0],

    [0,0,0,1,0,0,0],

]

start = (0, 0)

goal  = (6, 6)



path = a_star(grid, start, goal, heuristic_mode=mode)

print_path_on_grid(grid, path, start, goal)



vis_choice = input("Show visualization? y/n (may not work on phone): ").strip().lower()

if vis_choice == 'y':

    visualize(grid, path, start, goal)




import math
import heapq
from typing import List, Tuple, Optional

# Assuming Grid and Point are defined elsewhere, or moved from cell o9TGG1Jgbn71
Grid = List[List[int]]
Point = Tuple[int, int]

def a_star_animated(grid: Grid, start: Point, goal: Point, heuristic_mode: str = "manhattan"):
    if grid[start[0]][start[1]] == 1 or grid[goal[0]][goal[1]] == 1:
        # Yield an empty state if start or goal is a wall
        yield ([], set(), {})
        return # start or goal is a wall

    open_set_heap = [] # (fscore, gscore, node)
    heapq.heappush(open_set_heap, (0 + heuristic(start, goal, heuristic_mode), 0, start))
    came_from = {}
    gscore = {start: 0}
    closed = set()

    while open_set_heap:
        # Extract open set nodes for yielding
        current_open_nodes = [node for f, g, node in open_set_heap]
        yield (current_open_nodes, set(closed), dict(came_from))

        f, g, current = heapq.heappop(open_set_heap)

        if current == goal:
            # After goal is found, yield one more time to show final state
            yield ([], set(closed), dict(came_from))
            return # Path found, stop yielding

        if current in closed:
            continue
        closed.add(current)

        for nb in neighbors(current, grid):
            tentative_g = gscore[current] + 1  # cost between neighbors = 1
            if nb in gscore and tentative_g >= gscore[nb]:
                continue
            # better path found
            came_from[nb] = current
            gscore[nb] = tentative_g
            fscore = tentative_g + heuristic(nb, goal, heuristic_mode)
            heapq.heappush(open_set_heap, (fscore, tentative_g, nb))

    # If open_set_heap becomes empty and goal not reached, no path found
    yield ([], set(closed), dict(came_from))
