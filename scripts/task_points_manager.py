'''
David Lettier
http://www.lettier.com/

Blender task points manager.

This file draws the task points as found in ../task_points_configurations for [a], [b], [c], [d], and [e] 
key presses.

'''

# Get the controller in Blender that is attached to this script.
controller = bge.logic.getCurrentController( );
# get the game object that the controller is attached to.
obj = controller.owner;

# Blender calls this script each game loop so we cannot initialize each game loop.
# Thus get the "init" property of the controller and set it to zero that this portion of code
# only gets called once.

if ( obj[ "init" ] == 1 ):

	obj[ "init" ] = 0 # Don't run this again.
	
	bge.logic.task_points_added = [ ];
	
	bge.logic.task_points_configurations = [ [ ], [ ], [ ], [ ], [ ] ];
	
	a_file = open( "./task_points_configurations/a.conf", "r" );
	
	b_file = open( "./task_points_configurations/b.conf", "r" );
	
	c_file = open( "./task_points_configurations/c.conf", "r" );
	
	d_file = open( "./task_points_configurations/d.conf", "r" );
	
	e_file = open( "./task_points_configurations/e.conf", "r" );
	
	file_objects = [ a_file, b_file, c_file, d_file, e_file ];
	
	for x in range( 0, len( file_objects ) ):
		
		line = file_objects[ x ].readline( );
		
		while ( line != "" ):
			
			line_stripped_splitted = line.strip( ).split( " " );
			
			temp = [ ];
			
			for i in line_stripped_splitted:
				
				if ( i != '' ):
					
					temp.append( i );
					
			xy_point = temp;
			
			bge.logic.task_points_configurations[ x ].append( xy_point );
			
			line = file_objects[ x ].readline( );
			
	# Scrub out any empties.
			
	for x in range( 0, len( bge.logic.task_points_configurations ) ):
	
		bge.logic.task_points_configurations[ x ] = [ y for y in bge.logic.task_points_configurations[ x ] if y ];

keyboard = bge.logic.keyboard;
activated = bge.logic.KX_INPUT_JUST_ACTIVATED;

if keyboard.events[bge.events.AKEY] == activated:
	
	if ( len( bge.logic.task_points_added ) > 0 ):
		
		for x in range( 0, len( bge.logic.task_points_added ) ):
			
			bge.logic.task_points_added[ x ].endObject( );
			
		bge.logic.task_points_added = [ ];
	
	for x in range( 0, len( bge.logic.task_points_configurations[ 0 ] ) ):
		
		task_point = bge.logic.getCurrentScene( ).addObject( "task_point_marker", obj );
		
		task_point.worldPosition.x = float( bge.logic.task_points_configurations[ 0 ][ x ][ 0 ] );
			
		task_point.worldPosition.y = float( bge.logic.task_points_configurations[ 0 ][ x ][ 1 ] );
		
		task_point.worldPosition.z = bge.logic.getCurrentScene( ).objects[ "robot_1_base" ].worldPosition.z + 3;
		
		bge.logic.task_points_added.append( task_point );
	
elif keyboard.events[bge.events.BKEY] == activated:
	
	if ( len( bge.logic.task_points_added ) > 0 ):
		
		for x in range( 0, len( bge.logic.task_points_added ) ):
			
			bge.logic.task_points_added[ x ].endObject( );
			
		bge.logic.task_points_added = [ ];
			
	for x in range( 0, len( bge.logic.task_points_configurations[ 1 ] ) ):
		
		task_point = bge.logic.getCurrentScene( ).addObject( "task_point_marker", obj );
		
		task_point.worldPosition.x = float( bge.logic.task_points_configurations[ 1 ][ x ][ 0 ] );
			
		task_point.worldPosition.y = float( bge.logic.task_points_configurations[ 1 ][ x ][ 1 ] );
		
		task_point.worldPosition.z = bge.logic.getCurrentScene( ).objects[ "robot_1_base" ].worldPosition.z + 3;
		
		bge.logic.task_points_added.append( task_point );
	
elif keyboard.events[bge.events.CKEY] == activated:
	
	if ( len( bge.logic.task_points_added ) > 0 ):
		
		for x in range( 0, len( bge.logic.task_points_added ) ):
			
			bge.logic.task_points_added[ x ].endObject( );
			
		bge.logic.task_points_added = [ ];
			
	for x in range( 0, len( bge.logic.task_points_configurations[ 2 ] ) ):
		
		task_point = bge.logic.getCurrentScene( ).addObject( "task_point_marker", obj );
		
		task_point.worldPosition.x = float( bge.logic.task_points_configurations[ 2 ][ x ][ 0 ] );
			
		task_point.worldPosition.y = float( bge.logic.task_points_configurations[ 2 ][ x ][ 1 ] );
		
		task_point.worldPosition.z = bge.logic.getCurrentScene( ).objects[ "robot_1_base" ].worldPosition.z + 3;
		
		bge.logic.task_points_added.append( task_point );
	
elif keyboard.events[bge.events.DKEY] == activated:
	
	if ( len( bge.logic.task_points_added ) > 0 ):
		
		for x in range( 0, len( bge.logic.task_points_added ) ):
			
			bge.logic.task_points_added[ x ].endObject( );
			
		bge.logic.task_points_added = [ ];
			
	for x in range( 0, len( bge.logic.task_points_configurations[ 3 ] ) ):
		
		task_point = bge.logic.getCurrentScene( ).addObject( "task_point_marker", obj );
		
		task_point.worldPosition.x = float( bge.logic.task_points_configurations[ 3 ][ x ][ 0 ] );
			
		task_point.worldPosition.y = float( bge.logic.task_points_configurations[ 3 ][ x ][ 1 ] );
		
		task_point.worldPosition.z = bge.logic.getCurrentScene( ).objects[ "robot_1_base" ].worldPosition.z + 3;
		
		bge.logic.task_points_added.append( task_point );
	
elif keyboard.events[bge.events.EKEY] == activated:
	
	if ( len( bge.logic.task_points_added ) > 0 ):
		
		for x in range( 0, len( bge.logic.task_points_added ) ):
			
			bge.logic.task_points_added[ x ].endObject( );
			
		bge.logic.task_points_added = [ ];
			
	for x in range( 0, len( bge.logic.task_points_configurations[ 4 ] ) ):
		
		task_point = bge.logic.getCurrentScene( ).addObject( "task_point_marker", obj );
		
		task_point.worldPosition.x = float( bge.logic.task_points_configurations[ 4 ][ x ][ 0 ] );
			
		task_point.worldPosition.y = float( bge.logic.task_points_configurations[ 4 ][ x ][ 1 ] );
		
		task_point.worldPosition.z = bge.logic.getCurrentScene( ).objects[ "robot_1_base" ].worldPosition.z + 3;
		
		bge.logic.task_points_added.append( task_point );