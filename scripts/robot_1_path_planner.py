'''

David Lettier (C) 2014.

http://www.lettier.com/

BlenderSim Version 2.0

This file calculates the A* path to the task points (for robot 1)
unless you set compute_a_star_path to False. If False, the path is
the previous HRTeam waypoints from the log of the previously run
experiment.

'''

import math
import time
import copy

bge = bge  # To avoid Flake8 lint errors.

# True: Compute an A* path.
# False: Use Waypoints from HRTeam.
compute_a_star_path = False

small_cost = 1.0
diagonal_cost = math.sqrt(2.0 * small_cost * small_cost)
small_cost = 23
diagonal_cost = 33


def find_node(width, height):

  i = math.floor(height / 23.0)
  j = math.floor(width / 23.0)

  n = (i * 27) + j

  return (n, i, j)


def get_node_neighbors(nodes, node):

  # Node: (
  #   number,
  #   (i, j),
  #   terrain_cost,
  #   g_cost,
  #   h_cost,
  #   f_cost,
  #   parent_node_name
  # )

  i = node[1][0]
  j = node[1][1]

  neighbors = []

  e = j + 1

  if (e <= 26):

    neighbors.append(nodes[(i * 27) + e])

  ne = (i + 1, j + 1)

  if (ne[0] <= 23 and ne[1] <= 26):

    neighbors.append(nodes[(ne[0] * 27) + ne[1]])

  n = i + 1

  if (n <= 23):

    neighbors.append(nodes[(n * 27) + j])

  nw = (i + 1, j - 1)

  if (nw[0] <= 23 and nw[1] >= 0):

    neighbors.append(nodes[(nw[0] * 27) + nw[1]])

  w = j - 1

  if (w >= 0):

    neighbors.append(nodes[(i * 27) + w])

  sw = (i - 1, j - 1)

  if (sw[0] >= 0 and sw[1] >= 0):

    neighbors.append(nodes[(sw[0] * 27) + sw[1]])

  s = i - 1

  if (s >= 0):

    neighbors.append(nodes[(s * 27) + j])

  se = (i - 1, j + 1)

  if (se[0] >= 0 and se[1] <= 26):

    neighbors.append(nodes[(se[0] * 27) + se[1]])

  return neighbors


def movement_cost(node1, node2):

  # Node: (
  #   number,
  #   (i, j),
  #   terrain_cost,
  #   g_cost,
  #   h_cost,
  #   f_cost,
  #   parent_node_name
  # )

  di = abs(node1[1][0] - node2[1][0])
  dj = abs(node1[1][1] - node2[1][1])

  if (di == 1 and dj == 1):

    return diagonal_cost + node2[2]

  else:

    return small_cost + node2[2]


def heuristic_cost(node1, node2, mode=0):

  # Node: (
  #   number,
  #   (i, j),
  #   terrain_cost,
  #   g_cost,
  #   h_cost,
  #   f_cost,
  #   parent_node_name
  # )

  if (mode > 2):

    mode = 2

  x1 = bge.logic.globalDict["arena_grid_centers"][node1[1][0]][node1[1][1]][1]
  y1 = bge.logic.globalDict["arena_grid_centers"][node1[1][0]][node1[1][1]][0]

  x2 = bge.logic.globalDict["arena_grid_centers"][node2[1][0]][node2[1][1]][1]
  y2 = bge.logic.globalDict["arena_grid_centers"][node2[1][0]][node2[1][1]][0]

  dx = abs(x1 - x2)
  dy = abs(y1 - y2)

  if (mode == 0):  # HRTeam, Diagonal Distance

    dd = min(dx, dy) * diagonal_cost + (max(dx, dy) - min(dx, dy)) * small_cost

    return dd

  elif (mode == 1):  # Euclidean

    return math.sqrt(dx * dx + dy * dy)

  elif (mode == 2):  # Manhattan

    return dx + dy


def a_star_path(start, end, nodes):

  # Node: (
  #   number,
  #   (i, j),
  #   terrain_cost,
  #   g_cost,
  #   h_cost,
  #   f_cost,
  #   parent_node_name
  # )

  open_set = []
  closed_set = []

  sn = nodes[find_node(start[0], start[1])[0]]
  en = nodes[find_node(end[0], end[1])[0]]

  open_set.append(sn)

  # a_star_markers = []

  path_found = False

  while (len(open_set) != 0):

    open_set.sort(key=lambda x: x[5], reverse=False)

    current_node = open_set[0]

    open_set.remove(current_node)

    closed_set.append(current_node)

    nodes[current_node[0]] = current_node

    if (sn[0] == current_node[0]):

      ii = current_node[1][0]
      jj = current_node[1][1]

      x = bge.logic.globalDict["arena_grid_centers"][ii][jj][1] - (23.0 / 2)
      y = bge.logic.globalDict["arena_grid_centers"][ii][jj][0] - (23.0 / 2)

      a_star_marker = bge.logic.getCurrentScene().addObject(
          "a_star_start_marker",
          obj
      )
      a_star_marker.worldPosition.x = x / 100.0
      a_star_marker.worldPosition.y = y / 100.0
      a_star_marker.worldPosition.z = 0.0

      path_found = True

    elif (en[0] == current_node[0]):

      ii = current_node[1][0]
      jj = current_node[1][1]

      x = bge.logic.globalDict["arena_grid_centers"][ii][jj][1] - (23.0 / 2)
      y = bge.logic.globalDict["arena_grid_centers"][ii][jj][0] - (23.0 / 2)

      a_star_marker = bge.logic.getCurrentScene().addObject(
          "a_star_end_marker",
          obj
      )
      a_star_marker.worldPosition.x = x / 100.0
      a_star_marker.worldPosition.y = y / 100.0
      a_star_marker.worldPosition.z = 0.0

      path_found = True

      break

    else:

      ii = current_node[1][0]
      jj = current_node[1][1]

      x = bge.logic.globalDict["arena_grid_centers"][ii][jj][1] - (23.0 / 2)
      y = bge.logic.globalDict["arena_grid_centers"][ii][jj][0] - (23.0 / 2)

      a_star_marker = bge.logic.getCurrentScene().addObject(
          "a_star_search_marker",
          obj
      )
      a_star_marker.worldPosition.x = x / 100.0
      a_star_marker.worldPosition.y = y / 100.0
      a_star_marker.worldPosition.z = 0.0

    current_node_neighbors = get_node_neighbors(nodes, current_node)

    for neighbor in current_node_neighbors:

      if (neighbor in closed_set):

        continue

      g_temp = current_node[3] + movement_cost(current_node, neighbor)

      h_temp = heuristic_cost(neighbor, en, 2)

      if (not (neighbor in open_set)):

        h = h_temp

        g = g_temp

        f = g + h

        neighbor[3] = g
        neighbor[4] = h
        neighbor[5] = f
        neighbor[6] = current_node[0]

        nodes[neighbor[0]] = neighbor

        open_set.append(neighbor)

      elif (neighbor in open_set):

        if g_temp < neighbor[3]:

          open_set.remove(neighbor)

          h = h_temp

          g = g_temp

          f = g + h

          neighbor[3] = g
          neighbor[4] = h
          neighbor[5] = f
          neighbor[6] = current_node[0]

          nodes[neighbor[0]] = neighbor

          open_set.append(neighbor)

  if (path_found is True):

    path_squares = [en[0]]

    current_node = en
    parent_node = nodes[en[6]]

    while(parent_node[0] != current_node[0]):

      ii = current_node[1][0]
      jj = current_node[1][1]

      x = bge.logic.globalDict["arena_grid_centers"][ii][jj][1]
      y = bge.logic.globalDict["arena_grid_centers"][ii][jj][0]

      a_star_marker = bge.logic.getCurrentScene().addObject(
          "a_star_path_marker",
          obj
      )
      a_star_marker.worldPosition.x = x / 100.0
      a_star_marker.worldPosition.y = y / 100.0
      a_star_marker.worldPosition.z = 0.0

      current_node = parent_node
      parent_node = nodes[current_node[6]]

      path_squares.insert(0, current_node[0])

    ii = parent_node[1][0]
    jj = parent_node[1][1]

    x = bge.logic.globalDict["arena_grid_centers"][ii][jj][1]
    y = bge.logic.globalDict["arena_grid_centers"][ii][jj][0]

    a_star_marker = bge.logic.getCurrentScene().addObject(
        "a_star_path_marker",
        obj
    )
    a_star_marker.worldPosition.x = x / 100.0
    a_star_marker.worldPosition.y = y / 100.0
    a_star_marker.worldPosition.z = 0.0

    return path_squares

  else:

    return None

# Get the controller in Blender that is attached to this script.

controller = bge.logic.getCurrentController()

# Get the game object that the controller is attached to.

obj = controller.owner

# Blender calls this script each game loop so we cannot
# initialize each game loop. Thus get the "init" property
# of the control and set it to False that this portion of code
# only gets called once.

if (obj["init"] is True):

  obj["init"] = False  # Don't run this again.

  bge.logic.globalDict["robot_1_path_planner_start_time"] = (
      time.time() * 1000.0
  )

  bge.logic.globalDict["load_robot_1_waypoints"] = False

  bge.logic.globalDict["arena_grid_centers"] = []

  width = 602.0 + 23.0
  height = 538.0 + 23.0

  wall_cost = 500000000.0

  c = 23.0 / 2.0

  ii = 0
  jj = 0

  i = c
  j = c

  nodes = []
  n = 0

  while (True):

    row = []

    j = c

    jj = 0

    while (True):

      row.append((i, j))

      # |-------------------------|
      # |       |    12   |       |
      # |       |         |       |
      # |       |         |       |
      # |       |         |       |
      # |      5|        6|       |
      # |       |         |       |
      # |       |         |       |
      # |   10  |     11  |       |
      # |   ----|   -----------   |
      # |                         |
      # |                         |
      # |1                       4|
      # |                         |
      # |    8        9           |
      # |   ----|    -----|       |
      # |       |         |       |
      # |       |         |       |
      # |       |         |       |
      # |       |2        |3      |
      # |       |         |       |
      # |       |    7    |       |
      # |-------------------------|

      # if (width and height in blocks)

      if ((jj == 0) and (ii >= 0 and ii <= 23)):

        # 1
        # Node: (
        #   number,
        #   (i, j),
        #   terrain_cost,
        #   g_cost,
        #   h_cost,
        #   f_cost,
        #   parent_node_name
        # )

        nodes.append([n, (ii, jj), wall_cost, 0.0, 0.0, 0.0, n])

      elif ((jj == 8) and (ii >= 0 and ii <= 8)):

        # 2

        nodes.append([n, (ii, jj), wall_cost, 0.0, 0.0, 0.0, n])

      elif ((jj == 18) and (ii >= 0 and ii <= 8)):

        # 3

        nodes.append([n, (ii, jj), wall_cost, 0.0, 0.0, 0.0, n])

      elif ((jj == 26) and (ii >= 0 and ii <= 23)):

        # 4

        nodes.append([n, (ii, jj), wall_cost, 0.0, 0.0, 0.0, n])

      elif ((jj == 8) and (ii >= 14 and ii <= 23)):

        # 5

        nodes.append([n, (ii, jj), wall_cost, 0.0, 0.0, 0.0, n])

      elif ((jj == 18) and (ii >= 14 and ii <= 23)):

        # 6

        nodes.append([n, (ii, jj), wall_cost, 0.0, 0.0, 0.0, n])

      elif ((jj >= 0 and jj <= 26) and (ii == 0)):

        # 7

        nodes.append([n, (ii, jj), wall_cost, 0.0, 0.0, 0.0, n])

      elif ((jj >= 4 and jj <= 8) and (ii >= 8 and ii <= 9)):

        # 8

        nodes.append([n, (ii, jj), wall_cost, 0.0, 0.0, 0.0, n])

      elif ((jj >= 13 and jj <= 18) and (ii >= 8 and ii <= 9)):

        # 9

        nodes.append([n, (ii, jj), wall_cost, 0.0, 0.0, 0.0, n])

      elif ((jj >= 4 and jj <= 8) and (ii == 14)):

        # 10

        nodes.append([n, (ii, jj), wall_cost, 0.0, 0.0, 0.0, n])

      elif ((jj >= 13 and jj <= 22) and (ii == 14)):

        # 11

        nodes.append([n, (ii, jj), wall_cost, 0.0, 0.0, 0.0, n])

      elif ((jj >= 0 and jj <= 26) and (ii == 23)):

        # 12

        nodes.append([n, (ii, jj), wall_cost, 0.0, 0.0, 0.0, n])

      else:

        nodes.append([n, (ii, jj), 0.0, 0.0, 0.0, 0.0, n])

      n += 1

      j += 23.0

      jj += 1

      if (j >= width):

        break

    bge.logic.globalDict["arena_grid_centers"].append(row)

    i += 23.0

    ii += 1

    if (i >= height):

      break

  # All task points from ../task_points_configurations/a.conf
  # for all robots.
  # all_task_points = [
  #     (100.0, 100.0),
  #     (100.0, 89.5),
  #     (501.5, 448.5),
  #     (501.5, 89.5),
  #     (100.0, 448.5),
  #     (150.5, 269.0),
  #     (301.0, 89.5),
  #     (301.0, 448.5),
  #     (451.5, 269.0),
  #     (89.5, 336.0),
  #     (89.5, 206.0),
  #     (260.0, 336.0),
  #     (260.0, 206.0),
  #     (561.0, 336.0),
  #     (561.0, 206.0),
  #     (155.0, 50.0),
  #     (155.0, 488.0),
  #     (365.0, 50.0),
  #     (365.0, 488.0),
  #     (551.5, 50.0),
  #     (551.5, 488.0)
  # ]

  # Robot 1 task points from ../task_points_configurations/a.conf
  robot_1_task_points = [
      (100.0, 100.0),
      (100.0, 89.5),
      (155.0, 50.0),
      (89.5, 206.0),
      (501.5, 89.5)
  ]

  # Waypoints from ../waypoint_logs/1.log
  # for robot 1.
  # [0] is Y and [1] is X.
  robot_1_waypoints = [
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

  bge.logic.globalDict["robot_1_path"] = []

  if (compute_a_star_path is False):

    for i in range(len(robot_1_waypoints)):

      print('[robot_1_path_planner]', 'Adding waypoint:', robot_1_waypoints[i])

      bge.logic.globalDict["robot_1_path"].append(
          (robot_1_waypoints[i][1], robot_1_waypoints[i][0])
      )

  else:

    for t in range(1, len(robot_1_task_points)):

      nodes_copy = copy.deepcopy(nodes)

      tp_path = a_star_path(
          robot_1_task_points[t - 1],
          robot_1_task_points[t],
          nodes_copy
      )

      if (tp_path is not None):

        for k in range(0, len(tp_path) - 1):

          i = nodes_copy[tp_path[k]][1][0]
          j = nodes_copy[tp_path[k]][1][1]

          bge.logic.globalDict["robot_1_path"].append(
              bge.logic.globalDict["arena_grid_centers"][i][j]
          )

        bge.logic.globalDict["robot_1_path"].append(
            (robot_1_task_points[t][1], robot_1_task_points[t][0])
        )

  bge.logic.globalDict["robot_1_path"].append("stop")

  bge.logic.globalDict["load_robot_1_waypoints"] = True

if (
    ((time.time() * 1000.0) - bge.logic.globalDict[
        "robot_1_path_planner_start_time"
    ] >= 1000.0) and
    (bge.logic.globalDict["load_robot_1_waypoints"])
):

  bge.logic.globalDict["robot_1_waypoints"] = bge.logic.globalDict[
      "robot_1_path"
  ]

  bge.logic.globalDict["load_robot_1_waypoints"] = False
