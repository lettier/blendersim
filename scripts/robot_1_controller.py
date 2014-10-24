'''

David Lettier (C) 2014.

http://www.lettier.com/

BlenderSim Version 2.0

This file controls the robot's movements.

'''

# Imports.

import mathutils
import math
import time
import pickle

bge = bge  # To avoid Flake8 lint errors.


def robot_1_moving():
  '''
    Determines if the robot is still moving by the cardinality of the
    set symmetric difference between the robot's current state and its
    last recorded state.

    If the cardinality is zero, then the robot is not moving.
    If the cardinality is greater than zero, it tests if the movement is
    within a small threshold.
  '''

  robot_1_base = bge.logic.getCurrentScene().objects["robot_1_base"]

  test = {

      "xpos": robot_1_base.worldPosition.x * 100.0,
      "ypos": robot_1_base.worldPosition.y * 100.0,
      "zpos": robot_1_base.worldPosition.z * 100.0,
      "xrot": robot_1_base.worldOrientation.to_euler().x,
      "yrot": robot_1_base.worldOrientation.to_euler().y,
      "zrot": robot_1_base.worldOrientation.to_euler().z

  }

  stopped = len(
      set(test.items()) ^ set(bge.logic.globalDict["robot_1_state"].items())
  )

  if (stopped == 0):

    return False

  else:

    x1 = bge.logic.globalDict["robot_1_simulated_poses"][-2][1]
    y1 = bge.logic.globalDict["robot_1_simulated_poses"][-2][2]
    z1 = bge.logic.globalDict["robot_1_simulated_poses"][-2][3]

    x2 = test["xpos"]
    y2 = test["ypos"]
    z2 = test["zrot"]

    dx = abs(x1 - x2)
    dy = abs(y1 - y2)
    dz = abs(z1 - z2)

    if (dx <= 0.02 and dy <= 0.02 and dz <= 0.00087):

      return False

    else:

      return True


def update_robot_1_state():

  robot_1_base = bge.logic.getCurrentScene().objects["robot_1_base"]

  bge.logic.globalDict["robot_1_state"] = {

      "xpos": robot_1_base.worldPosition.x * 100.0,
      "ypos": robot_1_base.worldPosition.y * 100.0,
      "zpos": robot_1_base.worldPosition.z * 100.0,
      "xrot": robot_1_base.worldOrientation.to_euler().x,
      "yrot": robot_1_base.worldOrientation.to_euler().y,
      "zrot": robot_1_base.worldOrientation.to_euler().z

  }


def stop_robot_1():

  bge.logic.robot_1_wheel_front_L.applyTorque([0.0, 0.0, 0.0], True)
  bge.logic.robot_1_wheel_front_R.applyTorque([0.0, 0.0, 0.0], True)
  bge.logic.robot_1_wheel_back_L.applyTorque([0.0, 0.0, 0.0], True)
  bge.logic.robot_1_wheel_back_R.applyTorque([0.0, 0.0, 0.0], True)


def drop_robot_1_campose_marker():

  robot_1_campose_marker = bge.logic.getCurrentScene().addObject(
      "robot_1_campose_marker",
      obj
  )
  robot_1_campose_marker.worldPosition = obj.worldPosition
  robot_1_campose_marker.worldPosition.z = 23.0 / 100.0


def drop_robot_1_waypoint_marker(waypoint):

  robot_1_waypoint_marker = bge.logic.getCurrentScene().addObject(
      "waypoint_marker",
      obj
  )
  robot_1_waypoint_marker.worldPosition.x = waypoint[1] / 100.0
  robot_1_waypoint_marker.worldPosition.y = waypoint[0] / 100.0
  robot_1_waypoint_marker.worldPosition.z = 25.0 / 100.0


def add_sim_pose():

  bge.logic.globalDict["robot_1_simulated_poses"].append(
      [
          time.time() * 1000.0,
          obj.worldPosition[0] * 100.0,
          obj.worldPosition[1] * 100.0,
          obj.worldOrientation.to_euler().z
      ]
  )

# Globals.

local = True

world = False

# Get the controller.

controller = bge.logic.getCurrentController()

# Get the game object that the controller is attached to.

obj = controller.owner

# Initialize variables and flags.

if (obj["init"] is True):

  obj["init"] = False

  # Robot 1's wheels.

  bge.logic.robot_1_wheel_front_L = bge.logic.getCurrentScene().objects[
      "robot_1_wheel_front_L"
  ]
  bge.logic.robot_1_wheel_front_R = bge.logic.getCurrentScene().objects[
      "robot_1_wheel_front_R"
  ]
  bge.logic.robot_1_wheel_back_L = bge.logic.getCurrentScene().objects[
      "robot_1_wheel_back_L"
  ]
  bge.logic.robot_1_wheel_back_R = bge.logic.getCurrentScene().objects[
      "robot_1_wheel_back_R"
  ]

  bge.logic.robot_1_last_move_time = time.time() * 1000.0

  update_robot_1_state()

  bge.logic.globalDict["robot_1_waypoints"] = [
      "stop"
  ]

  bge.logic.globalDict["robot_1_simulated_poses"] = []

  add_sim_pose()

if (
    (bge.logic.globalDict["robot_1_waypoints"][0] != "stop") and
    (not robot_1_moving()) and
    ((time.time() * 1000.0) - bge.logic.robot_1_last_move_time >= 0.0)
):

  # Get and drop the next waypoint in the arena.
  # Note that waypoint[1] = X and waypoint[0] = Y.

  waypoint = bge.logic.globalDict["robot_1_waypoints"][0]

  drop_robot_1_waypoint_marker(waypoint)

  # Calculate the angle to turn in order to face the waypoint.

  # Convert the waypoint to a 3D vector.

  waypoint = mathutils.Vector((waypoint[1], waypoint[0], 1.0))

  # Translate the waypoint to the robot's local space.

  mat_trans = mathutils.Matrix.Translation(
      (
          -obj.worldPosition[0] * 100.0,
          -obj.worldPosition[1] * 100.0,
          -obj.worldPosition[2] * 100.0
      )
  )

  waypoint_trans = mat_trans * waypoint

  waypoint_rot = mathutils.Matrix.Rotation(
      -obj.worldOrientation.to_euler()[2], 4, "Z"
  ) * waypoint_trans

  # Now that the waypoint world coordinate is transformed to the
  # robot's local space, compute the angle between the robot's x-axis
  # and the waypoint line going from the robot's origin to the waypoint.

  rotateZ = math.atan2(waypoint_rot[1], waypoint_rot[0])

  # First turn and then move forward.

  rotateZ = rotateZ * 180.0 / math.pi

  if (abs(rotateZ) < 1.0):  # Turn error threshold.

    a = 82.7271515601
    b = 23.12349975
    c = waypoint_rot[0]
    f = (a / b) * c

    bge.logic.robot_1_wheel_front_L.applyTorque([0.0, 0.0, f], True)
    bge.logic.robot_1_wheel_front_R.applyTorque([0.0, 0.0, f], True)
    bge.logic.robot_1_wheel_back_L.applyTorque([0.0, 0.0, f], True)
    bge.logic.robot_1_wheel_back_R.applyTorque([0.0, 0.0, f], True)

    print(
        '[robot_1_controller]',
        'Reached waypoint:',
        bge.logic.globalDict["robot_1_waypoints"][0][::-1]
    )

    bge.logic.globalDict["robot_1_waypoints"] = bge.logic.globalDict[
        "robot_1_waypoints"
    ][1:]

  elif (rotateZ < 0.0):

    a = 20.8
    b = 44.260811
    c = abs(rotateZ)
    t = (a / b) * c

    bge.logic.robot_1_wheel_front_L.applyTorque([0.0, 0.0, t], True)
    bge.logic.robot_1_wheel_front_R.applyTorque([0.0, 0.0, -t], True)
    bge.logic.robot_1_wheel_back_L.applyTorque([0.0, 0.0, t], True)
    bge.logic.robot_1_wheel_back_R.applyTorque([0.0, 0.0, -t], True)

  elif (rotateZ > 0.0):

    a = 20.8
    b = 44.260811
    c = abs(rotateZ)
    t = (a / b) * c

    bge.logic.robot_1_wheel_front_L.applyTorque([0.0, 0.0, -t], True)
    bge.logic.robot_1_wheel_front_R.applyTorque([0.0, 0.0, t], True)
    bge.logic.robot_1_wheel_back_L.applyTorque([0.0, 0.0, -t], True)
    bge.logic.robot_1_wheel_back_R.applyTorque([0.0, 0.0, t], True)

  bge.logic.robot_1_last_move_time = time.time() * 1000.0

update_robot_1_state()

stop_robot_1()

add_sim_pose()

drop_robot_1_campose_marker()

if (not robot_1_moving()):

  # The robot is no longer moving so pickle out its simulated camera poses or
  # positions for later analysis.

  pickle_file = open("./pickled_data/robot_1_simulated_motion.pkl", "wb")

  pickle.dump(
      bge.logic.globalDict["robot_1_simulated_poses"],
      pickle_file,
      protocol=2,
      fix_imports=True
  )

  pickle_file.close()
