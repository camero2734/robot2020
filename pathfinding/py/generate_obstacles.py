
import time
import math
import random
import numpy

from dataclasses import dataclass
from typing import Any

# Some relevant definitions
class robot:
    w = 50
    h = 100

class start:
    x = random.randint(15, 60)
    y = 90

class end:
    x = 36
    y = 1

@dataclass
class Point:
    x: Any
    y: Any
    r: Any=0
    a: Any=0
    w: Any=0
    h: Any=0
    def __repr__(self):
        return f"({self.x}, {self.y})"

def generate_obstacles():
    #
    #    THIS PART JUST RANDOMLY GENERATES OBSTACLES
    #

    dist = lambda x1, y1, x2, y2: math.sqrt((x2-x1) ** 2 + (y2-y1) ** 2)
    numObstacles = 5
    b = 2
    width = 360
    height = 540

    obstacles = []
    centers = []

    for i in range(numObstacles):
        dim = None
        while (dim is None):
            cx = random.randint(30, width - 30)
            cy = random.randint(int(0.33 * height), int(0.67 * height))
            cr = random.randint(30, 50) / 2

            if all(dist(c.x, c.y, cx, cy) >= cr + c.r for c in centers):
                dim = Point(x = cx, y = cy, r = cr)
                centers.append(dim)

        for a in numpy.linspace(0, 2 * math.pi, num=10):
            px = int(dim.x + dim.r * math.cos(a) + random.uniform(-0.3, 7))
            py = int(dim.y + dim.r * math.sin(a) + random.uniform(-0.3, 7))

            obstacles.append(Point(x = px, y = py))

    #
    #   ACTUAL 3D PART
    #
    obs = [[[False for a in range(0, 180, 15)] for y in range(109)] for x in range(73)]

    for o in obstacles:
        for ang in range(0, 180, 15):
            # Check square area around obstacle to see which points collide at angle
            for dx in range(-100, 100, 5):
                for dy in range(-100, 100, 5):
                    # Determine if point intersects rotated robot
                    if pointInRobot(Point(x=o.x + dx, y=o.y + dy), Point(x=o.x, y=o.y, a=ang-75, w=robot.w, h=robot.h)):
                        try:
                            obs[int(math.round((o.x+dx)/5))][int(math.round((o.y+dy)/5))][a] = True;
                        except:
                            pass

    return obs

#
#     Helper function that uses the rotation matrix to check if an obstacle is
#     inside of the rotated robot
#
def pointInRobot(o, r):
    # Set origin of o to r center
    o_p = Point(x=o.x - r.x, y=o.y - r.y)
    # Rotation angle
    _a = -r.a * math.pi / 180
    # Rotate angle
    P = Point(x=o_p.x*math.cos(_a) - o_p.y*math.sin(_a), y=o_p.x*math.sin(_a) + o_p.y*math.cos(_a))

    insideX = P.x > -r.w / 2 and P.x < r.w / 2
    insideY = P.y > -r.h / 2 and P.y < r.h / 2

    return insideX and insideY




obstacles = generate_obstacles()
print(len(obstacles))
