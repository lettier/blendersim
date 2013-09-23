'''

David Lettier
http://www.lettier.com/

Blendersim version 1.0.

This file populates the ../waypoint_logs files 1.log, 2.log, 3.log, and 4.log from some master log such as ../archive/PHYS_CS_Auction_A_1_3.log.

'''

import sys, os, math, subprocess;

def find_robots_in_log_with_respective_start_positions( log_file_name ):
	
	print "[WAYPOINT_LOG_POPULATOR.PY] Looking for robots in master log file: " + str( log_file_name );
	
	log_file = None;
	
	try:
	
		log_file = open( log_file_name, "r" );
		
	except Exception:
		
		print "[WAYPOINT_LOG_POPULATOR.PY] Cannot find master log file: " + str( log_file );
		
		return None;
		
	line = log_file.readline( );
	
	robots_added = 0;
	
	robot_locations_names = [ ];
	
	robot_names = [ ];
	
	while( line != "" ):
		
		if ( "WAYPOINTS" in line ):
			
			break;
			
		if ( "SENT" in line ):
			
			if ( "CAMPOSE" in line ):
				
				line_stripped_split = line.strip( ).split( " " );
				
				robot_location_name = [ line_stripped_split[ 6 ], line_stripped_split[ 7 ], line_stripped_split[ 12 ] ];
				
				if ( not ( robot_location_name in robot_locations_names ) ):
					
					if robots_added != 4:
						
						robot_locations_names.append( robot_location_name );
						
						robots_added = robots_added + 1;
						
					else:
						
						break;
				
		line = log_file.readline( );
		
	# Find robots closest to (100,100) starting position. This is robot 1 or 1.log.
	
	distances = [ ];
		
	for robot in xrange( 0, len( robot_locations_names ) ):
		
		distances.append( math.sqrt( math.pow( ( 100.0 - float( robot_locations_names[ robot ][ 0 ] ) ), 2 ) + math.pow( ( 100.0 - float( robot_locations_names[ robot ][ 1 ] ) ), 2 ) ) );
		
	robot_names.append( robot_locations_names[ distances.index( min( distances ) ) ][ 2 ] ); 
	
	# Find robots closest to (25,100) starting position. This is robot 2 or 2.log.
	
	distances = [ ];
		
	for robot in xrange( 0, len( robot_locations_names ) ):
		
		distances.append( math.sqrt( math.pow( ( 25.0 - float( robot_locations_names[ robot ][ 0 ] ) ), 2 ) + math.pow( ( 100.0 - float( robot_locations_names[ robot ][ 1 ] ) ), 2 ) ) );
		
	robot_names.append( robot_locations_names[ distances.index( min( distances ) ) ][ 2 ] ); 
		
	# Find robots closest to (25,25) starting position. This is robot 3 or 3.log.
	
	distances = [ ];
		
	for robot in xrange( 0, len( robot_locations_names ) ):
		
		distances.append( math.sqrt( math.pow( ( 25.0 - float( robot_locations_names[ robot ][ 0 ] ) ), 2 ) + math.pow( ( 25.0 - float( robot_locations_names[ robot ][ 1 ] ) ), 2 ) ) );
		
	robot_names.append( robot_locations_names[ distances.index( min( distances ) ) ][ 2 ] );
	
	# Find robots closest to (100,25) starting position. This is robot 4 or 4.log.
	
	distances = [ ];
		
	for robot in xrange( 0, len( robot_locations_names ) ):
		
		distances.append( math.sqrt( math.pow( ( 100.0 - float( robot_locations_names[ robot ][ 0 ] ) ), 2 ) + math.pow( ( 25.0 - float( robot_locations_names[ robot ][ 1 ] ) ), 2 ) ) );
		
	robot_names.append( robot_locations_names[ distances.index( min( distances ) ) ][ 2 ] );
	
	return robot_names;
		
if __name__ == "__main__":

	log_file_name = sys.argv[ 1 ];

	robots = find_robots_in_log_with_respective_start_positions( log_file_name );
	
	if ( robots == None ):
		
		sys.exit( 1 );	
	
	waypoint_log_files = [ "../waypoint_logs/1.log", "../waypoint_logs/2.log", "../waypoint_logs/3.log", "../waypoint_logs/4.log" ];
	
	# Remove the waypoint_logs files if they already exist.

	for log_file in xrange( 0, len( waypoint_log_files ) ):
	
		try:
			
			os.remove( waypoint_log_files[ log_file ] );
			
		except OSError:
			
			pass;
			
	for i in xrange( 0, len( waypoint_log_files ) ):
		
		print "[WAYPOINT_LOG_POPULATOR.PY] Writing out waypoint log file: " + str( waypoint_log_files[ i ] );
	
		log_file = None;
		
		try:
		
			log_file = open( log_file_name, "r" );
			
		except Exception:
			
			print "[WAYPOINT_LOG_POPULATOR.PY] Cannot find master log file: " + str( log_file );
			
			sys.exit( 1 );
			
		waypoint_log = open( waypoint_log_files[ i ], "w" );
			
		line = log_file.readline( );
		
		while( line != "" ):
			
			if ( "SENT" in line ):
			
				if ( "CAMPOSE" in line ):
					
					if ( robots[ i ] in line ):
						
						waypoint_log.write( line );
						
			elif ( "RECIEVED" in line or "RECEIVED" in line ): # Search for typo.
						
				if ( "WAYPOINTS" in line ):
					
					if ( robots[ i ] in line ):
						
						waypoint_log.write( line );
						
						
			line = log_file.readline( );
						
		waypoint_log.close( );
		
		log_file.close( );
					
	