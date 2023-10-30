from collections import defaultdict


def solution_fast(l):

    # Only want to store second level of numbers which are possibly
    # produce lucky triples. The first level is input data itself,
    # and the third level does not need to be stored as it's values
    # are irrelevant. It is sufficient to store only total count of triples.

    # Dictionary of number from the input => number of times it can be a
    # second number in a possible lucky triple identified so far.
    second_numbers = defaultdict(int)

    # Number of lucky triples identified.
    n_triples = 0

    for idx, k in enumerate(l):

        # Number of times k can be a second number in lucky triples.
        second_number = 0

        # Lookup if k can be a second number in possible lucky triples
        # by checking all known first numbers prior to k.
        # Accumulate how many such possibly triples would be.
        for first_number in l[:idx]:
            if k % first_number == 0:
                second_number += 1

        # Lookup if k can be a third number in possible lucky triples known
        # so far, by dividing it into identified second numbers.
        # Accumulate how many quantities of such triples would be.
        for second, quantity in second_numbers.items():
            if k % second == 0:
                n_triples += quantity

        # Append k to the list of identified second numbers and their
        # quantities. Increase quantity of possible triples if there was
        # the same number before.
        if second_number > 0:
            second_numbers[k] += second_number

    return n_triples


print(solution_fast([1] * 2000))

# print(solution_fast([1, 2, 3, 4, 5, 6]))
# print(solution_fast([1,1,1]))
print(solution_fast([1, 2, 3, 4, 5, 6, 7, 8, 9]))
# 124 126 128
# 136 139
# 148
# 248

# print(solution([1, 2, 3, 4, 6, 8, 9]))
# print(solution([1, 2, 2, 2]))
# 111
