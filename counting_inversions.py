#!\usr\bin\python3

import random


def counting_inversions(arr):
    """
    O(n*log(n)), dived & conquer algorithm for counting inversions in an array.
    Inversion means arr[i] > arr[j] while i < j.
    All sorting changes are done in arr_copy,
    rather than some new small pieces of array for sub functions to return.
    :param arr: type(arr) = 'list', as a array of number.
    :return: the number of inversions and sorted array arr_copy.
    """
    arr_copy = arr[:]  # have a copy of arr, without changing the origin one.

    def count_split_inv(begin, end):
        """
        This function counting the inversions of elements in two adjacent pieces of arr_copy.
        And then sorting this two pieces into a one, which is arr_copy[begin:end + 1]
        first piece: arr_copy[begin:mid + 1]
        second piece: arr_copy[mid + 1:end + 1]
        :param begin: the beginning index of the first piece of list in arr_copy
        :param end: the last index of the second piece of list in arr_copy
        :return: the number of inversions between two adjacent pieces of arr_copy.
        """
        mid = (begin + end) // 2
        i, j = begin, mid + 1
        res, c = 0, 0
        while i <= mid:  # This is linear time consuming.
            while j <= end and arr_copy[i] > arr_copy[j]:
                c, j = c + 1, j + 1   # Can do this because the two pieces arr_copy[begin:mid + 1]
            res, i = res + c, i + 1   # and arr_copy[mid + 1:end + 1] has already been sorted.
        i, j, k = 0, mid + 1 - begin, begin
        arr_copy2 = arr_copy[begin:end + 1]  # used for sorting
        while i <= mid - begin and j <= end - begin:
            if arr_copy2[i] <= arr_copy2[j]:
                arr_copy[k], k, i = arr_copy2[i], k + 1, i + 1
            else:
                arr_copy[k], k, j = arr_copy2[j], k + 1, j + 1
        while i <= mid - begin:
            arr_copy[k], k, i = arr_copy2[i], k + 1, i + 1
        while j <= end - begin:
            arr_copy[k], k, j = arr_copy2[j], k + 1, j + 1
        return res

    def c_i(begin=0, end=len(arr) - 1):
        if begin == end:
            return 0
        mid = (begin + end) // 2
        res1 = c_i(begin, mid)
        res2 = c_i(mid + 1, end)
        res3 = count_split_inv(begin, end)
        return res1 + res2 + res3  # return a integer.

    return c_i(), arr_copy  # return a tuple.


def test(size=pow(10, 5)):
    l = list(range(size))
    random.shuffle(l)
    print('the list l: {}'.format(l))
    l_sorted = sorted(l)
    ans = counting_inversions(l)
    print('using built-in function sorted: {}'.format(l_sorted))
    print('using counting_inversions: {}'.format(ans[1]))
    print('Does counting_inversions sorting right? {}'.format(ans[1] == l_sorted))
    print('the number of inversions is: {}'.format(ans[0]))


if __name__ == '__main__':
    test()
    test(10)
    l = [int(i) for i in open('IntegerArray.txt')]
    ans = counting_inversions(l)
    print(ans[0])
