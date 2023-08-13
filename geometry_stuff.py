import math


# Using https://rootllama.wordpress.com/2014/06/20/ray-line-segment-intersection-test-in-2d/


def ray_segment_intersection(ray, segment, angle):
    """
    Checks the intersection between a ray and a segment
    :param ray: list, contains two points
    :param segment: List, contains two points (point is a tuple with two integers)
    :return: Tuple, a point which the ray and segment intersects. if it doesn't
    intersect, returns None
    """

    # Using https://stackoverflow.com/questions/14307158/how-do-you-check-for-intersection-between-a-line-segment-and-a-line-ray-emanatin
    # Any point on the segment is representable as q + u s. for a scalar parameter (0 <= u <=1)
    q = segment[0][0], segment[0][1]
    s = segment[1][0] - segment[0][0], segment[1][1] - segment[0][1]
    # s = x2-x1, y2-y1
    angle = -angle
    # Any point on the ray through p is representable as p+tr. for a scalar parameter 0<=t
    r = math.cos(angle), math.sin(angle)
    r = round(r[0], 8), round(r[1], 8)
    p = ray[0], ray[1]
    v1 = q[0] - p[0], q[1] - p[1]
    # Four cases! if r * s == 0
    r_product_s = special_inner_product(r, s)
    if r_product_s == 0:
        if special_inner_product(v1, r) != 0:
            return None
        t0 = inner_product(v1, s) / inner_product(r, r)
        t1 = t0 + inner_product(s, r) / inner_product(r, r)
        if 0 <= abs(t0 - t1) <= 1:
            return None
        else:
            intersect_point = q[0] + t0 * s[0], q[1] + t0 * s[1]
            return intersect_point
    t = special_inner_product(v1, s) / r_product_s
    u = special_inner_product(v1, r) / r_product_s
    if t >= 0 and 0 <= u <= 1:
        intersect_point = p[0] + t * r[0], p[1] + t * r[1]
        return intersect_point
    return None


def inner_product(v1, v2):
    sum_vec = 0
    for i in range(len(v1)):
        sum_vec += v1[i] * v2[i]
    return sum_vec


def special_inner_product(v1, v2):
    return v1[0] * v2[1] - v1[1] * v2[0]

def angle_calculator_radians(source_point, point2):
    """
    Calculates angles between two points
    :param point1: Tuple of two integers, represents the first point
    :param point2: Tuple of two integers, represents the second point
    :return:
    """
    delta_x = point2[0] - source_point[0]
    delta_y = source_point[1] - point2[1]

    rads = math.atan2(delta_y, delta_x)
    #rads %= (2* math.pi)
    return rads
