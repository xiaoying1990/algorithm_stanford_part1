#!/usr/bin/python3

import random


def merge_sort(ar):
    """
    O(n*log(n)), dived & conquer algorithm for sorting array to increasing order.
    :param ar: type(ar) = 'list', as a array of number.
    :return: None, while sorting the parameter 'arr' itself. We can change it, because list is mutable.
    """
    arr = ar[:]
    def merge(begin, end, mid):
        """
        The key function which merge two adjacent pieces of arr into a sorted one.
        This function uses a copy list: arr[begin:end + 1].
        first piece: arr[begin:mid + 1]
        second piece: arr[mid + 1:end + 1]
        :param begin: the beginning index of the first piece of list in arr
        :param end: the last index of the second piece of list in arr
        :param mid: the last index of the first piece of list in arr
        :return: None, with the sorting change of arr[begin:end + 1]
        """
        i, j, k = 0, mid + 1 - begin, begin  # i and j means the index of the two pieces in arr_copy.
        arr_copy = arr[begin:end + 1]        # k is for resetting value from arr_copy to arr.
        while i <= mid - begin and j <= end - begin:
            if arr_copy[i] <= arr_copy[j]:
                arr[k], k, i = arr_copy[i], k + 1, i + 1
            else:
                arr[k], k, j = arr_copy[j], k + 1, j + 1
        while i <= mid - begin:
            arr[k], k, i = arr_copy[i], k + 1, i + 1
        while j <= end - begin:
            arr[k], k, j = arr_copy[j], k + 1, j + 1

    def merge_sort_for_arr(begin=0, end=len(arr) - 1):
        if begin == end:
            return
        mid = (begin + end) // 2
        merge_sort_for_arr(begin, mid)
        merge_sort_for_arr(mid + 1, end)
        merge(begin, end, mid)

    merge_sort_for_arr()
    return arr


def test():
    l = list(random.randint(0 * i, 100) for i in range(50000))
    random.shuffle(l)
    print('the list l: {}'.format(l))
    l_sorted = sorted(l)
    l_sorted2 = merge_sort(l)
    print('using built-in function sorted: {}'.format(l_sorted))
    print('list l after applying merger_sort: {}'.format(l_sorted2))
    print('Does these the same result? {}'.format(l_sorted2 == l_sorted))
    print('Does these the same list object? {}'.format(l_sorted2 is l_sorted))

if __name__ == '__main__':
    test()
