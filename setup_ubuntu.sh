#!/bin/bash

envname="satoyama-env"

apifolder="$1"
# startloc=`pwd`
if [ -z "$apifolder" ]; then
	echo Please specify the path to the satoyama-api folder, for instance: sh satoyama-api/setup_ubuntu.sh satoyama-api/
fi 

if [ -d "$apifolder" ]; then
	echo Using "$apifolder"
	if [ -e "$apifolder/wercker.yml" ]; then
		echo Folder seems to be correct.
	else
		echo Folder has no wercer.yml file. Are you sure you are specifying the right path? Exitting...
		exit 1
	fi
else
        echo $apifolder: Folder does not exist! Exitting..
	exit 1
fi

#sh installation/ubuntu_packages_setup.sh
#sh installation/ubuntu_db_setup.sh
sh "$apifolder/installation/ubuntu_env_setup.sh" "$apifolder" "$envname"
