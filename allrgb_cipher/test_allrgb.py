import allrgb
import hilbert
import graphs
import math

import random

bits = 6
image_size = (1 << (3 * bits // 2))


def pixels_bfs(image_size):
    return graphs.bfs(*graphs.tree_to_graph(graphs.random_spanning_tree(graphs.grid_graph(image_size, image_size))))


def pixels_hilbert(image_size):
    h = hilbert.Hilbert(2)
    for k in range(image_size * image_size):
        yield h.encode(k)


def cube_create():
    n = 1 << bits

    cube = []
    filler = cube_fill()

    for k in range(n):
        row_of_columns = []
        for j in range(n):
            column = []
            for i in range(n):
                # column.append((next(filler) + i//2, next(filler) + j//2, next(filler) + k//2))
                column.append(( i, j, int(math.fabs(50*(math.sin(10*(i**2 + j**2))))) ))
            row_of_columns.append(column)
        cube.append(row_of_columns)

    return cube


def cube_fill():
    with open("filename.txt") as fileobj:
        for line in fileobj:
            for ch in line:
                if (ord(ch) > 96) and (ord(ch) < 123):
                    yield (ord(ch)-97)
                else:
                    continue


cube = cube_create()
print(cube)


def cube_interpreter(coords):
    element = tuple(cube[coords[0]][coords[1]][coords[2]])

    return element


def colors_bfs(bits):
    colors = graphs.bfs(*graphs.tree_to_graph(graphs.random_spanning_tree(
        graphs.grid_graph(1 << bits, 1 << bits, 1 << bits))))
    for color in colors:
        # yield [c << (8 - bits) for c in color]
        yield [c << (8 - bits) for c in cube_interpreter(color)]

def colors_hilbert(bits):
    h = hilbert.Hilbert(3)
    for k in range(1 << (3 * bits)):
        # yield [c << (8 - bits) for c in h.encode(k)]
        yield [c << (8 - bits) for c in cube_interpreter(h.encode(k))]


filename = 'pixelbfs_colorhilbert_cipher' + '.png'
filename_ = 'pixelhilbert_colorhilbert_cipher' + '.png'
_filename_ = 'pixelbfs_colorbfs_cipher' + '.png'
print(filename)
# allrgb.show((image_size*2, image_size), pixels_bfs(image_size), colors_hilbert(bits), filename)
allrgb.show((image_size, image_size), pixels_bfs(image_size), colors_hilbert(bits), filename)
# allrgb.show((image_size, image_size), pixels_hilbert(image_size), colors_hilbert(bits), filename_)
# allrgb.show((image_size, image_size), pixels_bfs(image_size), colors_bfs(bits), _filename_)
