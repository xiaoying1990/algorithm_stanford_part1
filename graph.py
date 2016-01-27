#!/usr/bin/python3

import enum
import math
import random


class Type(enum.Enum):
    directed = 0
    undirected = 1


class Graph:
    class Node:
        def __init__(self, node_id, v):
            self._id = node_id
            self._value = v

    def __init__(self, size, typ: Type):
        self._size = size
        self._v_n = 0
        self._e_m = 0
        self._dic = {}
        self._nodes = {}
        self._type = typ

    def add_node(self, node_id, v=None, conn: (None, list) = None):
        no = Graph.Node(node_id, v)
        if node_id in self._nodes:
            raise Exception('There is already have a node with the same identifier {}'
                            .format(node_id))
        self._nodes[node_id] = no
        self._v_n += 1
        self._dic[node_id] = [] if not conn else conn
        self._e_m += len(conn) if conn else 0

    def set_node_conn(self, node_id, conn: list):
        if node_id not in self._nodes:
            raise Exception('Node {} is not in graph.'.format(node_id))
        self._e_m -= len(self._dic[node_id])
        self._dic[node_id] = conn
        self._e_m += len(conn)

    def check_it(self):
        if self._type == Type.undirected:
            assert self._e_m % 2 == 0, 'Undirected graph must have even number of edges.'
            tmp = self._e_m // 2
            for i in self._nodes.keys():
                for j in self._dic[i]:
                    if self._dic[j].count(i) != self._dic[i].count(j):
                        raise Exception('Undirected graph. Node a, Node b in it: num(a->b) must be equal to num(b->a).')
        else:
            tmp = self._e_m
        assert self._size == (self._v_n, tmp), 'Input must have some problem.'

    @property
    def graph_type(self):
        return self._type

    @property
    def graph_size(self):
        return self._size

    @property
    def graph_num_of_nodes(self):
        return self._v_n

    @property
    def graph_num_of_edges(self):
        return self._size[1]

    def __str__(self):
        return """graph with {2} nodes, {3} edges:
    nodes: {0},
    relations: {1}""".format(self._nodes.keys(), self._dic, *self._size)

    def random_contraction_min_cut(self):
        if self._type == Type.directed:
            raise Exception('Only undirected graph can do this.')
        if self._v_n == 1:
            raise Exception('Graph has only one node.')
        elif self._v_n == 2:
            return self._e_m // 2
        ans = self._e_m // 2
        t = int(self._v_n * self._v_n * math.log(self._v_n, math.e))
        for i in range(t // self._v_n):
            ans = min(ans, self.r_c_m())
            if i % 100 == 0:
                print('***** try: {} --- {}, ans: {}'.format(i, t // self._v_n, ans))
        return ans

    @staticmethod
    def _get_group_id(key, group):
        for i, j in enumerate(group):
            if key in j:
                return i
        raise Exception('Impossible.')

    def r_c_m(self):
        se = [[i] for i in self._nodes.keys()]
        es = dict((i, j[:]) for i, j in self._dic.items())
        while len(se) > 2:
            kv = random.choice(list(es.keys()))
            while len(es[kv]) == 0:
                kv = random.choice(list(es.keys()))
            p1, p2 = kv, random.choice(es[kv])
            i1, i2 = self._get_group_id(p1, se), self._get_group_id(p2, se)
            assert i1 != i2
            for i in se[i1]:
                j = 0
                while j < len(es[i]):
                    t = es[i][j]
                    if t in se[i2]:
                        del es[i][j]
                        es[t].remove(i)
                    else:
                        j += 1
            se[i1].extend(se[i2])
            del se[i2]
        _res = 0
        for i in es.values():
            _res += len(i)
        assert _res % 2 == 0, 'Impossible.'
        return _res // 2
