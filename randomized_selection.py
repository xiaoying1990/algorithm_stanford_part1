#!/usr/bin/python3

import random


def randomized_selection(a, index):  # O(n)

    def choose_pivot(begin, end):
        return random.randint(begin, end)

    def r_s(begin, end):
        if begin > end:
            raise Exception('Not find, which is impossible.')
        pv = choose_pivot(begin, end)
        ar[begin], ar[pv] = ar[pv], ar[begin]
        pn, k = begin + 1, ar[begin]
        for i in range(begin + 1, end + 1):
            if ar[i] < k:
                ar[pn], ar[i] = ar[i], ar[pn]
                pn += 1
        ar[begin], ar[pn - 1] = ar[pn - 1], ar[begin]
        t = pn - 1
        if t == index:
            return k
        elif t < index:
            return r_s(pn, end)
        else:
            return r_s(begin, pn - 2)

    if index > len(a) - 1 or index < 0:
        raise IndexError('Index should be correct. Length of array: {}. Search index: {}'
                         .format(len(a), index))
    ar = a[:]
    return r_s(0, len(ar) - 1), ar


def test():
    l = list(range(500))
    random.shuffle(l)
    print('the list l: {}'.format(l))
    l_sorted = sorted(l)
    l_sorted2 = [randomized_selection(l, i)[0] for i in range(len(l))]
    print('using built-in function sorted: {}'.format(l_sorted))
    print('list l after applying randomized_selection: {}'.format(l_sorted2))
    print('Does these the same result? {}'.format(l_sorted2 == l_sorted))
    l = list(range(10))
    random.shuffle(l)
    print(l)
    print(randomized_selection(l, 5))
    print(randomized_selection(l, 5))

if __name__ == '__main__':
    test()
