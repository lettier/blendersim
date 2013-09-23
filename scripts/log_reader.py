'''

David Lettier
http://www.lettier.com/

This file reads a log file with at most one robot.

Use this class to read a log file and capture the CAMPOSEs and WAYPOINTs.

'''

class Log_Reader:
	
	__log_file = None;
	
	__camposes = [ ];
	__waypoints = [ ];
	__last_used_camposes_index = 0;
	__last_used_waypoints_index = 0;
	
	__log_file_time_delta = 0.0;
	__time_then = 0.0;
	
	def __init__( self, file_name ):
		
		# Open up file.
		
		__log_file = open( file_name, "r", 1 )
		
		# Return if file doesn't exist.
		
		if ( __log_file == None ):
			
			print( "[ERROR] file does not exist." );
			
			return None;
		
		# Read line by line.
		
		line = __log_file.readline( )
		
		while ( line != "" ):
			
			# Store campose lines as list of tuples ( time( h:m:s, seconds_total, seconds_running ),(x,y,orientation),robot_id(name,number) ).
			
			if "CAMPOSE" in line:
				
				line_splitted = line.split( " " )
				
				time = line_splitted[ 0 ]
				
				time = time.split( ":" )
				
				hours_to_seconds = int( time[ 0 ] ) * 3600;
				
				minutes_to_seconds = int( time[ 1 ] ) * 60;
				
				total_seconds = hours_to_seconds + minutes_to_seconds + float( time[ 2 ] + "." + time[ 3 ] + time[ 4 ] )
				
				time = time[ 0 ] + ":" + time[ 1 ] + ":" + time[ 2 ] + "." + time[ 3 ] + time[ 4 ]
				
				seconds_running = 0.0
				
				x = int( line_splitted[ 6 ] )
				
				y = int( line_splitted[ 7 ] )
				
				o = float( line_splitted[ 8 ] )
				
				robot_id = ( line_splitted[ 12 ], int( line_splitted[ 13 ].strip() ) );
				
				self.__camposes.append( ( [ time, total_seconds, seconds_running ], ( x, y, o ), robot_id ) );
				
				# Check for different robots in the log file.
				
				try:

					if ( robot_id[ 1 ] != self.__camposes[ -2 ][ 2 ][ 1 ] ):
						
						print( "[ERROR] can only handle logs with one robot." )
						
						return None;
					
				except:
					
					pass	
				
			elif ( "WAYPOINTS" in line ):
				
				# Store waypoint strings as list of tuples ( time( h:m:s, seconds_total, [(x,y),(x1,y1),...,(xn,yn)], robot_id( name, number ) )

				line_splitted = line.split( " " );
					
				time = line_splitted[ 0 ]
				
				time = time.split( ":" )
				
				hours_to_seconds = int( time[ 0 ] ) * 3600;
				
				minutes_to_seconds = int( time[ 1 ] ) * 60;
				
				total_seconds = hours_to_seconds + minutes_to_seconds + float( time[ 2 ] + "." + time[ 3 ] + time[ 4 ] )
				
				time = time[ 0 ] + ":" + time[ 1 ] + ":" + time[ 2 ] + "." + time[ 3 ] + time[ 4 ]
				
				seconds_running = 0.0
				
				number_of_waypoints = int( line_splitted[ 6 ] )
				
				count = number_of_waypoints * 2
				
				waypoints_temp = None
				
				if ( int( line_splitted[ 7 ] ) != 0 and int( line_splitted[ 8 ] ) != 0 ):
				
					waypoints_temp = ( int( line_splitted[ 7 ] ), int( line_splitted[ 8 ] ) )
					
				elif ( int( line_splitted[ 7 ] ) == 0 and int( line_splitted[ 8 ] ) == 0 ):
					
					line = __log_file.readline( )
					
					continue;
				
				''' LEGACY
								
				for iterator in range( 7, 7 + count, 2 ):
					
					waypoints_temp.append( ( int( line_splitted[ iterator ] ), int( line_splitted[ iterator + 1 ] ) ) )					
				
				robot_id = ( line_splitted[ 7 + count + 3 ], int( line_splitted[ 7 + count + 4 ].strip() ) );
				
				previous_waypoints = [ ];
				
				try:
					
					previous_waypoints = self.__waypoints[ -1 ][ 1 ];
					
				except:
					
					pass;
					
				# Don't add waypoint strings that are in series.
				
				same = 0;
				
				try:
				
					i = 0
				
					for e in range( len( previous_waypoints ) - len( waypoints_temp ), len( previous_waypoints ) ):
						
						if ( previous_waypoints[ e ] == waypoints_temp[ i ] ):
							
							same = same + 1;
							
						i = i + 1
							
				except:
					
					pass;
						
				if ( same != len( waypoints_temp ) ):
				
				'''
				
				self.__waypoints.append( ( [ time, total_seconds, seconds_running ], waypoints_temp, robot_id ) );						
			
			line = __log_file.readline( )		
		
		# Calculate time delta (total time that passed) in the log file.
				
		self.__time_delta = self.__camposes[ -1 ][ 0 ][ 1 ] - self.__camposes[ 0 ][ 0 ][ 1 ];
		
		time_delta_temp = self.__waypoints[ -1 ][ 0 ][ 1 ] - self.__waypoints[ 0 ][ 0 ][ 1 ];
				
		if ( time_delta_temp > self.__time_delta ):
			
			self.__time_delta = time_delta_temp;
		
		# Calculate running time per CAMPOSE and WAYPOINT line in log file.
		
		for x in range( 0, len( self.__camposes ) ):
			
			self.__camposes[ x ][ 0 ][ 2 ] = self.__camposes[ x ][ 0 ][ 1 ] - self.__camposes[ 0 ][ 0 ][ 1 ];
			
		for x in range( 0, len( self.__waypoints ) ):
			
			self.__waypoints[ x ][ 0 ][ 2 ] = self.__waypoints[ x ][ 0 ][ 1 ] - self.__waypoints[ 0 ][ 0 ][ 1 ];
	
		# Init __time_then.
		
		import time
		
		self.__time_then = time.time( );
	
	def return_next_campose( self ):
		
		self.__last_used_camposes_index = self.__last_used_camposes_index + 1;
		
		try:
		
			return self.__camposes[ self.__last_used_camposes_index - 1 ][ 1 ]
		
		except:
			
			return None
		
		'''
		
		# Calculate time delta since last call using __time_then.
		
		import time
		
		current_time_delta = time.time( ) - self.__time_then
		
		for x in range( self.__last_used_camposes_index, len( self.__camposes ) ):
			
			if ( self.__camposes[ x ][ 0 ][ 2 ] < current_time_delta ):
				
				pass;
			
			elif ( self.__camposes[ x ][ 0 ][ 2 ] == current_time_delta ):
				
				self.__last_used_camposes_index = x;
				
				break;
				
			elif ( self.__camposes[ x ][ 0 ][ 2 ] > current_time_delta ):
				
				self.__last_used_camposes_index = x - 1;
				
				break;
				
		return self.__camposes[ self.__last_used_camposes_index ][ 1 ]
		
		'''
	
	def return_number_of_waypoints_left( self ):
		
		#sum = 0;
		
		#for x in range( self.__last_used_waypoints_index, len( self.__waypoints ) ):
			
			#sum = sum + len( self.__waypoints[ x ][ 1 ] )
			
		return len( self.__waypoints ) - self.__last_used_waypoints_index;
	
	def return_next_waypoint( self ):
		
		self.__last_used_waypoints_index = self.__last_used_waypoints_index + 1;
		
		try:
		
			return self.__waypoints[ self.__last_used_waypoints_index - 1 ][ 1 ]
		
		except:
			
			return None
		
		'''

		# Calculate time delta since last call using __time_then.
		
		import time
		
		current_time_delta = time.time( ) - self.__time_then
		
		for x in range( self.__last_used_waypoints_index, len( self.__waypoints ) ):
			
			if ( self.__waypoints[ x ][ 0 ][ 2 ] < current_time_delta ):
				
				pass;
			
			elif ( self.__waypoints[ x ][ 0 ][ 2 ] == current_time_delta ):
				
				self.__last_used_waypoints_index = x;
				
				break;
				
			elif ( self.__waypoints[ x ][ 0 ][ 2 ] > current_time_delta ):
				
				self.__last_used_waypoints_index = x - 1;
				
				break;
				
		try:
				
			return self.__waypoints[ self.__last_used_waypoints_index ][ 1 ].pop( 0 )
		
		except:
			
			return None
	
		# Based on time passed since last call, pass the next waypoint.
		
		# Waypoints change over time and some get added over time.
		
		# Search the list of waypoint tuples finding the tuple that has a time less than the current time pass since last call
		# and the tuple that has a time greater than the current time. Use the tuple with the greatest less than current 
		# time as the current tuple to read waypoints from.
		
		# Example:
		# ct9.5
		# 0 - t0
		# 1 - t4
		# 2 - t7
		# 3 - t10		
		# Use tuple # 2.
		
		'''
		
	def return_all_camposes( self ):
		
		return self.__camposes;
	
	def return_all_waypoints( self ):
		
		return self.__waypoints;
	
if __name__ == "__main__":
	
	log_reader = Log_Reader( "wayPoint.log" );
	
	y = log_reader.return_all_camposes( )
	
	for x in range( 0, len( y ) ):
		
		print log_reader.return_next_campose( )