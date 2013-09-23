'''

David Lettier
http://www.lettier.com/

BlenderSim version 1.0.

This script runs all robot clients in four subprocesses.

'''

import subprocess;

if __name__ == '__main__':

	subprocess.call( ["python", "robot_1_client.py" ] );
	subprocess.call( ["python", "robot_2_client.py" ] );
	subprocess.call( ["python", "robot_3_client.py" ] );
	subprocess.call( ["python", "robot_4_client.py" ] );