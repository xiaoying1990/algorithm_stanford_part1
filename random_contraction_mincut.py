#!/usr/bin/python3

from graph import *


def test():
    g = Graph((4, 5), Type.undirected)
    g.add_node(1, conn=[2, 3])
    g.add_node(2, conn=[1, 3, 4])
    g.add_node(3, conn=[1, 2, 4])
    g.add_node(4, conn=[2, 3])
    g.check_it()
    res = g.random_contraction_min_cut()
    print(g, 'Min cut: {}'.format(res), sep='\n')


def test2():
    f = open('kargerMinCut.txt')
    di = {}
    es = 0
    for i in f:
        da = [int(j) for j in i.split()]
        di[da[0]] = da[1:]
        es += len(da) - 1
    es //= 2
    g = Graph((200, es), Type.undirected)
    for i in range(200):
        g.add_node(i + 1)
    for i, j in di.items():
        g.set_node_conn(i, j)
    g.check_it()
    res = g.random_contraction_min_cut()
    print('Min cut: {}'.format(res))


if __name__ == '__main__':
    test()
    test2()
