#!/usr/bin/python3
import random

SMALL_ENOUGH = 100  # when to directly multiply x and y.


def karatsuba_multiplication(x, y):
    """
    O(n^(lg(2, 3)) for big x and y, rather than O(n^2), thanks for divide and conquer strategy.
    :param x: integer x
    :param y: integer y
    :return: x * y
    """
    length_of_x, length_of_y = len(str(x)), len(str(y))
    if length_of_x * length_of_y < SMALL_ENOUGH:
        return x * y
    half_lox, half_loy = length_of_x//2, length_of_y//2
    a, b = int(str(x)[:-half_lox]), int(str(x)[-half_lox:])
    c, d = int(str(y)[:-half_loy]), int(str(y)[-half_loy:])
    return pow(10, half_lox + half_loy) * karatsuba_multiplication(a, c) + \
        pow(10, half_lox) * karatsuba_multiplication(a, d) + \
        pow(10, half_loy) * karatsuba_multiplication(b, c) + \
        karatsuba_multiplication(b, d) if length_of_x != length_of_y else \
        (lambda tmp_ac, tmp_bd, tmp_ac_bd_ad_bc:
            pow(10, 2 * half_lox) * tmp_ac +
            pow(10, half_lox) * (tmp_ac_bd_ad_bc - tmp_ac - tmp_bd) +
            tmp_bd)(karatsuba_multiplication(a, c),  # if x and y have the same length,
                    karatsuba_multiplication(b, d),  # we can just recursively call the function itself three times.
                    karatsuba_multiplication(a + b, c + d))


def test():
    for i in range(100000):
        x, y = random.randint(pow(10, 20), pow(10, 30)), random.randint(pow(10, 20), pow(10, 30))
        a, b = x * y, karatsuba_multiplication(x, y)  # In python, the multiplication for long int is already very fast.
        if a != b:  # And in python 3.4, there is no 'L' or 'l' tag for long int.
            print('{} {}'.format(a, b))
        if i % 10000 == 0:
            print('*', end=' ')
    print('\nrandom test done!')

if __name__ == '__main__':
    test()
