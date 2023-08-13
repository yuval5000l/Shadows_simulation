import pygame as pg
from settings import *
from geometry_stuff import *


# Flags here are:
# 0 - impenterable wall
# 1 - Player
# 2 - Mirror?

class Player:
    def __init__(self, screen):
        self.rect = pg.Rect(30, 30, 30, 30)
        self.layer = screen
        self.walls = [Wall(self.rect.topleft, self.rect.topright, 1),
                      Wall(self.rect.bottomleft, self.rect.topleft, 1),
                      Wall(self.rect.bottomleft, self.rect.bottomright, 1),
                      Wall(self.rect.bottomright, self.rect.topright, 1)]

    def update(self):
        pg.draw.rect(self.layer, GREEN, self.rect, 3)

    def get_points(self):
        return [self.rect.topleft, self.rect.topright,
                self.rect.bottomleft, self.rect.bottomright]

    def get_walls(self):
        return self.walls

    def hit_by_light(self):
        # print("HIT DAT SWEET PLAYER")
        pass


class LightSource:
    def __init__(self, points, polys=None):
        if polys is None:
            polys = []
        self.x, self.y = points[0], points[1]
        self.polys = polys  # List of Polygons
        self.layer = screen
        self.endpoints = [poly.get_points() for poly in self.polys]

    def update(self):
        source_point = pg.mouse.get_pos()
        self.x, self.y = source_point[0], source_point[1]
        pg.draw.circle(self.layer, WHITE, (self.x, self.y), 3)
        self.casting_rays()

    def add_polys(self, poly):
        self.polys.append(poly)

    def remove_polys(self, poly):
        if poly in self.polys:
            self.polys.remove(poly)

    def sort_endpoints(self):
        self.endpoints = []
        source_point = self.x, self.y
        for poly in self.polys:
            for point in poly.get_points():
                self.endpoints.append(point)

        angle_measure = angle_helper(source_point)
        self.endpoints = sorted(self.endpoints, key=angle_measure)

    def casting_rays(self):
        source_point = self.x, self.y
        wall_check = []
        counter = 0
        self.sort_endpoints()
        for point in self.endpoints:
            for fix in [-0.00001, 0, 0.00001]:
                # for fix in [-0.00001,0, 0.00001]:
                angle = angle_calculator_radians(source_point, point)
                new_point, distance, poly_wall = self.make_ray(angle + fix)
                if new_point is not None and new_point not in wall_check:
                    if poly_wall[1].flag == 1:
                        leyla.hit_by_light()
                    wall_check.append(new_point)
                    counter += 1
        draw_polygon_alpha(self.layer, WHITE, wall_check)
        # for i in range(len(wall_check)):
        # pg.draw.line(self.layer, RED, wall_check[i - 1], wall_check[i],
        #             width=2)

    def make_ray(self, angle=90):
        closet_intersect = [None, 0, None]  # point,distance, Polygon
        mouse_point = self.x, self.y
        for polygon in self.polys:
            for wall in polygon.get_walls():
                intersect = ray_segment_intersection(mouse_point,
                                                     wall.get_points(), angle)
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
                        closet_intersect[1] = distance_between_points(
                            [self.x, self.y], intersect)
                        closet_intersect[2] = [polygon, wall]
        return closet_intersect


def closet_point(source, point1, point2):
    distance_point1 = distance_between_points(source, point1)
    distance_point2 = distance_between_points(source, point2)
    if distance_point1 < distance_point2:
        return point1
    return point2


# def light_up(wall):
#     pg.draw.line(screen, RED, wall.get_points()[0], wall.get_points()[1],
#                  width=2)


class Polygon:
    def __init__(self, points):
        self.points = points
        self.walls = [Wall(points[i - 1], points[i]) for i in
                      range(len(points))]

    def update(self):
        for wall in self.walls:
            pg.draw.line(screen, LIGHT, wall.get_points()[0],
                         wall.get_points()[1], 3)

    def get_walls(self):
        return self.walls

    def get_points(self):
        return self.points


class Wall:
    def __init__(self, point, endpoint, flag=0):
        if point[0] < endpoint[0]:
            self.endpoint = point
            self.endpoint2 = endpoint
        elif point[0] == endpoint[0]:
            if point[1] > endpoint[1]:
                # point y is bigger than endpoint y
                self.endpoint = point
                self.endpoint2 = endpoint
            else:
                self.endpoint = endpoint
                self.endpoint2 = point
        else:
            self.endpoint = endpoint
            self.endpoint2 = point
        self.flag = flag

    def get_points(self):
        return self.endpoint, self.endpoint2

    def closet_endpoint(self, point):
        endpoint_distance = distance_between_points(self.endpoint, point)
        endpoint2_distance = distance_between_points(self.endpoint2, point)
        if endpoint_distance < endpoint2_distance:
            return self.endpoint
        return self.endpoint2

    def farthest_endpoint(self, point):
        if self.closet_endpoint(point) == self.endpoint:
            return self.endpoint2
        return self.endpoint

    def is_point_in_wall(self, point):
        if self.endpoint2[0] >= point[0] >= self.endpoint[0]:
            if self.endpoint2[1] > self.endpoint[1]:
                if self.endpoint2[1] >= point[1] >= self.endpoint[0]:
                    return True
            elif self.endpoint2[1] <= point[1] <= self.endpoint[0]:
                return True
        else:
            if self.endpoint2[1] > self.endpoint[1]:
                if self.endpoint2[1] >= point[1] >= self.endpoint[0]:
                    return True
            elif self.endpoint2[1] <= point[1] <= self.endpoint[0]:
                return True
        return False

    # TODO
    def check_light_wall(self, point):
        if self.endpoint[0] < point[0] < self.endpoint2[0]:
            pass


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
leyla = Player(screen)
light_point.add_polys(leyla)

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
    leyla.update()
    light_point.update()
    pg.display.update()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
