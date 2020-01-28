import time
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
            cx = random.randint(30, 330)
            cy = random.randint(180, 360)
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

    startTime = time.time()
    # Create point array [[x, y], [x, y, ...]]
    x_vals = []
    y_vals = []
    for x in range(-rw//2, 1+rw//2, 5):
        for y in range(-rh//2, 1+rh//2, 5):
            x_vals.append(x)
            y_vals.append(y)

    points = numpy.vstack((x_vals, y_vals))

    # Loop through angles:
    for ang in range(0, 12):
        angle = math.radians(15 * ang)
        # Create rotation matrix
        c, s = math.cos(angle), math.sin(angle)
        rot_m = numpy.array([[c, -s], [s, c]])
        # Multiply by rotation matrix
        rot_points = numpy.matmul(rot_m, points)
        # Loop through each point and add to obs
        for p in rot_points.T:
            px = int(p[0] / 5)
            py = int(p[1] / 5)
            for o in obstacles:
                try:
                    obs[px + int(o[0]/5)][py + int(o[1]/5)][ang] = True;
                except IndexError:
                    pass

    # exit()
    # for o in obstacles:
    #     for ang in range(0, 12):
    #         angle = math.radians(15 * ang)
    #         c, s = math.cos(angle), math.sin(angle)
    #         # Check robot-sized area around obstacle to see which points collide at angle
    #         for x in range(-rw//2, 1+rw//2, 5):
    #             xc, xs = x*c, x*s
    #             for y in range(-rh//2, 1+rh//2, 5):
    #                 # Rotate point by ang (wrt obstacle center) and find closest grid point
    #                 Px = round(((xc - y*s) + o[0])/5)
    #                 Py = round(((xs + y*c) + o[1])/5)
    #                 # Mark grid point as obstacle (try/except bc point could be off the map)
    #                 try:
    #                     obs[Px][Py][ang] = True;
    #                 except IndexError:
    #                     pass

    print([(c[0]//5, c[1]//5) for c in centers])
    return obs
