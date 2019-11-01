import slicer_workshop as sw
from matplotlib import pyplot
from stl import mesh


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


# triangles = create_triangles_from_stl('pyramid.stl')
triangles = create_triangles()

for i in range(0, len(triangles)-1):
    for k in range(1, len(triangles)):
        if sw.has_common_edge(triangles[i], triangles[k]):
            print(f'Triangle № {i+1} has common edge with the triangle № {k+1}')

# Creating a test plane
plane = sw.Plane(0.2)

# Finding triangles, wich intersect the plane
triangle_numbers = [num for num in range(len(triangles)) if triangles[num].is_intersects_plane(plane)]

# Finding intersections
intersections = [sw.Intersection(triangles[k], plane) for k in triangle_numbers]

# Printing intersections types
for i in range(len(intersections)):
    print(f'Triangle № {triangle_numbers[i] + 1} intersects the plane by the {intersections[i].type} type')
    print(f'Points count: {intersections[i].points["count"]}')
    for n in range(intersections[i].points['count']):
        print(f'{n + 1}) {intersections[i].points["points"][n]};')

# Dividing data to x and y
X = [intersections[k].points['points'][i][0] for k in range(len(intersections))
     for i in range(intersections[k].points['count'])]
Y = [intersections[k].points['points'][i][1] for k in range(len(intersections))
     for i in range(intersections[k].points['count'])]

X.append(X[0])
Y.append(Y[0])

print(X)
print(Y)

pyplot.plot(X, Y)
pyplot.show()
