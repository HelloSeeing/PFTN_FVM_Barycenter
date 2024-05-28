#!-*- coding:utf-8 -*-

import numpy as np

class halfEdge(object):
    def __init__(self, s, t, idx) -> None:
        self.s = s
        self.t = t
        self.idx = idx
        self.next_idx = None
        self.opposite_idx = None

    def outer_normal(self, nodes):
        s = nodes[self.s]
        t = nodes[self.t]
        v = np.array((s[0] - t[0], s[1] - t[1]))
        n = np.array((t[1] - s[1], s[0] - t[0]))
        cross_product = np.cross(v, n)
        if cross_product < 0:
            n = -n
        return n

class fvMesh(object):
    def __init__(self, x0, x1, y0, y1, nrows=1, ncols=1) -> None:
        
        self.x0 = x0
        self.x1 = x1
        self.y0 = y0
        self.y1 = y1
        self.nrows = nrows
        self.ncols = ncols

    def _generate_mesh(self):

        x = np.linspace(self.x0, self.x1, self.ncols + 1)
        y = np.linspace(self.y0, self.y1, self.nrows + 1)

        nx, ny = np.meshgrid(x, y)

        nodes = np.stack((nx, ny), axis=1)

        hes = [None for _ in range(6 * self.nrows * self.ncols)]
        cells = [None for _ in range(2 * self.nrows * self.ncols)]
        k = 0

        for i in range(self.nrows):
            for j in range(self.ncols):
                # upper left triangle
                cell_id = 2 * (i * self.ncols + j)
                
                p0 = i * (self.ncols + 1) + j
                p1 = p0 + 1
                p2 = p0 + self.ncols + 1

                he0 = halfEdge(p0, p1, idx=k)
                he0.next_idx = k + 1
                if i > 0:
                    adjacent_cell_id = 2 * ((i - 1) * self.ncols + j) + 1
                    adjacent_he = cells[adjacent_cell_id][1]
                    he0.opposite_idx = adjacent_he.idx
                    adjacent_he.opposite_idx = he0.idx

                # record into halfedges
                hes[3 * cell_id] = he0

                he1 = halfEdge(p1, p2, idx=k + 1)
                he1.next_idx = k + 2
                hes[3 * cell_id + 1] = he1

                he2 = halfEdge(p2, p0, idx=k + 2)
                he2.next_idx = k
                hes[3 * cell_id + 2] = he2

                cells[cell_id] = (he0, he1, he2)

                k += 3

                # lower right triangle
                cell_id = 2 * (i * self.ncols + j) + 1
                
                p0 = p1
                p1 = p0 + self.ncols + 1

                he0 = halfEdge(p0, p1, idx=k)
                he0.next_idx = k + 1
                hes[3 * cell_id] = he0

                he1 = halfEdge(p1, p2, idx=k + 1)
                he1.next_idx = k + 2
                hes[3 * cell_id + 1] = he1

                he2 = halfEdge(p2, p0, idx=k + 2)
                he2.next_idx = k
                hes[3 * cell_id + 2] = he2

                cells[cell_id] = (he0, he1, he2)

                k += 3

        return nodes, hes, cells
