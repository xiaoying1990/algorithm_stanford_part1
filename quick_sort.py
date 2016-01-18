#!/usr/bin/python3

import random


def quick_sort(li: list) -> list:
    l = li[:]

    def choose_pivot(begin: int, end: int) -> int:
        mid = (begin + end) // 2
        if l[begin] < l[mid]:
            if l[begin] < l[end]:
                return mid if l[mid] < l[end] else end
            else:
                return begin
        else:
            if l[mid] < l[end]:
                return begin if l[begin] < l[end] else end
            else:
                return mid
        # return random.randint(begin, end)

    def q_s(begin: int, end: int) -> int:
        if begin >= end:
            return 0
        pv = choose_pivot(begin, end)
        l[begin], l[pv] = l[pv], l[begin]
        ps, t = begin + 1, l[begin]
        for i in range(begin + 1, end + 1):
            if t > l[i]:
                l[ps], l[i] = l[i], l[ps]
                ps += 1
        l[begin], l[ps - 1] = l[ps - 1], l[begin]
        a = q_s(begin, ps - 2)
        b = q_s(ps, end)
        return a + b + end - begin

    hit = q_s(0, len(l) - 1)
    return l, hit


def test():
    l = list(random.randint(0 * i, 100) for i in range(50000))
    random.shuffle(l)
    print('the list l: {}'.format(l))
    l_sorted = sorted(l)
    l_sorted2= quick_sort(l)[0]
    print('using built-in function sorted: {}'.format(l_sorted))
    print('list l after applying quick_sort: {}'.format(l_sorted2))
    print('Does these the same result? {}'.format(l_sorted2 == l_sorted))

if __name__ == '__main__':
    test()
    ls = [int(i) for i in open('QuickSort.txt')]
    ans, hi = quick_sort(ls)
    print(ans == list(range(10001))[1:])
    print(hi)

