#!/usr/bin/python3

import random
import math
import time


def get_closest_pair(p):   # O(n*lgn)
    def simple_way(s: list) -> tuple:
        if len(s) < 2:
            return None
        best = dist((s[0], s[1]))
        best_pair = s[0], s[1]
        for i in range(len(s)):
            for j in range(i + 1, len(s)):
                t = dist((s[i], s[j]))
                if best > t:
                    best, best_pair = t, (s[i], s[j])
        return best_pair

    def get_sorted(s: list) -> tuple:
        sx = sorted(s, key=lambda x: x[0])
        sy = sorted(s, key=lambda x: x[1])
        return sx, sy

    def dist(x: tuple) -> (int, float):
        return math.sqrt(pow(x[0][0] - x[1][0], 2) + pow(x[0][1] - x[1][1], 2))

    def closest_split_pair(px: list, py: list, delta: (int, float)) -> tuple:
        _x = px[len(px) // 2 - 1][0]
        sy = [po for po in px if abs(po[0] - _x) <= delta]
        sy = [po for po in py if po in sy]
        # sy = sorted(sy, key=lambda x: x[1])
        best, best_pair = delta, None
        for i in range(len(sy)):
            for j in range(1, min(8, len(sy) - i)):
                a, b = sy[i], sy[i + j]
                d = dist((a, b))
                if d < best:
                    best, best_pair = d, (a, b)
        return best_pair

    def closest_pair(px: list, py: list) -> tuple:
        if len(px) < 10:
            return simple_way(px)
        q = px[:len(px) // 2]
        r = px[len(px) // 2:]
        a = closest_pair(*get_sorted(q))
        b = closest_pair(*get_sorted(r))
        delta = min(dist(a), dist(b))
        c = closest_split_pair(px, py, delta)
        return sorted((a, b, c) if c else (a, b), key=lambda x: dist(x))[0]

    setattr(get_closest_pair, 'simple_way', simple_way)
    setattr(get_closest_pair, 'dist', dist)
    return closest_pair(*get_sorted(p))


def test(n=1000):
    p = [(random.random(), 0 * i + random.random()) for i in range(n)]
    print('There are {} points in set.'.format(n))
    t1 = time.time()
    a = get_closest_pair(p)
    print('use O(n*lgn) algorithm: {}'.format(time.time() - t1))
    t2 = time.time()
    b = get_closest_pair.simple_way(p)
    print('use O(n^2) algorithm: {}'.format(time.time() - t2))
    print('The closest pair in p is: {}'.format(a))
    print('The closest pair in p is: {}'.format(b))
    print('Is these the same stuff? {}'.format(a == b or tuple(reversed(a)) == b))
    print('dist 1: {}, dist 2: {}'.format(get_closest_pair.dist(a), get_closest_pair.dist(b)))

if __name__ == '__main__':
    test(100)
    test()
