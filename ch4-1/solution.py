from itertools import permutations


def solution(times, time_limit):

    # Sanity checks
    n = len(times)
    if n < 5:
        return []

    # Complete set of bunnies to save
    bunnies = range(n - 2)

    real_times = get_shortest_paths(times)
    if not real_times:
        # Negative cycle detected. It means we may gain infinite
        # time following the path in a loop. This in turn allows
        # us to save complete set of bunnies having enough
        # time for anything.
        return bunnies

    # We are going to brute-force all possible escape paths, with various
    # combinations of bunnies.
    bunnies_variations = get_bunnies_variations(bunnies)

    start = 0
    bulkhead = n - 1
    best_saved_bunnies = []

    # Search shortest path between start, various sets of bunnies and
    # bulkhead positions using the computed shortest paths.
    for save_plan in bunnies_variations:

        # No need to consider plans worse than the known one.
        if not is_better_plan(best_saved_bunnies, save_plan):
            continue

        time_left = time_limit
        prev = start
        for bunny_worker_id in save_plan:
            coordinate = bunny_worker_id + 1
            time_left -= real_times[prev][coordinate]
            prev = coordinate

        # With all the planned bunnies in hands we are heading to bulkhead
        # to see if it's still open
        time_left -= real_times[prev][bulkhead]

        if time_left >= 0:
            # Still open, let's escape! New set of saved bunnies is
            # better than previous one, so arrange them for the answer.
            save_plan.sort()
            best_saved_bunnies = save_plan

    return best_saved_bunnies


def is_better_plan(old, new):
    """
    Returns True if new plan can be preferred over the old one. It may
    contain more bunnies, or save bunnies with lower worker IDs.
    """
    if len(new) < len(old):
        return False
    if len(new) > len(old):
        return True
    # Equal number of saved bunnies. Prefer the one with
    # lowest worker IDs (as indexes) in sorted order.
    # Old one is already sorted, new one is not yet.
    new_sorted = new[:]
    new_sorted.sort()
    return new_sorted < old


def get_shortest_paths(times):
    """
    Returns adjacency matrix with weights updated according to computed
    shortest paths among supplied times. Returns False if there is a negative
    cycle detected.

    Uses Floyd-Warshall algorithm to compute shortest paths between each
    position in supplied adjacency matrix and discover negative cycles.
    """
    n = len(times)
    shortest = times[:]
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if shortest[i][j] > shortest[i][k] + shortest[k][j]:
                    shortest[i][j] = shortest[i][k] + shortest[k][j]
                if shortest[j][j] < 0:
                    # Negative cycle detected.
                    return False
    return shortest


def get_bunnies_variations(bunnies):
    """
    Returns list of all possible combinations of bunnies to save,
    decreasing in number of saved individuals. Thus first variations
    in list will have the maximum value.
    BTW do not consider empty list - it is a default worst case answer.
    """
    bunnies_variations = []
    for n_bunnies_to_save in range(len(bunnies), 0, -1):
        for variant in permutations(bunnies, n_bunnies_to_save):
            bunnies_variations.append(list(variant))
    return bunnies_variations

# solution([
#    [0, 2, 2, 2, -1],
#    [9, 0, 2, 2, -1],
#    [9, 3, 0, 2, -1],
#    [9, 3, 2, 0, -1],
#    [9, 3, 2, 2, 0]
# ], 1)
# [1, 2]
#

# Infinite negative cycle
# solution([
#     [0, 2, 2, 2, -1],
#     [9, 0, 2, 2, 0],
#     [9, 3, 0, 2, 0],
#     [9, 3, 2, 0, 0],
#     [-1, 3, 2, 2, 0]
# ], -100)

print solution([
   [0, 1, 1, 1, 1],
   [1, 0, 1, 1, 1],
   [1, 1, 0, 1, 1],
   [1, 1, 1, 0, 1],
   [1, 1, 1, 1, 0]
], 3)
# [0, 1]
# 0 -> (1) -> 1 => [2]
# 1 -> (1) -> 4 => [1]
# 4 -> (1) -> 2 => [0]
# 2 -> (1) -> 4 => [-1]
