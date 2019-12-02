import slicer_workshop as sw
from matplotlib import pyplot
from stl import mesh
import os
from PIL import Image


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
    return [scale_min, scale_max]
#    return tuple([scale_min, scale_max])


def calculate_layers_count(step=0.1, filename=''):
    if filename == '':
        return 10
    else:
        model = mesh.Mesh.from_file(filename)
        max_z = model.max_[2]
        min_z = model.min_[2]
        dz = abs(max_z - min_z)
    return int(dz/step)


def clear_directory():
    directory_name = 'pict'
    for filename in os.listdir(directory_name):
        if filename.endswith('.png'):
            os.unlink(directory_name + '/' + filename)


filename = 'example.stl'
step = 10

triangles = create_triangles_from_stl(filename)
print(f'Triangles count = {len(triangles)}')
# triangles = create_triangles()

layers_count = calculate_layers_count(step, filename)

scale = calculate_scale(filename)

try:
    os.mkdir('pict')
except FileExistsError:
    clear_directory()

for j in range(layers_count):
    # Creating a test plane
    plane = sw.Plane(j*step)

    # Finding triangles, wich intersect the plane
    triangle_numbers = [num for num in range(len(triangles)) if triangles[num].is_intersects_plane(plane)]

    # Finding intersections
    intersections = [sw.Intersection(triangles[k], plane) for k in triangle_numbers]

    # Printing intersections types
    fig = pyplot.figure(figsize=(3.2, 3.2))
    ax = fig.add_subplot()
    for i in range(len(intersections)):
        X, Y = [], []
        for n in range(intersections[i].points['count']):
            X.append(intersections[i].points["points"][n][0])
            Y.append(intersections[i].points["points"][n][1])
        ax.plot(X, Y, color='green')

    ax.set_xlim(left=scale[0], right=scale[1])
    ax.set_ylim(bottom=scale[0], top=scale[1])
    ax.set_axis_off()
    fig.savefig(f'pict/figure{j+1}', dpi=200)
    ax.clear()

im = Image.open('pict/figure1.png')
print(im.info)
im.save('pict/test.png', dpi=(200.0, 200.0))
im = Image.open('pict/figure1.png')
print(im.info)
