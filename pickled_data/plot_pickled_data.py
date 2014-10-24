'''

David Lettier (C) 2014.

http://www.lettier.com/

BlenderSim 2.0

Plots the BlenderSim sim-posses pickled data.

'''

import sys
import numpy
import math
import pickle
import matplotlib.pyplot as plt
# import matplotlib.mlab as mlab
# from mpl_toolkits.mplot3d import Axes3D
# from matplotlib import cm
# from matplotlib.patches import Rectangle
# from scipy.stats import scoreatpercentile
# from scipy.stats import normaltest
# from scipy.stats import norm
# from scipy.stats import probplot
# from scipy.stats import mode


def rotate_point(x, y, angle_r):
  '''
    Rotates a point around the origin, counter-clockwise.
  '''

  x_rot = (math.cos(angle_r) * x) + (-math.sin(angle_r) * y)
  y_rot = (math.sin(angle_r) * x) + (math.cos(angle_r) * y)

  return x_rot, y_rot

real_robot_file = open("../waypoint_logs/1.log", "r")

line = real_robot_file.readline()

rm = []

while(line != ""):

  if (line.find("CAMPOSE") != -1):

    line_splitted = line.split(" ")

    rm.append([float(line_splitted[6]), float(line_splitted[7]), 0.0])

  line = real_robot_file.readline()

seen = []

for i in rm:

  if i not in seen:

    seen.append(i)

rm = seen

xr = []
yr = []

for i in rm:

  xr.append(i[0])
  yr.append(i[1])

robot_1_simulated_motion = pickle.load(
    open("./robot_1_simulated_motion.pkl", "rb")
)

ts = list(map(lambda a: a[0], robot_1_simulated_motion))
xs = list(map(lambda a: a[1], robot_1_simulated_motion))
ys = list(map(lambda a: a[2], robot_1_simulated_motion))
zs = list(map(lambda a: a[3], robot_1_simulated_motion))

sm = []

for i in range(len(xs)):

  sm.append([xs[i], ys[i], 0.0])

robot_positions = [
    # [ 25, 100],
    [100, 100],  # Robot 1 starting position.
    # [100,  25],
    # [ 25,  25]
]

# Robot 1 task points from ../task_points_configurations/a.conf
task_points = [
    [100.0, 89.5],
    [155.0, 50.0],
    [89.5, 206.0],
    [501.5, 89.5]
]

# Waypoints from ../waypoint_logs/1.log
# for robot 1.
waypoints = [
    (100, 89),
    (94, 96),
    (117, 73),
    (140, 50),
    (155, 50),
    (140, 50),
    (117, 73),
    (94, 96),
    (71, 119),
    (71, 142),
    (48, 165),
    (48, 188),
    (71, 211),
    (89, 206),
    (71, 211),
    (71, 234),
    (94, 257),
    (117, 257),
    (140, 257),
    (163, 257),
    (186, 257),
    (186, 257),
    (209, 257),
    (232, 257),
    (232, 257),
    (255, 257),
    (278, 257),
    (301, 257),
    (324, 257),
    (347, 257),
    (370, 257),
    (393, 257),
    (416, 257),
    (439, 257),
    (462, 234),
    (485, 211),
    (508, 188),
    (508, 165),
    (508, 142),
    (508, 119),
    (501, 89)
]

wp = []

for i in waypoints:

  wp.append([i[0], i[1], 0.0])

arena_walls = [
    [[0, 0], [0, 538]],
    [[205, 205], [0, 206]],
    [[422, 422], [0, 206]],
    [[602, 602], [0, 538]],
    [[422, 422], [336, 538]],
    [[205, 205], [336, 538]],
    [[105, 205], [206, 206]],
    [[315, 422], [206, 206]],
    [[315, 520], [336, 336]],
    [[105, 205], [336, 336]],
    [[0, 602], [538, 538]],
    [[0, 602], [0, 0]]
]

# First plot.

plt.figure(1)

plt.title("BlenderSim \n Simulated versus Real Robot Motion")
# plt.title("BlenderSim \n Arena")

plt.axis("equal")

plt.xlabel("X-axis in Centimeters")
plt.ylabel("Y-axis in Centimeters")

plt.yticks(numpy.arange(0, 553, 23), rotation=0)
plt.xticks(numpy.arange(0, 633, 23), rotation=90)

plt.grid(True)

for i in arena_walls:

  plt.plot(i[0], i[1], "-k", linewidth=3.0)

plt.plot(xr, yr, "--o", color=(0.0, 0.4, 0.8), alpha=0.5)

plt.plot(xs, ys, "-or", alpha=0.5)

for i in robot_positions:

  plt.plot(i[0], i[1], "sw")

for i in task_points:

  plt.plot(i[0], i[1], "dw", markersize=12.0, linewidth=3.0)

for i in waypoints:

  plt.plot(i[0], i[1], "ow", markersize=6.0)

simu = plt.Circle((0, 0), 0.2, color="r", alpha=0.8)
real = plt.Circle((0, 0), 0.2, color=(0.0, 0.4, 0.8), alpha = 0.8)

plt.legend([real, simu], ["Real", "Simulated"])


# DISTANCES ----------------

def Lettier_Distance(P, Q):
  '''
    Imagine you have a rubber band connected to the two starting point
    positions in both P and Q. At each step, you advance one end of the rubber
    band to the next point in P and the other end of the rubber band to the
    next point in Q. If the distance grows between points Pi and Qi, the rubber
    band stretches but never shrinks. The resulting length of the rubber band
    is the max Euclidean distance once you reach Pn and Qn.

    If |P| < |Q| then keep advancing through the points in Q while keeping the
    one end of the rubber band fixed at the last point in P.

    If |P| > |Q| then keep advancing through the points in P while keeping the
    one end of the rubber band fixed at the last point in Q.
  '''

  max_distance = 0.0

  i = 0

  for Pi in P:

    Qi = None

    try:

      Qi = Q[i]

    except IndexError:

      # |P| > |Q|

      i = i - 1

      # Last point in Q.

      Qi = Q[i]

    delta_x = Qi[0] - Pi[0]
    delta_y = Qi[1] - Pi[1]
    delta_z = Qi[2] - Pi[2]

    distance = math.sqrt(
        math.pow(delta_x, 2) + math.pow(delta_y, 2) + math.pow(delta_z, 2)
    )

    if max_distance < distance:

      max_distance = distance

    i = i + 1

  # i = |P| - 1

  i = i - 1

  # Last point index in P.

  j = i

  if i != len(Q) - 1:

    # |P| < |Q|

    # Last point in P.

    Pi = P[j]

    for k in range(i + 1, len(Q)):

      # Keep advancing through Q.

      Qi = Q[k]

      delta_x = Qi[0] - Pi[0]
      delta_y = Qi[1] - Pi[1]
      delta_z = Qi[2] - Pi[2]

      distance = math.sqrt(
          math.pow(delta_x, 2) + math.pow(delta_y, 2) + math.pow(delta_z, 2)
      )

      if max_distance < distance:

        max_distance = distance

  return max_distance


def Frechet_Distance(P, Q):

  distance_matrix_PxQ = []

  for Pi in P:

    Pi_distances = []

    for Qi in Q:

      delta_x = Qi[0] - Pi[0]
      delta_y = Qi[1] - Pi[1]
      delta_z = Qi[2] - Pi[2]

      distance = math.sqrt(
          math.pow(delta_x, 2) + math.pow(delta_y, 2) + math.pow(delta_z, 2)
      )

      Pi_distances.append(distance)

    distance_matrix_PxQ.append(Pi_distances)

  i = 0
  j = 0

  max_distance = 0.0

  while True:

    if (i == len(P) - 1) and (j == len(Q) - 1):

      break

    elif i == len(P) - 1:  # i is all the way down the matrix.

      # You can only go to the right in the matrix.

      right_distance = distance_matrix_PxQ[i][j + 1]

      if max_distance < right_distance:

        max_distance = right_distance

      j = j + 1

    elif j == len(Q) - 1:  # j is all the way to the right of the matrix.

      # You can only go down the matrix.

      down_distance = distance_matrix_PxQ[i + 1][j]

      if max_distance < down_distance:

        max_distance = down_distance

      i = i + 1

    else:

      diagonal_distance = distance_matrix_PxQ[i + 1][j + 1]  # a
      right_distance = distance_matrix_PxQ[i][j + 1]  # b
      down_distance = distance_matrix_PxQ[i + 1][j]  # c

      if diagonal_distance <= right_distance:  # If a <= b

        if diagonal_distance <= down_distance:  # If a <= c

          # Go diagonal.

          if max_distance < diagonal_distance:

            max_distance = diagonal_distance

          i = i + 1
          j = j + 1

        else:  # c < a

          # Go down.

          if max_distance < down_distance:

            max_distance = down_distance

          i = i + 1

      else:  # b < a

        if right_distance <= down_distance:  # If b <= c

          # Go right.

          if max_distance < right_distance:

            max_distance = right_distance

          j = j + 1

        else:  # c < b

          # Go down.

          if max_distance < down_distance:

            max_distance = down_distance

          i = i + 1

  return max_distance


def Hausdorff_Distance(P, Q):

  def Directed_Hausdorff_Distance(P, Q):

    max_min_distance = 0.0

    for Pi in P:

      min_distance = sys.float_info.max

      for Qi in Q:

        delta_x = Qi[0] - Pi[0]
        delta_y = Qi[1] - Pi[1]
        delta_z = Qi[2] - Pi[2]

        distance = math.sqrt(
            math.pow(delta_x, 2) + math.pow(delta_y, 2) + math.pow(delta_z, 2)
        )

        if distance < min_distance:

          min_distance = distance

      if min_distance > max_min_distance:

        max_min_distance = min_distance

    return max_min_distance

  return max(
      Directed_Hausdorff_Distance(P, Q), Directed_Hausdorff_Distance(Q, P)
  )

print("Simulated vs. Real:")
print("Lettier Distance: ", Lettier_Distance(sm, rm))
print("Frechet Distance: ", Frechet_Distance(sm, rm))
print("Hausdorff Distance: ", Hausdorff_Distance(sm, rm))
print("\n")
print("Real vs. Waypoints:")
print("Lettier Distance: ", Lettier_Distance(rm, wp))
print("Frechet Distance: ", Frechet_Distance(rm, wp))
print("Hausdorff Distance: ", Hausdorff_Distance(rm, wp))
print("\n")
print("Simulated vs. Waypoints:")
print("Lettier Distance: ", Lettier_Distance(sm, wp))
print("Frechet Distance: ", Frechet_Distance(sm, wp))
print("Hausdorff Distance: ", Hausdorff_Distance(sm, wp))

# --------------------------

plt.show()
