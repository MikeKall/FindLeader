#!/bin/bash

# This is the initialiazation script that let's each device discover
# and elect a leader among them.

printf "\n== Sequence started ==\n\n"
printf "My ip address: "
hostname -I

myIP="$( hostname -I )"

# Deconstruct the IP address with delimiter '.'
IFS='.' read -ra x <<< "$myIP"

myNum=${x[3]}
#myNum=0 
# This list holds the nmap results
scan=()

# This list holds all the raspberry pi devices
devices=()
counter=0

printf "\nSearching the network for other devices:\n"
while IFS= read -r line; do
	scan+=( "$line" )
	# echo "${scan[$counter]}"
	if [[ ${scan[$counter]} == *"${x[0]}.${x[1]}.${x[2]}"* ]]; then
		printf "\nFound ${scan[$counter]}"
		devices+=( ".${scan[$counter]}" )
	fi

	counter=$(( $counter + 1 ))

done < <( nmap -n -sn ${x[0]}.${x[1]}.${x[2]}.0/24 -oG - | awk '/Up$/{print $2}' )

if [[ $counter == 1 ]]; then
	printf "\nThere is no other device on the network"
	echo "none" > leaderIP
else


	counter=0
	numberOfDevices=0
	maxNum=0

	# If this device becomes a follower then the flag turns false
	flag=true

	printf "\n\n====================="
	printf "\n\nSearching for leader:\n\n"

	# Seperate the IPs with . as delimiter
	IFS='.' read -ra IP <<< "${devices[@]}"

	# Delete all spaces
	delete=( )
	IP=( ${IP[@]/$delete} )
	# =====================

	# Loop through the numbers to find the 4th one of each IP
	for i in "${IP[@]}"; do

		# echo "Counter: $counter Division: $(($counter % 3 )) Line: $i"
		# Dividing by 3 in order to check the last digit in the ip address
		if ! [[ $counter == 0 ]]; then # 0 mod 3 = 0, we don't want that
			if [[ $(( $counter % 3 )) == 0 ]]; then

				if [[ $myNum -lt $i ]]; then
					flag=false
				fi
				if [[ $maxNum -lt $i ]]; then
					maxNum=$i
				fi
				numberOfDevices=$(( $numberOfDevices + 1 ))
				counter=0
			else
				counter=$(( $counter + 1 ))
			fi
		else
			counter=$(( $counter + 1 ))
		fi

	done

	if $flag; then
		printf "\n>I am the leader"
		printf "\n$(( $numberOfDevices - 1 )) follower(s)\n\n"
		python3 leader.py
	else
		printf "Leader is ${x[0]}.${x[1]}.${x[2]}.$maxNum\n"
		echo "${x[0]}.${x[1]}.${x[2]}.$maxNum" > leaderIP
		printf "\n>I am following\n"
		python3 follower.py
	fi
fi
