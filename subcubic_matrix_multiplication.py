#!/usr/bin/python3

import random
import copy
import functools
import time


class Matrix:
    """
    Matrix operations:
        binary operators: + , -, *, * num,
        unary operator: ^T, -, abs()
    Matrix access:
        []([]), iterable Rows() & Cols(), len()
    """
    class SelectedArea:  # todo: matrix[slice][slice], problem: is_regular_.., add, deepcopy, [][] too time consuming
        def __init__(self, parent, row_slice, col_slice):
            self._parent = parent
            self._area = row_slice, col_slice

        def __str__(self):
            return str([r[self._area[1]] for r in self._parent.matrix[self._area[0]]])

        def __setitem__(self, key, value):
            pass

        def __getitem__(self, item):
            pass

    class SelectedRows:
        def __init__(self, parent, row_slice):
            self._row_slice = row_slice
            self._parent = parent

        def __getitem__(self, item):
            if isinstance(item, int):
                return [r[item] for r in self._parent.matrix[self._row_slice]]
            elif isinstance(item, slice):
                # return Matrix.SelectedArea(self._parent, self._row_slice, item)
                return Matrix(r[item] for r in self._parent.matrix[self._row_slice])
            else:
                raise IndexError('Matrix column index must be a integer or a slice, not {}'.format(item))

        def __setitem__(self, key, value):
            for r, v in zip(self._parent.matrix[self._row_slice], value):
                r[key] = v

        def __str__(self):
            return str(self._parent[self._row_slice])

    def __init__(self, *args, **kwargs):
        if len(args) == 1:
            if isinstance(args[0], Matrix.SelectedRows):
                self._matrix = Matrix(list(args[0])).transposition_matrix().matrix
            else:
                self._matrix = copy.deepcopy(list(args[0]))
        elif len(args) == 2:
            ran_num = kwargs.get('ran', False)
            n_rows, n_cols = args[0], args[1]
            if isinstance(n_cols, int):
                self._matrix = [[random.random() * 100 if ran_num else 0 * (r + c)
                                 for c in range(n_cols)] for r in range(n_rows)]
            elif isinstance(n_cols, tuple):
                self._matrix = [[random.random() * 100 if ran_num else 0 * (r + c)
                                 for c in range(n_cols[r])] for r in range(n_rows)]
        else:
            raise Exception('arguments wrong: {}'.format(args))

    def __getitem__(self, item):
        if isinstance(item, slice):
            return self.SelectedRows(self, item)
        elif isinstance(item, int):
            return self._matrix[item]
        else:
            raise IndexError('Matrix row index must be a integer or a slice, not {}'.format(item))

    def __setitem__(self, key, value):
        self._matrix[key] = list(value)

    def __str__(self):
        return str(self._matrix)

    def rows(self):
        for row in self._matrix:
            yield row

    def cols(self):
        n_c = self.num_cols
        if isinstance(n_c, int):
            for c in range(n_c):
                yield [r[c] for r in self._matrix]
        elif isinstance(n_c, tuple):
            for c in range(max(n_c)):
                yield [r[c] if c < len(r) else None for r in self._matrix]
        else:
            raise Exception('impossible')

    def transposition_matrix(self):
        if not self.is_regular_matrix():
            raise Exception('Can not do this, for {} is not a regular matrix.'.format(self))
        return Matrix(self.cols())

    def is_regular_matrix(self):
        t = tuple(len(r) for r in self._matrix)
        assert len(t) == self.num_rows, 'impossible'
        return max(t) == min(t) and functools.reduce((lambda x, y: x and y),
                                                     ((lambda x: isinstance(x, (int, float)))(e)
                                                      for r in self._matrix for e in r)
                                                     )

    def len(self):
        return self.num_rows, self.num_cols

    @property
    def matrix(self):
        return self._matrix

    @matrix.setter
    def matrix(self, value):
        self._matrix = value

    @property
    def num_rows(self):
        return len(self._matrix)

    @property
    def num_cols(self):
        t = tuple(len(r) for r in self._matrix)
        return max(t) if max(t) == min(t) else t

    @staticmethod
    def add(ma: 'Matrix', mb: 'Matrix') -> 'Matrix':
        if ma.is_regular_matrix() and mb.is_regular_matrix() \
                and ma.num_rows == mb.num_rows and ma.num_cols == mb.num_cols:
            return Matrix([ca + cb for ca, cb in zip(ra, rb)] for ra, rb in zip(ma, mb))
        else:
            raise Exception('Matrix is not regular or cannot be added. \n{} \n{}'.format(ma, mb))

    def __eq__(self, other):
        return functools.reduce((lambda x, y: x and y),
                                (i < other.num_rows and (j < other.num_cols[i] if isinstance(other.num_cols, tuple)
                                                         else j < other.num_cols)
                                 and (abs(other[i][j] - e) < 0.0000001 if isinstance(e, float)
                                      else other[i][j] == e)
                                 for i, r in enumerate(self._matrix) for j, e in enumerate(r))
                                )

    def __add__(self, other):
        return self.add(self, other)

    @staticmethod
    def sub(ma: 'Matrix', mb: 'Matrix') -> 'Matrix':
        return Matrix.add(ma, Matrix.dm(mb, -1))

    def __sub__(self, other):
        return self.sub(self, other)

    def __abs__(self):
        return Matrix([abs(e) for e in r] for r in self._matrix)

    @staticmethod
    def dm(ma: ('Matrix', int), d: (int, float)) -> 'Matrix':
        if ma.is_regular_matrix():
            return Matrix([d * v for v in r] for r in ma)
        else:
            raise Exception('matrix is not regular. \n{}'.format(ma))

    def __neg__(self):
        return Matrix.dm(self, -1)

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Matrix.dm(self, other)
        elif isinstance(other, Matrix):
            if self.num_cols * self.num_rows * other.num_cols * other.num_rows < 100000000:
                return Matrix.mul_simple(self, other)
            return Matrix.mul(self, other)
        else:
            raise Exception('{} is not a number or a matrix.'.format(other))

    @staticmethod
    def mul_simple(ma: 'Matrix', mb: 'Matrix') -> 'Matrix':  # O(n^3)
        if not ma.is_regular_matrix() or not mb.is_regular_matrix():
            raise Exception('at least one matrix is not regular.\n{}\n{}'
                            .format(ma, mb))
        if ma.num_cols != mb.num_rows:
            raise Exception('cannot multiply the two matrix, ' +
                            'because the number of columns {} of {} != the number of rows {} of {}'
                            .format(ma.num_cols, ma, mb.num_rows, mb)
                            )
        same_index = ma.num_cols
        return Matrix([sum(r[i] * c[i] for i in range(same_index)) for c in mb.cols()] for r in ma.rows())

    @staticmethod
    def mul(ma: 'Matrix', mb: 'Matrix') -> 'Matrix':   # O(n^2)
        if not ma.is_regular_matrix() or not mb.is_regular_matrix():
            raise Exception('at least one matrix is not regular.\n{}\n{}'
                            .format(ma, mb))
        if ma.num_cols != mb.num_rows:
            raise Exception('cannot multiply the two matrix, ' +
                            'because the number of columns {} of {} != the number of rows {} of {}'
                            .format(ma.num_cols, ma, mb.num_rows, mb)
                            )
        ar, ac, br, bc = ma.len() + mb.len()
        ans = Matrix(ar, bc)
        a, b, c, d = ma[:ar // 2][:ac // 2], ma[:ar // 2][ac // 2:], ma[ar // 2:][:ac // 2], ma[ar // 2:][ac // 2:]
        e, f, g, h = mb[:br // 2][:bc // 2], mb[:br // 2][bc // 2:], mb[br // 2:][:bc // 2], mb[br // 2:][bc // 2:]
        if ar % 2 == 0 and ac % 2 == 0 and br % 2 == 0 and bc % 2 == 0:
            p1, p2, p3, p4, p5, p6, p7 = a * (f - h), (a + b) * h, (c + d) * e, \
                                         d * (g - e), (a + d) * (e + h), \
                                         (b - d) * (g + h), (a - c) * (e + f)
            part1, part2, part3, part4 = p5 + p4 - p2 + p6, \
                                         p1 + p2, \
                                         p3 + p4, \
                                         p1 + p5 - p3 - p7
        else:
            part1, part2, part3, part4 = a * e + b * g, \
                                         a * f + b * h, \
                                         c * e + d * g, \
                                         c * f + d * h
        ans[:ar // 2][:bc // 2], ans[:ar // 2][bc // 2:], \
            ans[ar // 2:][:bc // 2], ans[ar // 2:][bc // 2:] = part1, part2, part3, part4
        assert ans.len() == (ar, bc), 'impossible'
        # print('------{}'.format(ans.len()))
        return ans


def test():
    a = Matrix([[1, 2], [3, 0], [4, 3]])
    a[0:2][0:2] = [[3, -1], [2, 3]]
    print(a[0:2][0])
    print(a[:][:])
    print(type(a[:][:]))
    b = Matrix([[2, 4], [2, 1], [-4, 6]])
    c = Matrix([[1, 2], [3, 0, 1.2], [4]])
    print('Matrix a: {}'.format(a))
    print('Matrix b: {}'.format(b))
    print('-a: {}'.format(-a))
    print('|b|: {}'.format(abs(b)))
    print('a + b: {}'.format(a + b))
    print('a - b: {}'.format(a - b))
    print('a * 3.1: {}'.format(a * 3.1))
    print('T of b: {}'.format(b.transposition_matrix()))
    bt = b.transposition_matrix()
    print('a * b^T: {}'.format(a * bt))
    print('test multiply: {}'.format(a * bt == Matrix.mul_simple(a, bt)))
    print('Matrix c: {}, is it a regular matrix? {}'.format(c, c.is_regular_matrix()))
    print('len of a and c: \n{}\n{}'.format(a.len(), c.len()))
    print('build 0s Matrix with same len of a and c:\n{}\n{}'.format(Matrix(*a.len()), Matrix(*c.len())))
    print('deep copy of matrix c: {}, is it "c"? {}'.format(Matrix(c), c is Matrix(c)))
    print('test == operator: {}'.format(c == Matrix(c)))
    a = Matrix(50, 50, ran=True)
    b = Matrix(50, 50, ran=True)
    t1 = time.time()
    c = a * b
    print('time consuming for a * b: {} seconds'.format(time.time() - t1))
    t2 = time.time()
    d = Matrix.mul_simple(a, b)
    print('time consuming for mul_simple(a, b): {} seconds'.format(time.time() - t2))
    print(c == d)

if __name__ == '__main__':
    test()
