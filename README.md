![Alt text](https://raw.githubusercontent.com/lettier/blendersim/thesis_proof_of_concept/screenshot.jpg)

# BlenderSim

## Dependencies

* OS
  * Python2
  * Blender 2.72
* Python
  * numpy
  * matplotlib
  * scipy

## Quickstart

```bash
cd blendersim  
blender BlenderSim.2.blend  
```  
[File] > [External Data] > [Find Missing Files] > Navigate to BlenderSim directory. > [Find Missing Files]  
Press [p] over the game window.
```bash
cd pickled_data/  
python2 plot_pickled_data.py  
```
Or if you do not have Python 3 but only 2 installed.
```bash
cd pickled_data/  
python plot_pickled_data.py  
```

## Overview

Over the course of three months, a Blender based simulation was developed for HRTeam titled BlenderSim.
Initially, BlenderSim was wholly physics based, but soon proved to be problematic on three fronts: time,
scale, and intricacy. The problems faced by using the physics engine to model the locomotion of the robots
gave way to the thesis of tuning the physics engine via a genetic algorithm. In the interim, the physics engine
was abandoned and a constant linear motion model was used, in order to progress on the development of
the BlenderSim 3D simulation environment.

As a proof of concept of the thesis, BlenderSim was revisited with the physics engine providing the
motion model, using the best-fitness parameters learned by BBAutoTune. Using one robot, the motion of the
simulated, physics-based robot was compared to the real robot by re-running a previously logged HRTeam
experiment in BlenderSim.

## Preliminary Work

Initial problems arose when the treads of the SRV-1 were recreated in the simulation. Even after numerous
hours adjusting physics parameters and rigid-body configurations, the treads would consistently behave in
erratic fashions.

Scale was problematic as the Blender/Bullet physics engine has difficulty with collisions of objects
that have a size outside of the assumed range of .05 to 10 meters. Objects smaller than .05 (5cm)
Blender/Bullet units, in any given dimension, erratically jitter despite having no force acting upon them.
As such, since the wheel dimensions of the real SRV-1 are 2.11cm x 2.45cm x 2.52cm, the to-scale 3D model
of the SRV-1 was affected by this scale limitation of the physics engine.

To rectify these issues, the default physics engine was not used to provide a motion model and
was only kept to keep the robots from running through each other and the arena. In its place, a constant linear
and angular velocity motion model was developed which only moves the 3D robot as if it were a single point
body.

## Evaluation

For the purposes of the proof of concept, most of the original architecture of BlenderSim was simplified.
The simulation contained one robot, one robot controller, one robot path planner, and the arena. The purpose
was to evaluate the efficacy of the physics parameters learned by BBAutoTune, when deployed in
the simulated robot environment and measured in comparison with its physical robot counterpart.

## Arena

The arena is a 602cm x 538cm enclosure with a main hallway and six compartments. The floor and all of
walls are physics based in BlenderSim and respond accordingly should any robot try to pass through them.
All dimensions and proportions of the simulated arena match the real arena used in HRTeam
experiments.

## Surveyor SRV-1 Blackfin 3D Model

The physics parameters governing the wheels were the same best-fitness parameters found by BBAutoTune.
Residing 1.37cm off of the arena floor from their local origins in the positive global
z-axis, the robot's base and wheels had their z-translation fixed. This distance between the wheels and
the floor is important since this was the same height used to the tune the physics engine parameters in
BBAutoTune. Using any other height would result in different motion from the motion observed during tuning.

## Robot Path Planner

Given a HRTeam experiment log and a robot number, the path planner extracts the waypoints that the
real robot was instructed to go to during the HRTeam experiment. These waypoints come from an A*
calculated path that runs from the robot’s starting position to various points of interest or task points. With
the waypoints extracted from the log file, the robot path planner populates the robot controller’s waypoint
queue.

## Robot Controller

The robot controller is expressed in the simulation as the base of the SRV-1 3D model.
Contained in its logic is a path or waypoint queue that it runs through. This queue is populated by the
robot path planner. For each waypoint in the queue, the robot controller will first rotate the robot towards
the point and then move the robot forward to reach the point. Once the robot moves forward, the waypoint
is removed from the queue.

For either rotating or moving the robot, the robot controller can only apply torque to the robot’s
wheels—no other force or mechanism is used. Recalling from subsection 4.5.2 and section 4.6, a torque
setting of 82.7271515601 resulted in the simulated robot moving forward 23.12349975cm. Since turning had
not been learned by BBAutoTune, there were no baseline values of torque versus rotation. To correct for
this, the torque value for the robot’s left wheels was set to −20.8 while the torque value for the right wheels
was set to 20.8 resulting in an in-place rotation of 44.260811 degrees. Note that, the torque value ±20.8 was
chosen arbitrarily.

Using these torque versus displacement values, the robot controller linearly interpolates the amount
of torque needed to first rotate the robot towards a waypoint (to within 1 degree) and then move the robot
forward to reach the waypoint. While rotating, if the robot over or undershoots the orientation needed to
face the waypoint, the robot controller will continuously interpolate the torque needed to get the robot facing
the waypoint to within 1 degree. Depending on the sign of the angle needed to orient the robot towards the
waypoint, the robot controller will either rotate the robot counter-clockwise or clockwise by applying the
same magnitude but opposing signs of torque to either the left or right wheels. While moving forward, if
the robot over or undershoots the position of the waypoint, the robot controller performs no correction but
proceeds to orient and move the robot towards the next waypoint in the queue (if there is one). Note that
for moving the robot forward, the robot controller applies the same torque value to all four wheels.

## Task Points Manager

HRTeam experiments have five predefined sets of interest pointsâ or task points that the robots visit as
they travel around the arena. BlenderSim imitates this using its task points manager. At the start of the
simulation, the task points manager reads the five configurations from the task points configuration directory.
Controls include keys a through e where each key corresponds to five possible task point configurations.

## Platform

BlenderSim was run on a 64bit Linux operating system with 32GB of RAM and an Intel Core i7-4770K four
core processor running at 3.9GHz.

## Experimental Design

To compare the simulated versus real robot motion (using the physics engine and the best-fitness physics
parameters found by BBAutoTune), a HRTeam experiment was re-run in BlenderSim but for only one
robotâspecifically robot one with a starting position at (100cm, 100cm). The A* path (the waypoints) and
the task points that the real robot one was instructed to travel along were extracted from the experimentâs
log file. Positioning the simulated robot at the same starting position as the real robot in the experiment,
the simulated robot was instructed to travel along the same set of waypoints and task points as the real
robot was instructed to.

## Experimental Result

Comparing the simulated versus real robot paths, the discrete Frechet and Hausdorff distances between them
were 40.575953633cm and 19.1208685021cm respectively. Between the simulated and real robot paths, the
real robot path was the most dissimilar from the waypoint path (the waypoint path is the collection of
waypoints that start at the robot's starting position and then travel to the four task points in the arena).

_(C) 2014 David Lettier._  
http://www.lettier.com/
