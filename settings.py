import math
import pygame as pg

WINDOW_SIZE = (600, 600)
MAX_X = 800
MAX_Y = 800
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
SUN = (100, 150, 100)
DARK = (32, 32, 32)
LIGHT = (192, 192, 192)
SHADOW = (240, 240, 240)
NAVY_BLUE = (0, 0, 100)
LIGHT_NAVY_BLUE = (0, 0, 50)


def angle_calculator_degrees(point1, point2):
    """
    Calculates angles between two points
    -> 0 degrees
    ^ 90 degrees
    <- 180 degrees
    down 270 degrees
    :param point1: Tuple of two integers, represents the first point
    :param point2: Tuple of two integers, represents the second point
    :return:
    """
    delta_x = point1[0] - point2[0]
    delta_y = point2[1] - point1[1]

    rads = math.atan2(delta_y, delta_x)
    #    return rads
    rads %= 2 * math.pi
    degree = math.degrees(rads)
    return degree


def angle_calculator(point1, point2):
    """
    Calculates angles between two points
    -> 0 degrees
    ^ 90 degrees
    <- 180 degrees
    down 270 degrees
    :param point1: Tuple of two integers, represents the first point
    :param point2: Tuple of two integers, represents the second point
    :return:
    """
    delta_x = point2[0] - point1[0]
    delta_y = point2[1] - point1[1]

    rads = math.atan2(delta_y, delta_x)
    rads %= 2 * math.pi
    return rads
    # rads %= 2 * math.pi
    # degree = math.degrees(rads)
    # return degree


def distance_helper(point1):
    point1 = point1

    def temp_distance(point2):
        return math.sqrt(((point2[1] - point1[1]) ** 2) +
                         ((point2[0] - point1[0]) ** 2))

    return temp_distance


def angle_helper(point1):
    source_point = point1

    def angle_rad(point2):
        """
        Calculates angles between two points
        :param point1: Tuple of two integers, represents the first point
        :param point2: Tuple of two integers, represents the second point
        :return:
        """
        delta_x = point2[0] - source_point[0]
        delta_y = source_point[1] - point2[1]

        rads = math.atan2(delta_y, delta_x)
        # rads %= (2* math.pi)
        return rads

    return angle_rad


def distance_between_points(point1, point2):
    return math.sqrt(((point2[1] - point1[1]) ** 2) +
                     ((point2[0] - point1[0]) ** 2))


def sort_by_angle(lst, source_point):
    angle_measure = angle_helper(source_point)
    sorted(lst, key=angle_measure)


def draw_polygon_alpha(surface, color, points):
    if len(points) < 3:
        return
    lx, ly = zip(*points)
    min_x, min_y, max_x, max_y = min(lx), min(ly), max(lx), max(ly)
    target_rect = pg.Rect(min_x, min_y, max_x - min_x, max_y - min_y)
    shape_surf = pg.Surface(target_rect.size, pg.SRCALPHA)
    shape_surf.set_alpha(20)
    pg.draw.polygon(shape_surf, color,
                    [(x - min_x, y - min_y) for x, y in points])
    surface.blit(shape_surf, target_rect)

# def draw_poly_a(surface, color, points, alpha):
