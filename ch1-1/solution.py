import math

def solution(area):
    panels = []
    uncovered = area
    while uncovered > 0:
        max_size = int(math.sqrt(uncovered))
        square = max_size ** 2
        panels.append(square)
        uncovered -= square
    return panels

solution(15324)