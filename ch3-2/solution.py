def solution(M, F):

    # Parameters converted from the string representation.
    m = long(M)
    f = long(F)

    # Mach bombs replicate increasing by a number of existing Facula bombs.
    # Facula bombs, in turn, replicate increasing by a number of Mach bombs.
    # Thus for each particular values of m and f we can decide what was
    # the previous state: decreasing f by m or m by f appropriately.
    # It makes possible to deduce number of replications required
    # by going backward from the final values till initial numbers of 1 Mach
    # bomb and 1 Facula bomb achieved.
    #
    # Searching forward (from 1 and 1 until required combination is found)
    # seems impractical due to size of possible results tree.

    count = long(0)

    # Loop while there are still more then 1 Mach and 1 Facula bomb.
    # Concerning they are integer, it means both are greater then 0 and
    # their sum is greater then 2.
    while m > 0 and f > 0 and m + f > 2:

        # Each replication produces biggest quantity of particular bomb kind
        # (as it is a sum of previous values of bombs of both kinds).
        # So, the largest of two numbers has been increased by replication
        # on a previous step. Delta is the smallest number in pair.
        #
        # Simple iteration with delta decrease on each step didn't
        # succeed though due to timing out on one of the tests. In order to
        # save time (when numbers of bomb kinds are significantly different)
        # it makes sense to advance count as much times as possible each
        # iteration. It is exactly how many times one number is bigger then
        # other (slightly less then original big number actually, to not fall
        # into corner case of zero remainder)
        if m > f:
            times = (m-1)/f
            m -= f * times
            count += times
        elif f > m:
            times = (f-1)/m
            f -= m * times
            count += times
        elif f == m:
            # There is no way (except initial state) when number of
            # Mach and Facula bombs can be equal.
            return 'impossible'

    return str(count)


print solution('4', '7')
print solution('2', '1')
print solution('2', '4')
print solution('3', '5')
print solution('5', '2')
