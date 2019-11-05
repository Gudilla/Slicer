import slicer_workshop as sw
from matplotlib import pyplot
from stl import mesh
import numpy as np


# Creating a triangle set
def create_triangles():
    tri = list()
    # ADF
    tri.append(sw.Triangle([0, 1, 0], [0, 0, 0], [0.5, 0.5, 0]))
    # ADE
    tri.append(sw.Triangle([0, 1, 0], [0, 0, 0], [0.5, 0.5, 1]))
    # BFC
    tri.append(sw.Triangle([1, 1, 0], [0.5, 0.5, 0], [1, 0, 0]))
    # BEC
    tri.append(sw.Triangle([1, 1, 0], [0.5, 0.5, 1], [1, 0, 0]))
    # AFB
    tri.append(sw.Triangle([0, 1, 0], [0.5, 0.5, 0], [1, 1, 0]))
    # AEB
    tri.append(sw.Triangle([0, 1, 0], [0.5, 0.5, 1], [1, 1, 0]))
    # DFC
    tri.append(sw.Triangle([0, 0, 0], [0.5, 0.5, 0], [1, 0, 0]))
    # DEC
    tri.append(sw.Triangle([0, 0, 0], [0.5, 0.5, 1], [1, 0, 0]))
    return tri


def create_triangles_from_stl(filename):
    model = mesh.Mesh.from_file(filename)
    tri = [sw.Triangle(model.vectors[i][0], model.vectors[i][1], model.vectors[i][2]) for i in range(len(model.vectors))]
    return tri


def calculate_scale(filename=''):
    if filename == '':
        scale_min = -0.1
        scale_max = 1.1
    else:
        model = mesh.Mesh.from_file(filename)
        scale_min = min(model.min_[0], model.min_[1])
        scale_max = max(model.max_[0], model.max_[1])
        scale_min -= scale_max / 10
        scale_max += scale_max / 10
    return tuple([scale_min, scale_max])


triangles = create_triangles_from_stl('cone.stl')
# triangles = create_triangles()
scale = calculate_scale('cone.stl')

for i in range(0, len(triangles)-1):
    for k in range(1, len(triangles)):
        if sw.has_common_edge(triangles[i], triangles[k]):
            print(f'Triangle № {i+1} has common edge with the triangle № {k+1}')

for j in range(10):
    step = 10
    # Creating a test plane
    plane = sw.Plane(j*step)

    # Finding triangles, wich intersect the plane
    triangle_numbers = [num for num in range(len(triangles)) if triangles[num].is_intersects_plane(plane)]
    print(triangle_numbers)

    # Finding intersections
    intersections = [sw.Intersection(triangles[k], plane) for k in triangle_numbers]

    # Printing intersections types
    for i in range(len(intersections)):
        print(f'Triangle № {triangle_numbers[i] + 1} intersects the plane by the {intersections[i].type} type')
        print(f'Points count: {intersections[i].points["count"]}')
        X, Y = [], []
        for n in range(intersections[i].points['count']):
            print(f'{n + 1}) {intersections[i].points["points"][n]};')
            X.append(intersections[i].points["points"][n][0])
            Y.append(intersections[i].points["points"][n][1])
        pyplot.plot(X, Y, color='green')

    pyplot.xlim(scale)
    pyplot.ylim(scale)
    pyplot.axis('off')
    pyplot.savefig(f'figure{j+1}')
    pyplot.clf()

