#!/usr/bin/python3

import random
import time

SMALL_ENOUGH = 1000000


class ListMatrix:
    def __init__(self, li: (list, tuple), n_r: int, n_c: int):
        self._li = list(li)
        self._n_r = n_r
        self._n_c = n_c

    @property
    def size(self):
        return self._n_r, self._n_c

    @property
    def li(self):
        return self._li

    def __str__(self):
        return '----Matrix----\n'+'\n'.join(str(r) for r in self.rows())+'\n-------------\n'

    def __getitem__(self, item):
        pass

    def __setitem__(self, key, value):
        pass

    def rows(self):
        for r in range(self._n_r):
            yield self._li[r * self._n_c:(r + 1) * self._n_c]

    def cols(self):
        for c in range(self._n_c):
            yield self._li[c::self._n_c]


class Matrix(ListMatrix):
    """
    Matrix operations:
        binary operators: + , -, *, * num,
        unary operator: ^T, -, abs()
    Matrix access:
        []([]), iterable Rows() & Cols(), len()
    """
    class SelectedRows(ListMatrix):
        def __init__(self, l: list, n_r: int, n_c: int, parent: 'Matrix', row_item: (int, slice)):
            self._parent = parent
            self._row_item = row_item
            assert n_r * n_c == len(l), 'Impossible'
            super().__init__(l, n_r, n_c)

        def __getitem__(self, item: (int, slice)) -> (int, list, 'Matrix'):
            if isinstance(item, int) or (isinstance(item, slice) and item.step == 0):
                it = item
                if isinstance(item, slice) and item.step == 0:
                    it = item.start
                if it < self._n_c:
                    if self._n_r == 1:
                        return self._li[it]
                    return self._li[it::self._n_c]
                else:
                    raise IndexError('The column index {} is bigger than {}.'.format(item, self._n_c))
            elif isinstance(item, slice):
                sta = item.start if item.start else 0
                ste = item.step if item.step else 1
                sto = item.stop if item.stop else self._n_c
                l = [r for i, r in enumerate(self._li)
                     if (lambda index: ((sta <= index < sto) if ste > 0 else
                                        (sto < index <= sta)) and (index - sta) % ste == 0)
                     (i % self._n_c)]
                return Matrix(l, self._n_r, abs((sta - sto) // ste))
            else:
                raise IndexError('Matrix column index must be a integer or a slice, not {}'.format(item))

        def __setitem__(self, key: (int, slice), value: (int, list, tuple, 'Matrix', 'Matrix.SelectedRows')) -> None:
            if isinstance(value, (Matrix, Matrix.SelectedRows)):
                value = value.li
            if isinstance(key, int):
                if isinstance(self._row_item, int):
                    self._parent.li[self._row_item * self._n_c + key] = value
                elif isinstance(self._row_item, slice):
                    if isinstance(value, (int, float)):
                        for i in range(self._n_r):
                            self._parent.li[self._row_item.start + i * self._row_item.step * self._n_c + key] = value
                    else:
                        for i in min(range(self._n_r), len(value)):
                            self._parent.li[self._row_item.start + i * self._row_item.step * self._n_c + key] = value[i]
            elif isinstance(key, slice):
                if isinstance(self._row_item, int):
                    i = key.start if key.start else 0
                    ste = key.step if key.step else 1
                    sto = key.stop if key.stop else self._n_c
                    if isinstance(value, (int, float)):
                        if ste > 0:
                            while i < sto:
                                self._parent.li[self._row_item * self._n_c + i] = value
                                i += ste
                        elif ste == 0:
                            self._parent.li[self._row_item * self._n_c + i] = value
                        else:
                            while i > sto:
                                self._parent.li[self._row_item * self._n_c + i] = value
                                i += ste
                    else:
                        j = 0
                        if ste > 0:
                            while i < sto and j < len(value):
                                self._parent.li[self._row_item * self._n_c + i] = value[j]
                                i += ste
                                j += 1
                        elif ste == 0:
                            self._parent.li[self._row_item * self._n_c + i] = value[j]
                        else:
                            while i > sto and j < len(value):
                                self._parent.li[self._row_item * self._n_c + i] = value[j]
                                i += ste
                                j += 1
                elif isinstance(self._row_item, slice):
                    sta = key.start if key.start else 0
                    ste = key.step if key.step else 1
                    sto = key.stop if key.stop else self._n_c
                    r_sta = self._row_item.start if self._row_item.start else 0
                    r_ste = self._row_item.step if self._row_item.step else 1
                    # r_sto = self._row_item.stop if self._row_item.stop else self._parent.size[0]
                    if isinstance(value, (int, float)):
                        for i in range(self._n_r):
                            for j in range(abs((sta - sto) // ste)):
                                self._parent.li[r_sta + i * r_ste * self._n_c +
                                                sta + j * ste] = value
                    else:
                        k = 0
                        for i in range(self._n_r):
                            for j in range(abs((sta - sto) // ste)):
                                if k < len(value):
                                    self._parent.li[r_sta + i * r_ste * self._n_c +
                                                    sta + j * ste] = value[k]
                                    k += 1
                                else:
                                    return
            else:
                raise IndexError('Matrix column index mast be a integer or a slice, not {}'.format(key))

    def __init__(self, *args, **kwargs):
        if len(args) == 1:
            try:
                super().__init__(args[0].li[:], *args[0].size)
            except Exception as e:
                print('Argument must be a matrix or a selected_rows! \nNot {}\n{}'.format(args[0], e))
        elif len(args) == 2:
            ran_num = kwargs.get('ran', False)
            super().__init__([random.random() * 100 if ran_num else 0 * i
                              for i in range(args[0] * args[1])], args[0], args[1])
        elif len(args) == 3:
            assert isinstance(args[0], (list, tuple)), \
                'First argument must be a list or a tuple, not {}'.format(args[0])
            assert isinstance(args[1], int), 'Second argument must be a int, not {}'.format(args[1])
            assert isinstance(args[2], int), 'Third argument must be a int, not {}'.format(args[2])
            assert args[1] * args[2] == len(args[0]), 'Arguments wrong: {}'.format(args)
            super().__init__(*args)
        else:
            raise Exception('Arguments wrong: {}'.format(args))

    def __getitem__(self, item: (int, slice)) -> SelectedRows:
        if isinstance(item, (slice, int)):
            if isinstance(item, int):
                l = [r for i, r in enumerate(self._li) if item == i // self._n_c]
                n_r = 1
            else:
                sta = item.start if item.start else 0
                ste = item.step if item.step else 1
                sto = item.stop if item.stop else self._n_r
                l = [r for i, r in enumerate(self._li) if
                     (ste > 0 and (sta <= i // self._n_c < sto) and
                      (i // self._n_c - sta) % ste == 0) or
                     (ste < 0 and (sta >= i // self._n_c > sto) and
                      (i // self._n_c - sta) % ste == 0) or
                     (ste == 0 and sta == i // self._n_c)
                     ]
                n_r = abs((sta - sto) // ste)
            return self.SelectedRows(l, n_r, self._n_c, self, item)
        else:
            raise IndexError('Matrix row index must be a integer or a slice, not {}'.format(item))

    def __setitem__(self, key: (int, slice), value) -> None:
        self[key][:] = value

    def transposition_matrix(self):
        l = []
        for i in self.cols():
            l.extend(i)
        return Matrix(l, self._n_c, self._n_r)

    @staticmethod
    def add(ma: 'Matrix', mb: 'Matrix') -> 'Matrix':
        if ma.size == mb.size:
            return Matrix([x + y for x, y in zip(ma.li, mb.li)], *ma.size)
        else:
            raise Exception('Only same size matrix can be added together.\n{}\n{}'.format(ma, mb))

    def __eq__(self, other: 'Matrix'):
        if self.size == other.size and self.li == other.li:
            return True
        return False

    def __add__(self, other):
        return self.add(self, other)

    @staticmethod
    def sub(ma: 'Matrix', mb: 'Matrix') -> 'Matrix':
        return Matrix.add(ma, mb * -1)

    def __sub__(self, other):
        return self.sub(self, other)

    def __abs__(self):
        return Matrix([abs(e) for e in self.li], *self.size)

    @staticmethod
    def dm(ma: 'Matrix', d: (int, float)) -> 'Matrix':
        return Matrix([e * d for e in ma.li], *ma.size)

    def __neg__(self):
        return self * -1

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Matrix.dm(self, other)
        elif isinstance(other, Matrix):
            if self.size[0] * self.size[1] * other.size[0] * other.size[1] < SMALL_ENOUGH:
                return Matrix.mul_simple(self, other)
            return Matrix.mul(self, other)
        else:
            raise Exception('{} is not a number or a matrix.'.format(other))

    @staticmethod
    def mul_simple(ma: 'Matrix', mb: 'Matrix') -> 'Matrix':  # O(n^3)
        if ma.size[1] != mb.size[0]:
            raise Exception('cannot multiply the two matrix, ' +
                            'because the number of columns {} of ma != the number of rows {} of mb'
                            .format(ma.size[1], mb.size[0])
                            )
        same_index = ma.size[1]
        l = [sum(ma[i][k] * mb[k][j] for k in range(same_index))
             for i in range(ma.size[0]) for j in range(mb.size[1])]
        return Matrix(l, ma.size[0], mb.size[1])

    @staticmethod
    def mul(ma: 'Matrix', mb: 'Matrix') -> 'Matrix':   # O(n^2)
        if ma.size[1] != mb.size[0]:
            raise Exception('cannot multiply the two matrix, ' +
                            'because the number of columns {} of ma != the number of rows {} of mb'
                            .format(ma.size[1], mb.size[0])
                            )
        ar, ac, br, bc = ma.size + mb.size
        ans = Matrix(ar, bc)
        a, b = ma[:ar // 2][:ac // 2], ma[:ar // 2][ac // 2:]
        c, d = ma[ar // 2:][:ac // 2], ma[ar // 2:][ac // 2:]
        e, f = mb[:br // 2][:bc // 2], mb[:br // 2][bc // 2:]
        g, h = mb[br // 2:][:bc // 2], mb[br // 2:][bc // 2:]
        if ar % 2 == 0 and ac % 2 == 0 and br % 2 == 0 and bc % 2 == 0:
            p1, p2 = a * (f - h), (a + b) * h
            p3, p4 = (c + d) * e, d * (g - e)
            p5, p6, p7 = (a + d) * (e + h), (b - d) * (g + h), (a - c) * (e + f)
            part1, part2 = p5 + p4 - p2 + p6, p1 + p2
            part3, part4 = p3 + p4, p1 + p5 - p3 - p7
        else:
            part1, part2 = a * e + b * g, a * f + b * h
            part3, part4 = c * e + d * g, c * f + d * h
        ans[:ar // 2][:bc // 2], ans[:ar // 2][bc // 2:] = part1, part2
        ans[ar // 2:][:bc // 2], ans[ar // 2:][bc // 2:] = part3, part4
        # print('------{}'.format(ans.len()))
        return ans


def test():
    a = Matrix((1, 2, 3, 0, 4, 3), 2, 3)
    print(a, end='')
    a[0:2][0:2] = [3, -1, 2, 3]
    print(a, end='')
    print(type(a[0:2][0]), a[0:2][0], sep=': ')
    print(a[:][:], end='')
    print(a[0][0])
    print(type(a[0]), type(a[:][:]))
    b = Matrix([2, 4, 2, 1, -4, 6], 2, 3)
    print('Matrix a:\n{}'.format(a), end='')
    print('size of a: {} rows, {} columns'.format(*a.size))
    print('build 0s Matrix with same size of a:\n{}'.format(Matrix(*a.size)), end='')
    print('copy of matrix a: \n{}\nis it "a"? {}'.format(Matrix(a), a is Matrix(a)), end='')
    print('Matrix b: \n{}'.format(b), end='')
    print('-a: \n{}'.format(-a), end='')
    print('|b|: \n{}'.format(abs(b)), end='')
    print('a + b: \n{}'.format(a + b), end='')
    print('a - b: \n{}'.format(a - b), end='')
    print('a * 3.1: \n{}'.format(a * 3.1), end='')
    bt = b.transposition_matrix()
    print('T of b: \n{}'.format(bt), end='')
    print('a * b^T: \n{}'.format(a * bt), end='')
    print('test multiply: {}'.format(a * bt == Matrix.mul_simple(a, bt)))
    print('test == operator: {}'.format(b == Matrix(b)))
    t0 = time.time()
    a = Matrix(1500, 1500, ran=True)
    b = Matrix(1500, 1500, ran=True)
    print('time consuming for ran: {} seconds'.format(time.time() - t0))
    t1 = time.time()
    c = a + b
    print('time consuming for a * b: {} seconds'.format(time.time() - t1))
    t2 = time.time()
    d = Matrix.mul_simple(a, b)
    print('time consuming for mul_simple(a, b): {} seconds'.format(time.time() - t2))
    print(c == d)

if __name__ == '__main__':
    test()
