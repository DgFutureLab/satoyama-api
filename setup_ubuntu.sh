#!/bin/bash
if [ -z "$1" ]; then
	echo Please specify the path to the satoyama-api folder, for instance: sh satoyama-api/setup_ubuntu.sh satoyama-api/
fi 

if [ -d "$1" ]; then
	echo Using "$1"
	cd "$1"
	if [ -e wercker.yml ]; then
		echo Folder seems to be correct.
	else
		echo Folder has no wercer.yml file. Are you sure you are specifying the right path? Exitting...
		exit 1
		echo hun
	fi
else
        echo $1: Folder does not exist! Exitting..
	exit 1
fi
#sh installation/ubuntu_packages_setup.sh
#sh installation/ubuntu_db_setup.sh
#sh installation/ubuntu_env_setup.sh
