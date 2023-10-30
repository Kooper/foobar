#!/bin/env python2.7

from __future__ import print_function
from collections import Counter
from fractions import gcd
from math import factorial

def check_data(w, h, s):
    assert(min(w, h)) >= 1
    assert(max(w, h)) <= 12
    assert(s) >= 2
    assert(s) <= 20


# Integer partition from https://stackoverflow.com/questions/10035752/elegant-python-code-for-integer-partitioning
def partitions(n, I=1):
    yield (n,)
    for i in range(I, n//2 + 1):
        for p in partitions(n-i, i):
            yield (i,) + p

def s_power(partition1, partition2):
    return sum([sum([gcd(i, j) for i in partition1]) for j in partition2])

def conjugacy_size(r):
    n = factorial(sum(r))
    for k, v in Counter(r).items():
        n /=(k**v)*factorial(v)
    return n

# The solution from https://medium.com/@chris.bell_/google-foobar-as-a-non-developer-level-5-a3acbf3d962b
def solution(w, h, s):
    check_data(w, h, s)
    elements = 0
    for c in partitions(w):
        for r in partitions(h):
            C = conjugacy_size(c) * conjugacy_size(r)
            elements += C * (s**s_power(r, c))
    return "{}".format(elements / (factorial(w) * factorial(h)))


print(solution(2, 2, 2)) # must be 7
print(solution(1, 1, 20)) # must be 20
print(solution(2, 3, 4)) # must be 430
