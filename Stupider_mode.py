import pygame as pg
from settings import *
import math
import random
from geometry_stuff import *

class LightSource:
    def __init__(self, points, polys=None):
        if polys is None:
            polys = []
        self.x, self.y = points[0], points[1]
        self.polys = polys  # List of Polygons
        self.layer = screen

    def update(self):
        source_point = pg.mouse.get_pos()
        self.x, self.y = source_point[0], source_point[1]
        pg.draw.circle(self.layer, WHITE, (self.x, self.y), 3)
        # Stupider mode
        self.stupider_mode()

        # Stupid mode
        # self.stupid_mode()

        # Smarter moder
        # for poly in self.polys:
        #     for point in poly.get_points():
        #         pg.draw.line(self.layer, WHITE, source_point, point)

    def add_polys(self, poly):
        self.polys.append(poly)

    def remove_polys(self, poly):
        if poly in self.polys:
            self.polys.remove(poly)

    def stupider_mode(self):
        new_point = (self.x, self.y)
        angle = angle_calculator_radians((400, 400), new_point)
        new_point, distance, poly_wall = self.make_ray(angle)
        if new_point is not None:
            pg.draw.line(self.layer, WHITE, (400, 400), new_point)

    def stupid_mode(self):
        angle = 0
        while angle < math.pi * 2:
            angle += (math.pi * 2) / 18
            new_point = self.make_ray(angle)
            if new_point is not None:
                pg.draw.line(self.layer, WHITE, (self.x, self.y),
                             self.make_ray(angle))

    def make_ray(self, angle=90):
        closet_intersect = [None, 0, None]  # point,distance, Polygon
        mouse_point = 400, 400
        for polygon in self.polys:
            for wall in polygon.get_walls():
                intersect = ray_segment_intersection(mouse_point, wall,angle)
                #intersect = self.calculate_intersection2((mouse_point,
                #                                         [math.cos(
                #                                             angle) + 400,
                #                                          math.sin(
                #                                              angle) + 400]),
                #                                        wall)
                if not closet_intersect[0] and intersect:
                    closet_intersect[0] = intersect
                    closet_intersect[1] = distance_between_points([400,
                                                                   400],
                                                                  intersect)
                    closet_intersect[2] = [polygon, wall]
                elif intersect and closet_intersect[0]:
                    if closet_intersect[1] \
                            > distance_between_points([400, 400],
                                                      intersect):
                        closet_intersect[0] = intersect
                        closet_intersect[1] = distance_between_points([400,400],
                                                                      intersect)
                        closet_intersect[2] = [polygon, wall]
        return closet_intersect
        # slope = math.tan(angle)  # The m in -> m*x+c = 0
        # closet_intersect = None
        # for polygon in self.polys:
        #    intersect = self.calculate_intersection([(400,400)], polygon)
        #    if intersect is not None and intersect < closet_intersect:
        #        closet_intersect = intersect
        # return self.x, slope * (self.x)
        # if 0 <= angle <= 90:
        #     new_point = (MAX_X, slope * MAX_X)
        # elif 90 < angle <= 180:
        #     new_point = (-MAX_X, slope * MAX_X)
        # elif 180 < angle <= 270:
        #     new_point = (-MAX_X, -slope * MAX_X)
        # else:
        #     new_point = (MAX_X, -slope * MAX_X)
        # return new_point

    # def check_object_intersections(self, new_point):
    #     for polygon in self.polys:
    #         product = self.calculate_intersection(new_point,
    #                                               polygon.get_points())
    #         if product:
    #             return product[0]


    def calculate_intersection2(self, ray, segment):
        """
        Makes two y =mx+c stuff and then calculates the intersections
        :param ray:
        :param segment:
        :return:
        """
        # Only the ray is inifinte! (did it for a line, not a ray)
        x1 = ray[0][0]
        y1 = ray[0][1]
        x2 = ray[1][0]
        y2 = ray[1][1]
        if x2-x1 != 0:
            m_ray = (y2-y1) / (x2-x1)
        else:
            m_ray = 0
        c_ray = y2-m_ray*x2

        x3 = segment[0][0]
        y3 = segment[0][1]
        x4 = segment[1][0]
        y4 = segment[1][1]
        if x3-x4 != 0:
            m_seg = (y4 - y3) / (x4 - x3)
        else:
            m_seg = 0
        c_seg = y3 - m_seg*x3

        if m_ray - m_seg == 0:
            return None
        intersect_point_x = (c_seg-c_ray) / (m_ray-m_seg)
        intersect_point_y = (m_seg*intersect_point_x +c_seg)
        if x3 >= x4:
            if y3 >= y4:
                if x4 <= intersect_point_x <= x3 and y4 <= intersect_point_y <= y3:
                    return intersect_point_x, intersect_point_y
            else:
                if x4 <= intersect_point_x <= x3 and y4 >= intersect_point_y >= y3:
                    return intersect_point_x, intersect_point_y
        else:
            if y3 >= y4:
                if x4 >= intersect_point_x >= x3 and y4 <= intersect_point_y <= y3:
                    return intersect_point_x, intersect_point_y
            else:
                if x4 >= intersect_point_x >= x3 and y4 >= intersect_point_y >= y3:
                    return intersect_point_x, intersect_point_y

        return None


    def calculate_intersection(self, ray, segment):
        r_px = ray[0][0]
        r_py = ray[0][1]
        r_dx = ray[1][0] - r_px  # The actual length of the ray in x axis
        r_dy = ray[1][1] - r_py  # The actual length of the ray in y axis

        s_px = segment[0][0]
        s_py = segment[0][1]
        s_dx = segment[1][0] - s_px
        s_dy = segment[1][1] - s_py

        r_mag = math.sqrt(r_dx ** 2 + r_dy ** 2)
        s_mag = math.sqrt(s_dx ** 2 + s_dy ** 2)
        if r_dx / r_mag == s_dx / s_mag and r_dy / r_mag == s_dy / s_mag:
            return None
        if s_dx * r_dy - s_dy * r_dx == 0:
            T2 = (r_dx * (s_py - r_py) + r_dy * (r_px - s_px))
        else:
            T2 = (r_dx * (s_py - r_py) + r_dy * (r_px - s_px)) / (
                    s_dx * r_dy - s_dy * r_dx)
        if r_dx == 0:
            T1 = s_px + s_dx * T2 - r_px
        else:
            T1 = (s_px + s_dx * T2 - r_px) / r_dx

        if T1 < 0 or T2 < 0 or T2 > 1:
            return None
        # print(r_px + r_dx * T1, r_py + r_dy * T1)
        return r_px + r_dx * T1, r_py + r_dy * T1


class Polygon:
    def __init__(self, points):
        self.points = points
        self.walls = [(points[i - 1], points[i]) for i in range(len(points))]

    def update(self):
        for wall in self.walls:
            pg.draw.line(screen, WHITE, wall[0], wall[1])

    def get_walls(self):
        return self.walls

    def get_points(self):
        return self.points


pg.init()
font = pg.font.SysFont('ARIAL', 32)
screen = pg.display.set_mode(WINDOW_SIZE)
display = pg.Surface((MAX_X, MAX_Y))
pg.display.set_caption("Light_Test")
clock = pg.time.Clock()
screen.fill(DARK)
# p4 = [(100, 150), (120, 50), (120, 50), (200, 80), (200, 80), (140, 210),
#      (140, 210), (100, 150)]

p4 = [(100, 150), (120, 50), (200, 80), (140, 210)]
p5 = Polygon([(100, 200), (120, 250), (60, 300)])
p6 = Polygon([(200, 260), (220, 150), (300, 200), (350, 320)])
p7 = Polygon([(340, 60), (360, 40), (370, 70)])
p8 = Polygon([(450, 190), (560, 170), (540, 270), (430, 290), ])
p9 = Polygon([(400, 95), (580, 50), (480, 150)])
light_point = LightSource(pg.mouse.get_pos())
pol = Polygon(p4)
light_point.add_polys(pol)
light_point.add_polys(p5)
light_point.add_polys(p6)
light_point.add_polys(p7)
light_point.add_polys(p8)
light_point.add_polys(p9)
light_point.add_polys(
    Polygon([(0, 0), (0, MAX_Y), (MAX_X, MAX_Y), (MAX_X, 0)]))
running = True
while running:
    clock.tick(60)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    # Drawing
    screen.fill(DARK)
    light_point.update()
    pol.update()  # pg.draw.polygon(screen, WHITE, p4, width=2)
    p5.update()
    p6.update()
    p7.update()
    p8.update()
    p9.update()
    pg.display.update()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
