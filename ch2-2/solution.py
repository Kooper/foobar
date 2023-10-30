from __future__ import print_function

import itertools


def solution(h, q):
    # Going from bottom levels up to the root, computing flux numbers.
    # If encounter number from q - remember coordinates of it's root.
    # If travers one of remembered coordinates - get it's value into the result.
    coordinates = [(-1, -1) for _ in q]

    # Defaults result to -1
    result = [-1 for _ in q]

    # Set is used for faster element presence checking
    q_set = set(q)

    # Traversing tree from bottom up.
    for current_level in range(h, 0, -1):

        # The flux converter tree resembles geometric progression.
        # Sum of progression is number of elements in subtree.
        subtree_elements_number = 2 ** (h - current_level + 1) - 1

        # Boundaries of subtrees are easily detectable as powers of two.
        # Number of subtrees matches level.
        subtrees_boundaries = [2**n for n in range(1, current_level - 1)]
        subtrees_boundaries.reverse()

        # Each level contains number of elements equal to current progression level.
        width = 2**(current_level-1)

        # First element in a row equal to number of elements in subtree.
        next_precomputed_value = subtree_elements_number

        # itertools is used because range can't allocate lists big enough
        # for large levels.
        for e in itertools.islice(itertools.count(1), width):
            number = next_precomputed_value

            # Next value in a row accumulates the whole subtree
            next_precomputed_value += subtree_elements_number

            # Define if next element would cross a subtree boundary
            for u in subtrees_boundaries:
                # When crossing subtree boundary next value in a row
                # must accumulate values of root subtree nodes.
                if e % u == 0:
                    # The number of such nodes matches position of subtree
                    # boundary index.
                    next_precomputed_value += \
                        len(subtrees_boundaries) - subtrees_boundaries.index(u)
                    break

            # When number is among target numbers, remember coordinates
            # of it's root flux converter.
            if number in q_set:
                idx = q.index(number)
                root = e / 2 + e % 2
                coordinates[idx] = (current_level - 1, root)

            # When current coordinate is among coordinates of parent
            # flux converters to search - remember value of the flux converter.
            if (current_level, e) in coordinates:
                idx = coordinates.index((current_level, e))
                result[idx] = number

                # Shortcut when all coordinates found.
                if -1 not in result:
                    return result

    return result


# print(solution(5, [19, 14, 28]))
print(solution(3, [7, 3, 5, 1]))
