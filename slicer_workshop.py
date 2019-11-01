import numpy as np


def get_start_end(p1, p2, index):
    if p1[index - 1] > p2[index - 1]:
        start = Vertex(p2)
        end = Vertex(p1)
    else:
        start = Vertex(p1)
        end = Vertex(p2)
    return start, end


class Plane:
    def __init__(self, coordinate, axis='z'):
        """
        Collection of plane param's
        :param coordinate: coordinate value
        :param axis: by default is 'z'
        """
        self.coordinate = coordinate
        self.axis = axis
        self.intersection_hashes = list()

    def add_intersection(self, hash_value):
        self.intersection_hashes.append(hash_value)


class Vertex:
    def __init__(self, coordinates):
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.z = coordinates[2]

        self.hash = hash((self.x, self.y, self.z))

    def get_coordinates(self):
        return tuple([self.x, self.y, self.z])


class TriangleEdge:
    def __init__(self, p1, p2, axis='z'):
        """
        Class presents one edge in the triangle, contains it's points of start and end, also coordinate range.
        :param p1: <iterable object>, size 1X3 - 3-dimensional coordinates of the first point.
        :param p2: <iterable object>, size 1X3 - 3-dimensional coordinates of the second point.
        :param axis: ='z' by default, also could be 'y' or 'x', depends on what axis chosen for slicing.
        """
        # TODO: Also function only for z-axis
        #        i = 2
        #        if axis != 'z':
        #            if axis == 'y':
        #                i = 1
        #            if axis == 'x':
        #                i = 0
        if p1[2] == p2[2]:
            if p1[1] == p2[1]:
                # Sort by x-axis
                self.start, self.end = get_start_end(p1, p2, 1)
            else:
                # Sort by y-axis
                self.start, self.end = get_start_end(p1, p2, 2)
        else:
            # Sort by z-axis
            self.start, self.end = get_start_end(p1, p2, 3)

        start_hash = self.start.hash
        end_hash = self.end.hash
        self.hash = hash((start_hash, end_hash))

        self.coordinate_range = self.end.z - self.start.z


class Triangle:
    def __init__(self, p1, p2, p3):
        """
        Class describes the triangle in the 3-D space.
        :param p1: 3-dimensional list of coordinates of the first vertex in the triangle.
        :param p2: 3-dimensional list of coordinates of the second vertex in the triangle.
        :param p3: 3-dimensional list of coordinates of the third vertex in the triangle.
        Also it has "edges" property - describes edges of the triangle.
        Methods: get_triangle(); is_intersects_plane(plane);
        """
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

        self.edges = (TriangleEdge(p1, p2), TriangleEdge(p2, p3), TriangleEdge(p1, p3))

    def get_triangle(self):
        """
        :return: numpy array of triangle vertexes
        """
        return np.array([self.p1, self.p2, self.p3])

    def is_intersects_plane(self, plane):
        """
        Check the plane intersection with the triangle
        :param plane: <Plane class>
        :return: boolean answer
        """
        # TODO: This version only for 'z' axis
        if self.p1[2] == self.p2[2] == self.p3[2] == plane.coordinate:
            return False
        for edge in self.edges:
            if edge.end.z >= plane.coordinate >= edge.start.z:
                return True
        return False


def find_intersection_type(triangle, plane):
    """
    Find out what is the type of intersection
    :param triangle: <TriangleEdge class>
    :param plane: <Plane class>
    :return: integer value -> (1, 2, 3, 4)
    """
    # fourth type -> the triangle lies on the plane -> all three points on the plane
    # TODO: DISABLED IN Triangle class
    if triangle.p1[2] == triangle.p2[2] == triangle.p3[2] == plane.coordinate:
        return 4

    for edge in triangle.edges:
        # first type -> the triangle intersects the plane with two edges -> two intersection points
        if edge.end.z > plane.coordinate > edge.start.z:
            return 1
        # second type -> one of the triangle's edges lies on the plane -> two intersection points
        elif edge.start.z == plane.coordinate and edge.end.z == plane.coordinate:
            return 2

    # third type -> one of the triangle's vertexes lies on the plane -> one intersection point
    if triangle.p1[2] == plane.coordinate or triangle.p2[2] == plane.coordinate or triangle.p3[2] == plane.coordinate:
        return 3


def calculate_intersection_point(edge, plane):
    """
    Function calculates the XY coordinates of intersection point
    :param edge: <TriangleEdge class>
    :param plane: <Plane class>
    :return: tuple(X, Y)
    """
    kx = (edge.start.x - edge.end.x) / (edge.start.z - edge.end.z)
    bx = edge.start.x - kx * edge.start.z
    x = kx * plane.coordinate + bx

    ky = (edge.start.y - edge.end.y) / (edge.start.z - edge.end.z)
    by = edge.start.y - ky * edge.start.z
    y = ky * plane.coordinate + by

    return tuple([x, y])


def has_common_edge(triangle_1, triangle_2):
    for edge_1 in triangle_1.edges:
        for edge_2 in triangle_2.edges:
            if edge_1.hash == edge_2.hash:
                return True
    return False


class Intersection:
    def __init__(self, triangle, plane):
        """
        Class describes the intersection of the plane with the triangle.
        :param triangle: <Triangle class object>
        :param plane: <Plane class object>
        """
        self.type = find_intersection_type(triangle, plane)
        self.points = self.find_intersection_points(triangle, plane)

    def find_intersection_points(self, triangle, plane):
        """
        Set points parameter of the Intersection class object
        :param triangle: <Triangle class>
        :param plane: <Plane class>
        :return: {'count': int(cnt), 'points':[]}
        """
        # TODO: Func supports only the 'z'-axis
        points = {'count': 0, 'points': []}

        # Calculate two intersection points with two edges
        if self.type == 1:
            for edge in triangle.edges:
                if edge.hash in plane.intersection_hashes:
                    continue
                else:
                    if edge.start.z < plane.coordinate < edge.end.z:
                        points['count'] += 1
                        points['points'].append(calculate_intersection_point(edge, plane))
                        plane.add_intersection(edge.hash)

        # Get two intersection points
        elif self.type == 2:
            for edge in triangle.edges:
                if edge.start.hash not in plane.intersection_hashes:
                    if edge.start.z == plane.coordinate:
                        points['points'].append(edge.start.get_coordinates())
                        points['count'] += 1
                        plane.add_intersection(edge.start.hash)
                if edge.end.hash not in plane.intersection_hashes:
                    if edge.end.z == plane.coordinate:
                        points['points'].append(edge.end.get_coordinates())
                        points['count'] += 1
                        plane.add_intersection(edge.end.hash)

        # Get one intersection point
        elif self.type == 3:
            points['count'] = 1
            if triangle.p1[2] == plane.coordinate:
                points['points'] = [triangle.p1]
            elif triangle.p2[2] == plane.coordinate:
                points['points'] = [triangle.p2]
            elif triangle.p3[2] == plane.coordinate:
                points['points'] = [triangle.p3]

        return points
