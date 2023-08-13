import pygame as pg
from settings import *
import math
import random


# The main problem here is that we cant make horizontal lines, because r_dx = 0.
# Hope that it won't make a problem in the future

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
        # self.stupider_mode()

        # Stupid mode
        self.stupid_mode()

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
        new_point = self.make_ray()
        if new_point is not None:
            pg.draw.line(self.layer, WHITE, (400, 400), new_point)

    def stupid_mode(self):
        angle = 0
        while angle < math.pi * 2:
            angle += (math.pi * 2) / 18
            new_point, distance, poly_wall = self.make_ray(angle)
            poly_wall[0].light_up(poly_wall[1])
            if new_point is not None:
                pg.draw.line(self.layer, WHITE, (self.x, self.y),
                             new_point)

    def make_ray(self, angle=90):
        closet_intersect = [None, 0, None]  # point,distance, Polygon
        mouse_point = self.x, self.y
        for polygon in self.polys:
            for wall in polygon.get_walls():
                intersect = self.calculate_intersection((mouse_point,
                                                         [math.cos(
                                                             angle) + self.x,
                                                          math.sin(
                                                              angle) + self.y]),
                                                        wall)
                if not closet_intersect[0] and intersect:
                    closet_intersect[0] = intersect
                    closet_intersect[1] = distance_between_points([self.x,
                                                                   self.y],
                                                                  intersect)
                    closet_intersect[2] = [polygon, wall]
                elif intersect and closet_intersect[0]:
                    if closet_intersect[1] \
                            > distance_between_points([self.x, self.y],
                                                      intersect):
                        closet_intersect[0] = intersect
                        closet_intersect[1] = distance_between_points([self.x,
                                                                       self.y],
                                                                      intersect)
                        closet_intersect[2] = [polygon, wall]
        return closet_intersect

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
        if r_dx / r_mag == s_dx / s_mag and r_dy / r_mag == s_dy / s_mag \
                or s_dx * r_dy - s_dy * r_dx == 0 or r_dx == 0:
            return None
        T2 = (r_dx * (s_py - r_py) + r_dy * (r_px - s_px)) / (
                s_dx * r_dy - s_dy * r_dx)
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
            pg.draw.line(screen, LIGHT, wall[0], wall[1], width=3)

    def get_walls(self):
        return self.walls

    def get_points(self):
        return self.points

    def light_up(self, wall):
        pg.draw.line(screen, RED, wall[0], wall[1], width=2)


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
    Polygon([(0, 0), (0, MAX_Y-1), (MAX_X-1, MAX_Y-1), (MAX_X-1, 0)]))
running = True
while running:
    clock.tick(60)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    # Drawing
    screen.fill(LIGHT_NAVY_BLUE)
    pol.update()  # pg.draw.polygon(screen, WHITE, p4, width=2)
    p5.update()
    p6.update()
    p7.update()
    p8.update()
    p9.update()
    light_point.update()
    pg.display.update()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
