import math
import random
import numpy

# Some relevant definitions
rw = 50
rh = 100

startx = random.randint(15, 60)
starty = 90

endx = 36
endy = 1

width = 360
height = 540

def generate_obstacles():
    #
    #    THIS PART JUST RANDOMLY GENERATES OBSTACLES
    #

    dist = lambda x1, y1, x2, y2: math.sqrt((x2-x1) ** 2 + (y2-y1) ** 2)
    numObstacles = 5
    b = 2

    obstacles = []
    centers = []

    for i in range(numObstacles):
        dim = None
        while (dim is None):
            cx = random.randint(30, width - 30)
            cy = random.randint(int(0.33 * height), int(0.67 * height))
            cr = random.randint(30, 50) / 2

            if all(dist(c[0], c[1], cx, cy) >= cr + c[2] for c in centers):
                dim = (cx, cy, cr)
                centers.append(dim)

        for a in numpy.linspace(0, 2 * math.pi, num=10):
            px = int(dim[0] + dim[2] * math.cos(a) + random.uniform(-0.3, 7))
            py = int(dim[1] + dim[2] * math.sin(a) + random.uniform(-0.3, 7))

            obstacles.append((px, py))

    #
    #   ACTUAL 3D PART
    #
    obs = [[[False for a in range(0, 12)] for y in range(1+height//5)] for x in range(1+width//5)]

    for o in obstacles:
        for ang in range(0, 180, 15):
            angle = ang * math.pi / 180
            c, s = math.cos(angle), math.sin(angle)
            # Check robot-sized area around obstacle to see which points collide at angle
            for x in range(-rw//2, 1+rw//2, 5):
                for y in range(-rh//2, 1+rh//2, 5):
                    # Rotate point by ang (wrt obstacle center) and find closest grid point
                    Px = int(((x*c - y*s) + o[0])//5)
                    Py = int(((x*s + y*c) + o[1])//5)
                    # Mark grid point as obstacle
                    try:
                        obs[Px][Py][ang//15] = True;
                    except IndexError:
                        pass

    print([(c[0]//5, c[1]//5) for c in centers])
    return obs
