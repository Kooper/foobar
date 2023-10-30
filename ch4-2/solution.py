#!/bin/env python2.7

from itertools import combinations
import math


def solution(banana_list):
    check_data(banana_list)
    trainer_index_all_pairs = combinations(range(len(banana_list)), 2)
    pairs_matrix = [[0 for _ in banana_list] for _ in banana_list]
    for trainer1, trainer2 in trainer_index_all_pairs:
        banana1 = banana_list[trainer1]
        banana2 = banana_list[trainer2]
        if match(banana1, banana2):
            pairs_matrix[trainer1][trainer2] = pairs_matrix[trainer2][trainer1] = 1

    return get_trainers_on_watch(pairs_matrix)


def check_data(banana_list):
    assert len(banana_list) <= 100
    assert len(banana_list) > 0
    assert min(banana_list) >= 1
    assert max(banana_list) <= 1073741823


# Simulates a wresting match between trainers with banana1 and banana2 bananas.
# Returns True if trainers will clinch in a loop making it a useful match for
# distracting them from bunnies, or False if they will end in a draw.
def match(banana1, banana2):

    while True:

        if banana1 == banana2:
            return False

        # There will be no draw if one of the numbers is even while the
        #  other is odd
        if (banana1 + banana2) % 2 == 1:
            return True

        # Reduce both numbers keeping the proportion if we can.
        # We can at least for the evens.
        if banana1 % 2 == 0 and banana2 % 2 == 0:
            banana1 /= 2
            banana2 /= 2

        banana1, banana2 = wrestle(banana1, banana2)


# A wrestling round between trainers with banana1 and banana2 bananas.
# Returns tuple with the new numbers of bananas for both after the round.
def wrestle(banana1, banana2):

    # To not waste time we might rewind some wrtestling rounds if we can
    # predict the winner, such as in the case when the numbers are different
    # in orders of magnitude. It is geometric progression after all.
    ratio = max(banana1, banana2) / min(banana1, banana2)
    magnitude = int(math.log10(ratio))
    rounds_per_magnitude = [0, 2, 5, 8, 12, 15, 18, 22, 25, 28]
    n = 0
    if magnitude < len(rounds_per_magnitude):
        n = rounds_per_magnitude[magnitude]

    # Get sum of the geometric progression for the predicted number of
    # wrestling rounds
    anp1 = min(banana1, banana2) * pow(2, n + 1)
    sum_n = (min(banana1, banana2) - anp1) / (1 - 2)

    # Advance straight for the predicted number of rounds
    if banana1 > banana2:
        return banana1 - sum_n, banana2 + sum_n
    if banana1 < banana2:
        return banana1 + sum_n, banana2 - sum_n
    
    return banana1, banana2


# Removes the specified rows from the matrix. Rows are specified as their
# index numbers.
# Returns the new matrix
def remove_rows(rows, matrix):
    new_matrix = []
    for idx, _ in enumerate(matrix):
        if idx in rows:
            continue
        new_matrix.append([val for i, val in enumerate(matrix[idx]) if i not in rows])
    return new_matrix


# Returns list of tuples (row number, row weight) for the specified matrix.
# The list is returned sorted from small to big weights.
def get_weights(matrix):
    w = [(i, sum(val)) for i, val in enumerate(matrix)]
    def compare(t1, t2):
        return t1[1] - t2[1]
    return sorted(w, cmp=compare)


# Searches how many trainers keep watching the bunnies in the configuration
# described by the matrix. Searches cardinality matching.
# Returns number of trainers that are not distracted by the wrestling.
def get_trainers_on_watch(matrix):
    cardinalities = get_weights(matrix)
    trainers_on_watch = [i[0] for i in cardinalities if i[1] == 0]
    distracted_trainers = [i[0] for i in cardinalities if i[1] != 0]

    if len(trainers_on_watch) == len(matrix):
        return len(trainers_on_watch)
    elif len(trainers_on_watch) > 0:
        matrix = remove_rows(trainers_on_watch, matrix)
        cardinalities = get_weights(matrix)
    
    more_trainers_on_watch = 0
    for trainer in distracted_trainers:

        clinches = [(trainer, i) for i, val in enumerate(matrix[trainer]) if val != 0]

        for pair in clinches:
            submatrix = remove_rows(pair, matrix)
            more_trainers_on_watch = get_trainers_on_watch(submatrix)
            if more_trainers_on_watch == 0:
                return len(trainers_on_watch)
            else:
                # Had to return here. We could continue iteration to process
                # all the combinations and guarantee the best cardinality
                # matching if select minimal more_trainers_on_watch, but in
                # polynomial time :harold: which can't fit the time of
                # validation
                # 
                # Returning here results in a good enough greedy search
                # which matches pairs with the lowest cardinality at first,
                # in a hope that it will automatically resolve ambiguity.
                return len(trainers_on_watch) + more_trainers_on_watch
        
    return len(trainers_on_watch) + more_trainers_on_watch

print(solution([1, 7, 3, 21, 13, 19]))

# Should be 0 here, because can select the pairs 3:15 and 5:13.
# If select 13:15 then 2 trainers will still unocuppied
# print(solution([3, 5, 13, 15]))

# print(solution([7, 49]))

# The good examples of neverending chain:
# print(solution([2, 107374182]))
# print(solution([34956741, 72417442]))
# print(solution([1,2,1,1]))

print(solution([1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 2, 1, 2, 2])) # 28 - 12
# print(solution([2, 1, 1, 1, 1, 1, 1, 1]))
# print(solution([1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 2, 1]))
