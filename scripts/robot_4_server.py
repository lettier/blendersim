'''

David Lettier
http://www.lettier.com/

BlenderSim version 1.0.

This file serves waypoints from robot_*_client.py to the robot_*_controller.py script. 

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

	import socket, queue, threading, sys, socketserver # imports we need.
	
	# Flag for getting the first waypoint.
	
	bge.logic.robot_4_first_waypoint_received = False;
	
	# waypoint queue read from the robot_controller
	
	bge.logic.robot_4_waypoint_queue = queue.Queue( )
	
	class ThreadedRequestHandler( socketserver.BaseRequestHandler ):   

		def handle( self ):
			
			while True:
			
				# Echo the back to the client
				
				data = self.request.recv( 1024 ).decode( "utf-8" )
				data = data.strip( )
				
				print( "[ROBOT_4_SERVER.PY] Received: " + str( data ) )

				if ( data == "hello" ):

					self.request.send( bytes( "nicetomeetyou", "utf-8" ) )
					
					continue

				if ( data == "ready" ):

					self.request.send( bytes( "ready", "utf-8" ) )
					
					continue

				if ( "goto" in data.split( "," )[ 0 ] ):

					self.server.waypoint_q.put( str( data.split( "," )[ 1 ] + "," + data.split( "," )[ 2 ] ) )
					
					self.request.send( bytes( "next", "utf-8" ) )

					continue
				
				if ( data == "nomore" ):
					
					self.server.waypoint_q.put( "done" )
					
					self.request.send( bytes( "done", "utf-8" ) )
					
					continue
					
				if ( data == "" ):
					
					break
					
			return

	class ThreadedServer( socketserver.ThreadingMixIn, socketserver.TCPServer ):

		def __init__( self, server_address, RequestHandlerClass, waypoint_q, bge_obj ):

			self.allow_reuse_address = True
			
			socketserver.TCPServer.__init__( self, server_address, RequestHandlerClass )		

			self.waypoint_q = waypoint_q
			
			self.bge_obj = bge_obj
			
	address = ( '', 5004 );
	bge.logic.robot_4_server = ThreadedServer( address, ThreadedRequestHandler, bge.logic.robot_4_waypoint_queue, obj );
	ip, port = bge.logic.robot_4_server.server_address; # find out what port we were given

	t = threading.Thread( target = bge.logic.robot_4_server.serve_forever );
	t.setDaemon( True ); # don't hang on exit
	t.start( );
	
# Queue.get blocks normally. Here we want it not to block as the server waits for a connection and the first waypoint from the
# client.
	
if ( bge.logic.robot_4_first_waypoint_received == False ):
	
	import queue
	
	try:
	
		waypoint_coordinate = bge.logic.robot_4_waypoint_queue.get( False );
		bge.logic.getCurrentScene( ).objects[ "robot_4_base" ][ "waypoint_coordinate" ] = waypoint_coordinate;
		bge.logic.robot_4_first_waypoint_received = True;
	
	except queue.Empty:
		
		print( "[ROBOT_4_SERVER.PY] Waiting for the first waypoint." );
	
# Is the robot done with the current way point and is waiting for the next one?

if ( bge.logic.getCurrentScene( ).objects[ "robot_4_base" ][ "next" ] == "1" ):
	
	bge.logic.getCurrentScene( ).objects[ "robot_4_base" ][ "next" ] = "0"; # No longer waiting for next wait point.
	
	if ( bge.logic.getCurrentScene( ).objects[ "robot_4_base" ][ "traveling" ] == "0" and bge.logic.getCurrentScene( ).objects[ "robot_4_base" ][ "stopped" ] == "1"  ):
			
		waypoint_coordinate = bge.logic.robot_4_waypoint_queue.get( );
		
		if ( waypoint_coordinate == "done" ):
			
			bge.logic.robot_4_waypoint_queue.put( "done" );
			
			bge.logic.getCurrentScene( ).objects[ "robot_4_base" ][ "waypoint_coordinate" ] = "";
		
		elif ( waypoint_coordinate != ""  ):
		
			bge.logic.getCurrentScene( ).objects[ "robot_4_base" ][ "waypoint_coordinate" ] = waypoint_coordinate;		
			
			waypoint = bge.logic.getCurrentScene( ).addObject( "waypoint_marker", obj );
			
			waypoint.worldPosition.x = int( waypoint_coordinate.split( "," )[ 0 ] );
			
			waypoint.worldPosition.y = int( waypoint_coordinate.split( "," )[ 1 ] );
		
			waypoint.worldPosition.z = bge.logic.getCurrentScene( ).objects[ "robot_4_base" ].worldPosition.z + 3;		
			
if ( obj[ "game_quit" ] == 1 ):
	
	bge.logic.robot_4_server.shutdown( );
					
	bge.logic.endGame( );
	
obj[ "inc" ] += 1