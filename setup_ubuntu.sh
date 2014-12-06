#!/bin/bash

### Define paths
envname="satoyama-env"
apifolder=`dirname $0`
logfile="$HOME/satoyama-install.log"
### Define colors
DEFAULT=`tput sgr0`
ATTENTION=`tput setaf 3`
SUCCESS=`tput setaf 2`
ERROR=`tput setaf 1`

# if [ -z "$apifolder" ]; then
# 	echo "${ERROR} Please specify the path to the satoyama-api folder, for instance: sh satoyama-api/setup_ubuntu.sh satoyama-api/ ${DEFAULT}"
# fi 

if [ -d "$apifolder" ]; then
	if [ -e "$apifolder/wercker.yml" ]; then
		echo "${SUCCESS}Verified folder $apifolder ${DEFAULT}"
	else
		echo "${ERROR}Folder has no wercer.yml file. Are you sure you are specifying the right path? Exitting... ${DEFAULT}"
		exit 1
	fi
else
        echo "${ERROR}$apifolder: Folder does not exist! Exitting.. ${DEFAULT}"
	exit 1
fi

sh "$apifolder/installation/ubuntu_packages_setup.sh" "$apifolder" "$envname" "$DEFAULT" "$ATTENTION" "$SUCCESS" "$ERROR" "$logfile"
sh "$apifolder/installation/ubuntu_db_setup.sh" "$apifolder" "$envname" "$DEFAULT" "$ATTENTION" "$SUCCESS" "$ERROR" "$logfile"
sh "$apifolder/installation/ubuntu_env_setup.sh" "$apifolder" "$envname" "$DEFAULT" "$ATTENTION" "$SUCCESS" "$ERROR" "$logfile"
