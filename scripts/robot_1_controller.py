'''

David Lettier
http://www.lettier.com/

BlenderSim version 1.0.

This file controls the robot's movements to the waypoints as fed to it from robot_*_server.py.

'''

# Imports.

import mathutils, math, time, copy, datetime, os;

# Globals.

local = True;

world = False;

# Get the controller.
controller = bge.logic.getCurrentController( );

# Get the game object that the controller is attached to.
obj = controller.owner;

# Initialize variables and flags.
if ( obj[ "init" ] == 1 ):

	obj[ "init" ] = 0;	
	
	obj[ "robot_world_position" ] = str( obj.worldPosition );
	
	bge.logic.robot_1_add_marker = True;
	
	bge.logic.robot_1_robot_body_wPos = copy.deepcopy( obj.worldPosition );
	
	bge.logic.robot_1_rotate = False;
	
	bge.logic.robot_1_time_then = time.time( );
	
	bge.logic.robot_1_laydown_campose_time_then = time.time( );
	
	bge.logic.robot_1_orientation_then = ( obj.worldOrientation.to_euler( )[ 2 ] * 180.0 ) / math.pi;
	
	bge.logic.robot_1_magnitude_then = ( obj.worldPosition - bge.logic.robot_1_robot_body_wPos ).magnitude;
	
	bge.logic.robot_1_inc_then = 0;
	
	bge.logic.robot_1_wait_to_go_forward = 0;
	
	bge.logic.robot_1_angle_moved_sum = 0;
	
	bge.logic.robot_1_turn = 1;
	
	bge.logic.robot_1_turn_by = .096;
	
	bge.logic.robot_1_time_start_of_simulation = time.time( );
	
	bge.logic.robot_1_time_since_last_log = time.time( );
	
	obj[ "traveling" ] = "0";
	obj[ "stopped" ]   = "1";
	
	# Remove the log if it is already created.
	
	try:
		
		os.remove( "./robot_logs/robot_1.log" );
		
	except OSError:
		
		pass;
	
	log_file = open( "./robot_logs/robot_1.log", "a" );
			
	time_stamp = datetime.datetime.fromtimestamp( time.time( ) ).strftime( '%H:%M:%S.%f' );
	
	# Create the headers for the CSV file.
	
	log_file.write( "time_stamp" + "\t" + "time_since_sim_start (seconds)" + "\t" + "time_since_last_log_entry (seconds)" + "\t" + "log_type" + "\t" + "x" + "\t" + "y" + "\t" + "theta" + "\t" + "waypoint" + "\t" + "\n" ) 
	
	log_file.close( );

# Get owner's world orientation. 
orientation = obj.worldOrientation;

obj[ "robot_world_orientation" ] = str( orientation.to_euler( )[ 2 ] );
obj[ "robot_world_position" ] = str( obj.worldPosition );

waypointString = obj[ "waypoint_coordinate" ]; # Get the way point coordinate string.

if ( waypointString != "" ):
	
	obj[ "traveling" ] = "1";
	obj[ "stopped" ]   = "0";	
	
	go = 1;
	
	# Going forward.

	if ( bge.logic.robot_1_turn == 0 ): # Start moving towards the way point if the robot is done turning.

		#left_wheels = [ "robot_1_wheel_front_L", "robot_1_wheel_back_L" ];
	
		#right_wheels = [ "robot_1_wheel_front_R", "robot_1_wheel_back_R" ];

		#for wheel in right_wheels:
			
			#bge.logic.getCurrentScene( ).objects[ wheel ].applyRotation( [ 0, 0.384775442, 0 ], local );
			
		#for wheel in left_wheels:
			
			#bge.logic.getCurrentScene( ).objects[ wheel ].applyRotation( [ 0, 0.384775442, 0 ], local );
		
		obj.applyMovement( [ go * 0.384775442, 0, 0 ], local );
		
		# If the last time a campose was logged and drawn is greater than ~ 33 ms.
		
		if ( ( time.time() - bge.logic.robot_1_laydown_campose_time_then ) >= 0.033989 ):
		
			bge.logic.robot_1_laydown_campose_time_then = time.time( );
		
			campose = bge.logic.getCurrentScene( ).addObject( "robot_1_campose_marker", obj );

			campose.worldPosition = obj.worldPosition;

			campose.worldPosition.z += 3;
			
			log_file = open( "./robot_logs/robot_1.log", "a" );
			
			time_stamp = datetime.datetime.fromtimestamp( time.time( ) ).strftime( '%H:%M:%S.%f' );
			
			log_file.write( str( time_stamp ) + "\t" + str( time.time( ) - bge.logic.robot_1_time_start_of_simulation ) + "\t" + str( time.time( ) - bge.logic.robot_1_time_since_last_log ) + "\t" + " CAMPOSE " + "\t" + str( obj.worldPosition.x ) + "\t" + str( obj.worldPosition.y ) + "\t" + str( orientation.to_euler( )[ 2 ] ) + "\n" ); 
			
			bge.logic.robot_1_time_since_last_log = time.time( );
			
			log_file.close( );
			
		# Calculate distance between robot position and way point position.
	
		p = mathutils.Vector( obj.worldPosition );
		
		q = mathutils.Vector( ( float( waypointString.split( "," )[ 0 ] ), float( waypointString.split( "," )[ 1 ] ), 1.0 ) );

		v = p - q;
		
		dist = math.sqrt( v.dot( v ) );
		
		obj[ "dist_to_waypoint" ] = dist;
			
		if ( dist <= 1.5  ):
				
			# The robot is close enough to the way point, so stop and reset the flags.	
			
			# Log campose in the log file.
			
			log_file = open( "./robot_logs/robot_1.log", "a" );
		
			time_stamp = datetime.datetime.fromtimestamp( time.time( ) ).strftime( '%H:%M:%S.%f' );
		
			log_file.write( str( time_stamp ) + "\t" + str( time.time( ) - bge.logic.robot_1_time_start_of_simulation ) + "\t" + str( time.time( ) - bge.logic.robot_1_time_since_last_log ) + "\t" + " REACHED WAYPOINT " + "\t" + str( obj.worldPosition.x ) + "\t" + str( obj.worldPosition.y ) + "\t" + str( orientation.to_euler( )[ 2 ] ) + "\t" + "(" + obj[ "waypoint_coordinate" ] + ")" + "\n" ); 
		
			bge.logic.robot_1_time_since_last_log = time.time( );
			
			log_file.close( );
			
			# Reset flags and rotation parameters.

			go = 0;
			rotateZ = 0;
			bge.logic.robot_1_turn = 1;				
			bge.logic.robot_1_turn_by = .096;
			
			obj[ "traveling" ]				= "0";
			obj[ "stopped" ]  			 	= "1";
			obj[ "waypoint_coordinate" ]		= "";
			
			# Ask for the next way point.
			obj[ "next" ]      				= "1";
			
	# Rotating.
			
	elif ( bge.logic.robot_1_turn != 0 ): # Start turning to face the waypoint.
		
		# Convert way point string to a 3D vector.
	
		waypoint = mathutils.Vector( ( float( waypointString.split( "," )[ 0 ] ), float( waypointString.split( "," )[ 1 ] ), 1.0 ) );

		# Translate the way point to the robot's local space.
		
		mat_trans = mathutils.Matrix.Translation( ( -obj.worldPosition[ 0 ], -obj.worldPosition[ 1 ], -obj.worldPosition[ 2 ] ) );

		waypoint_trans = mat_trans * waypoint;

		waypoint_rot = mathutils.Matrix.Rotation( -orientation.to_euler( )[ 2 ], 4, 'Z') * waypoint_trans;
		
		# Now that the way point world coordinate is transformed to the robot's local space, 
		# compute the angle between the robot's  x-axis and the way point line going from the 
		# robot's origin to the way point.
		
		rotateZ = math.atan2( waypoint_rot[ 1 ], waypoint_rot[ 0 ] );

		#turn = 1 # Turn the robot.
		
		rotateZ = float( str( "%.4f" % rotateZ ) );

		if ( rotateZ < 0.0 ):

			bge.logic.robot_1_turn = -1; # If angle is negative, turn the other direction.
			
		if ( rotateZ > 0.0 ):
			
			bge.logic.robot_1_turn = 1;

		if ( abs( rotateZ ) <= .0035 ):

			bge.logic.robot_1_turn = 0; # At a certain point, stop turning and start moving forward.

		obj[ "rotate_to_face_waypoint"]          = rotateZ; # The angle the robot needs to turn to face the way point.
		obj[ "waypoint_coordinate_transformed" ] = str( waypoint_rot ); # The way points coordinates transformed to the robot's local space.
		obj[ "turn" ]     					 = str( bge.logic.robot_1_turn );
		obj[ "go" ]       					 = str( go );

		orientation = obj.worldOrientation;

		obj[ "robot_world_orientation" ] = str( orientation.to_euler( )[ 2 ] ); # Robot's world orientation.
		
		bge.logic.robot_1_turn_by = .096 * abs( rotateZ );		
		
		if ( bge.logic.robot_1_turn_by > .096 ):
			
			bge.logic.robot_1_turn_by = .096;
			
		#left_wheels = [ "robot_1_wheel_front_L", "robot_1_wheel_back_L" ]
	
		#right_wheels = [ "robot_1_wheel_front_R", "robot_1_wheel_back_R" ]
		
		# Either rotate right or left.
		
		#if ( bge.logic.robot_1_turn == 1 ):			

			#for wheel in right_wheels:
				
				#bge.logic.getCurrentScene( ).objects[ wheel ].applyRotation( [ 0, 0.02, 0 ], local )
				
			#for wheel in left_wheels:
				
				#bge.logic.getCurrentScene( ).objects[ wheel ].applyRotation( [ 0, -0.02, 0 ], local )
					
		#elif ( bge.logic.robot_1_turn == -1 ):
			
			#for wheel in right_wheels:
				
				#bge.logic.getCurrentScene( ).objects[ wheel ].applyRotation( [ 0, -0.02, 0 ], local )
				
			#for wheel in left_wheels:
				
				#bge.logic.getCurrentScene( ).objects[ wheel ].applyRotation( [ 0, 0.02, 0 ], local )
		
		obj.applyRotation( [ 0, 0, bge.logic.robot_1_turn * ( bge.logic.robot_1_turn_by ) ], local );