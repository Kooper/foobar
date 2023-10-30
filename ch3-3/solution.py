from itertools import chain
from collections import deque


def solution(m):
    height = len(m)
    width = len(m[0])

    # Sanity checks.
    if not 2 <= height <= 20 or not 2 <= width <= 20:
        return None

    start = (0, 0)
    escape = (height - 1, width - 1)

    # The shortest path length for cardinal moves.
    absolute_min = height + width - 1

    # May estimate longest path as number of nodes in labyrinth.
    current_min = height * width

    # Will search shortest escape path among labyrinths, which
    # are made of original labyrinth with wall removed. Will iterate over
    # all existing walls.
    # Add unmodified labyrinth to consideration by placing fake wall at start
    # position (start and end positions are always passable). Removing this
    # wall will produce the original maze at first iteration.
    for wall in chain([start], walls(m)):

        remodelled = destroy_wall(m, wall)
        moves = map2moves(remodelled)

        length = find_path_len(moves, start, escape, current_min)

        if length == absolute_min:
            # Won't find any shorter.
            return absolute_min

        if length is not None:
            current_min = min(current_min, length)

    return current_min


def map2moves(m):
    """
    Returns all passable nodes and corresponding moves in cardinal
    directions, which can be made from the nodes.
    """
    height = len(m)
    width = len(m[0])
    moves = {}

    # Traverse all nodes to define available moves from each one.
    for row in range(0, height):
        for col in range(0, width):

            # This location is a wall, no moves are available from it.
            if m[row][col] != 0:
                continue

            raw_neighbours = [
                (row - 1, col),
                (row + 1, col),
                (row, col - 1),
                (row, col + 1),
            ]

            actual_neighbours = [node for node in raw_neighbours
                          if 0 <= node[0] < height and 0 <= node[1] < width]

            # Nodes which are available for moves from the current node.
            moves[(row, col)] = [node for node in actual_neighbours
                                 if m[node[0]][node[1]] == 0]

    return moves


def walls(m):
    """
    Returns iterator enumerating all walls in the map m
    """
    height = len(m)
    width = len(m[0])
    for row in range(0, height):
        for column in range(0, width):
            if m[row][column] != 0:
                yield row, column


def destroy_wall(m, wall):
    """
    Returns copy of map m with specific wall removed
    """
    plan = map(list, m)
    plan[wall[0]][wall[1]] = 0
    return plan


def find_path_len(moves, start, end, max_len):
    """
    Finds shortest path length from start to end using breadth-first search.
    max_len specifies maximum length to search.
    Returns length of path found or None if no path exists or max_len
    is reached.
    """
    path_len_to = {start: 1}
    search_from = deque([start])

    while len(search_from):
        node = search_from.popleft()
        if node == end:
            return path_len_to[node]

        for neighbour in moves[node]:
            if neighbour not in path_len_to:
                path_len_to[neighbour] = path_len_to[node] + 1

                # Do not consider paths longer then max_len
                if path_len_to[neighbour] < max_len:
                    search_from.append(neighbour)

    return path_len_to.get(end)


print solution([
    [0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1],
    [0, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0]])
print solution([
    [0, 1, 1, 0],
    [0, 0, 0, 1],
    [1, 1, 0, 0],
    [1, 1, 1, 0]])
print solution([
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 0, 0, 0],
    [1, 1, 0, 1, 1, 0, 0, 0],
    [1, 1, 0, 1, 1, 1, 1, 1],
    [0, 0, 0, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
])

print solution([
    [0, 0],
    [0, 0],
])
