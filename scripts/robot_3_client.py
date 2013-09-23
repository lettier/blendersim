'''

David Lettier
http://www.lettier.com/

BlenderSim version 1.0.

This file makes a connection with robot_*_server.py, handshakes, and then feeds robot_*_server.py the waypoints as read from ../waypoint_logs/*.log.

'''

# imports

import asyncore, socket, sys, log_reader

# Client class. This uses asyncore to do non-blocking I/O with the server.

class Client( asyncore.dispatcher ):
	
	# Constructor. Takes a host, port, and beginning message.

	def __init__( self, host, port, message ):
		
		# Call asyncore's constructor.
		
		asyncore.dispatcher.__init__( self )
		
		# Create the socket.
		
		self.create_socket( socket.AF_INET, socket.SOCK_STREAM )
		self.connect( ( host, port ) )
		
		# The buffer that will be sent to the server.
		
		self.out_buffer = message
		
		# Flags.
		
		self.ready = 0
		self._readable = 0
		self._writable = 1
		
		# The messages to send to the server.
		
		#self.messages = [ "goto,9,6", "goto,-9,6", "goto,9,-6", "goto,-9,-6" ];
		
		try:
		
			log_file = "../waypoint_logs/3.log";
		
		except:
			
			print( "[ROBOT_3_CLIENT.PY] no log file specified." )
			
			sys.exit( )
			
		print( "[ROBOT_3_CLIENT.PY] using " + log_file + " log file." )
		
		self.log_reader = log_reader.Log_Reader( log_file )
		
		waypoints_temp = self.log_reader.return_all_waypoints( )
		
		print( "[ROBOT_3_CLIENT.PY] sending these waypoints (" + str( len( waypoints_temp ) ) + " in total):" )
		
		for x in waypoints_temp:
			
			print( x[ 1 ] );
		
	# Tell asyncore what to do when the connection closes.

	def handle_close( self ):
		
		print '[ROBOT_3_CLIENT.PY] Closing connection.'
		
		self.close( );
		
		print '[ROBOT_3_CLIENT.PY] Exiting system.'
		
		sys.exit( );
		
	# Tell asyncore what to do when the socket is ready to be read from.

	def handle_read( self ):
		
		message = self.recv( 1024 ).decode( "utf-8" )
		message = message.strip( );
		print '[ROBOT_3_CLIENT.PY] Received string:', message
		
		# Begin handshake.
		
		if ( message == "nicetomeetyou" ):

			self.out_buffer = "ready"
			self._readable = 0
			self._writable = 1
		
		if ( message == "ready" ):

			self.out_buffer = ""
			self._readable = 0
			self._writable = 1
			self.ready = 1
			
		# End handshake.
			
		if ( message == "next" ): # Server is asking for another way point.

			self.out_buffer = ""
			self._readable = 0
			self._writable = 1
			self.ready = 1
			
		if ( message == "done" ): # Server says the robot is done going to all way points.

			self.out_buffer = ""
			self._readable = 0
			self._writable = 0
			self.ready = 0
			
			print '[ROBOT_3_CLIENT.PY] Shutting down.'
			
			self.handle_close( );
		
		if ( self.ready ):
		
			if ( self.log_reader.return_number_of_waypoints_left( ) == 0 ): # Tell the server there are no more way points.
				
				self.out_buffer = "nomore";
				self._writable = 1;
				self._readable = 0;
				self.ready = 0;
				
			else: # Send the next way point message.
				
				next_waypoint = self.log_reader.return_next_waypoint( )
				
				self.out_buffer = "goto," + str( next_waypoint[ 0 ] ) + "," + str( next_waypoint[ 1 ] );	
				self.ready = 0;
			
		print "[ROBOT_3_CLIENT.PY] Out Buffer contents: ", self.out_buffer;
		print "[ROBOT_3_CLIENT.PY] Out buffer size: ", len( self.out_buffer );

	# Tell asyncore what to do when the socket is ready to be written to.

	def handle_write( self ):
		
		print "[ROBOT_3_CLIENT.PY] Sending string: ", self.out_buffer;
		sent = self.send( self.out_buffer );
		print "[ROBOT_3_CLIENT.PY] Sent: ", sent;
		
		self.out_buffer = self.out_buffer[ sent : ];
		
		if ( len( self.out_buffer ) != 0 ):			
			
			self._writable = 1;
			self._readable = 0;
		
		else:
			self._readable = 1;
			self._writable = 0;
			
		print "[ROBOT_3_CLIENT.PY] Out Buffer contents: ", self.out_buffer;
		print "[ROBOT_3_CLIENT.PY] Out buffer size: ", len( self.out_buffer );
		
	# Defines to asyncore when this channel is writable.
			
	def writable( self ):
		
		print "[ROBOT_3_CLIENT.PY] Writable? ", ( len( self.out_buffer ) > 0 and self._writable == 1 );
		return ( len( self.out_buffer ) > 1 and self._writable == 1 );
	
	# Defines to asyncore when this channel is readable.
	
	def readable( self ):
		
		print "[ROBOT_3_CLIENT.PY] Readable?", ( len( self.out_buffer ) == 0 and self._readable == 1 );
		return ( len( self.out_buffer ) == 0 and self._readable == 1 );

if __name__ == "__main__":

	client = Client( '', 5003, "hello" ) # Create the client.
	asyncore.loop() # Poll, send, receive, close.