# IoT Leader Election
This project is a leader election system between devices in an ad-hoc network. The leader becomes the device with the biggest ip address. When the leadership is established then the leader becomes a server that the followers can connect to and recieve commands.

# Setup

1. You need to have Debian or debian based operating system.
2. Install nmap (sudo apt install nmap).
3. All the files must be in the same folder.
4. If you are not running this project on an ad-hoc network then you can change the $myNum variable
from the start.sh file and set it as an integer of your choice.

# Execution

1. Give execute permissions to the start.sh script (chmod +x start.sh).
2. Execute the script from the same folder that the other 2 python scripts are.
3. Execute it for all the devices.
