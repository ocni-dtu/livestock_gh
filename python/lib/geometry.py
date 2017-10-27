__author__ = "Christian Kongsgaard"
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Christian Kongsgaard"
__email__ = "ocni@dtu.dk"
__status__ = "Work in Progress"

#----------------------------------------------------------------------------------------------------------------------#
#Functions and Classes

def fix_mesh(mesh, detail="normal"):
    from numpy.linalg import norm
    import pymesh

    bbox_min, bbox_max = mesh.bbox
    diag_len = norm(bbox_max - bbox_min)
    if detail == "normal":
        target_len = diag_len * 1e-2
    elif detail == "high":
        target_len = diag_len * 5e-3
    elif detail == "low":
        target_len = diag_len * 0.03
    print("Target resolution: {} mm".format(target_len))

    count = 0
    mesh, __ = pymesh.remove_degenerated_triangles(mesh, 100)
    mesh, __ = pymesh.split_long_edges(mesh, target_len)
    num_vertices = mesh.num_vertices
    while True:
        mesh, __ = pymesh.collapse_short_edges(mesh, 1e-6)
        mesh, __ = pymesh.collapse_short_edges(mesh, target_len,
                preserve_feature=True)
        mesh, __ = pymesh.remove_obtuse_triangles(mesh, 150.0, 100)
        if mesh.num_vertices == num_vertices:
            break

        num_vertices = mesh.num_vertices
        print("#v: {}".format(num_vertices))
        count += 1
        if count > 10:
            break

    mesh = pymesh.resolve_self_intersection(mesh)
    mesh, __ = pymesh.remove_duplicated_faces(mesh)
    mesh = pymesh.compute_outer_hull(mesh)
    mesh, __ = pymesh.remove_duplicated_faces(mesh)
    mesh, __ = pymesh.remove_obtuse_triangles(mesh, 179.0, 5)
    mesh, __ = pymesh.remove_isolated_vertices(mesh)

    return mesh


def ray_triangle_intersection(ray_near, ray_dir, V):
    """
    Möller–Trumbore intersection algorithm in pure python
    Based on http://en.wikipedia.org/wiki/M%C3%B6ller%E2%80%93Trumbore_intersection_algorithm
    """
    import numpy as np

    v1 = V[0]
    v2 = V[1]
    v3 = V[2]
    eps = 0.000001
    edge1 = v2 - v1
    edge2 = v3 - v1
    pvec = np.cross(ray_dir, edge2)
    det = edge1.dot(pvec)

    if abs(det) < eps:
        return False, None

    inv_det = 1. / det
    tvec = ray_near - v1
    u = tvec.dot(pvec) * inv_det
    if u < 0. or u > 1.:
        return False, None

    qvec = np.cross(tvec, edge1)
    v = ray_dir.dot(qvec) * inv_det
    if v < 0. or u + v > 1.:
        return False, None

    t = edge2.dot(qvec) * inv_det
    if t < eps:
        return False, None

    return True, t


def lowestFaceVertex(v0, v1, v2):
    from numpy import array

    V = [v0, v1, v2]
    x0 = v0[0]
    y0 = v0[1]
    z0 = v0[2]
    x1 = v1[0]
    y1 = v1[1]
    z1 = v1[2]
    x2 = v2[0]
    y2 = v2[1]
    z2 = v2[2]
    X = [x0, x1, x2]
    Y = [y0, y1, y2]
    Z = [z0, z1, z2]


    Zsort = sorted(Z)

    if Zsort[0] == Zsort[2]:
        return array([sum(X)/3, sum(Y)/3, sum(Z)/3])

    elif Zsort[0] < Zsort[1]:
        i = Z.index(Zsort[0])
        return V[i]

    elif Zsort[0] == Zsort[1]:
        i0 = Z.index(Zsort[0])
        i1 = Z.index(Zsort[1])
        x = 0.5*(X[i0] + X[i1])
        y = 0.5*(Y[i0] + Y[i1])
        return array([x, y, Zsort[0]])

    else:
        print('Error finding lowest point!')
        print('v0:',v0)
        print('v1:', v1)
        print('v2:', v2)
        return None


def angleBetweenVectors(v1, v2, forceAngle = None):
    """
    Computes the angle between two vectors.
    :param v1: Vector1 as numpy array
    :param v2: Vector2 as numpy array
    :param forceAngle: Default is None. Use to force angle into acute or obtuse.
    :return: Angle in radians and its angle type.
    """

    # Import
    from numpy import dot, sqrt, arccos, pi

    # Dot product
    dot_v1v2 = dot(v1, v2)

    # Determine angle type
    if dot_v1v2 > 0:
        angleType = 'acute'
    elif dot_v1v2 == 0:
        return pi/2, 'perpendicular'
    else:
        angleType = 'obtuse'

    # Vector magnitudes and compute angle
    magV1 = sqrt(v1.dot(v1))
    magV2 = sqrt(v2.dot(v2))
    angle = arccos(abs(dot_v1v2 / (magV1 * magV2)))

    # Compute desired angle type
    if forceAngle == None:
        return angle, angleType

    elif forceAngle == 'acute':
        if angleType == 'acute':
            return angle, 'acute'
        else:
            angle = pi - angle
            return angle, 'acute'

    elif forceAngle == 'obtuse':
        if angle > pi/2:
            return angle, 'obtuse'
        else:
            angle = pi - angle
            return angle, 'obtuse'
    else:
        print('forceAngle has to be defined as None, acute or obtuse. forceAngle was:', str(forceAngle))
        return None, None

def line_intersection(p1, p2, p3, p4):
    """
    Computes the intersection between two lines given 4 points on those lines.
    :param p1: Numpy array. First point on line 1
    :param p2: Numpy array. Second point on line 1
    :param p3: Numpy array. First point on line 2
    :param p4: Numpy array. Second point on line 2
    :return: Numpy array. Intersection point
    """

    # Imports
    from numpy import cross
    from numpy.linalg import norm

    # Direction vectors
    v1 = (p2 - p1)
    v2 = (p4 - p3)

    # Cross-products and vector norm
    cv12 = cross(v1, v2)
    cpv = cross((p1 - p3), v2)
    t = norm(cpv) / norm(cv12)

    return p1 + t * v1