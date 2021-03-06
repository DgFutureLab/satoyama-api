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

# if [ -d "$apifolder" ]; then
# 	if [ -e "$apifolder/wercker.yml" ]; then
# 		echo "${SUCCESS}Verified folder $apifolder ${DEFAULT}"
# 	else
# 		echo "${ERROR}Folder has no wercer.yml file. Are you sure you are specifying the right path? Exitting... ${DEFAULT}"
# 		exit 1
# 	fi
# else
#         echo "${ERROR}$apifolder: Folder does not exist! Exitting.. ${DEFAULT}"
# 	exit 1
# fi

sh "$apifolder/installation/ubuntu_packages_setup.sh" "$apifolder" "$envname" "$DEFAULT" "$ATTENTION" "$SUCCESS" "$ERROR" "$logfile"
if [ $? -eq 1 ]; then
	echo "Failed to install required packages..."
	exit 1
fi

sh "$apifolder/installation/ubuntu_db_setup.sh" "$apifolder" "$envname" "$DEFAULT" "$ATTENTION" "$SUCCESS" "$ERROR" "$logfile"
if [ $? -eq 1 ]; then
	echo "Failed to setup database..."
	exit 1
fi

sh "$apifolder/installation/ubuntu_env_setup.sh" "$apifolder" "$envname" "$DEFAULT" "$ATTENTION" "$SUCCESS" "$ERROR" "$logfile"
if [ $? -eq 1 ]; then
	echo "Failed to setup python environment..."
	exit 1
fi

echo " ____   __   ____   __   _  _   __   _  _   __          __   ____   __  
/ ___) / _\ (_  _) /  \ ( \/ ) / _\ ( \/ ) / _\  ___   / _\ (  _ \ (  ) 
\___ \/    \  )(  (  O ) )  / /    \/ \/ \/    \(___) /    \ ) __/  )(  
(____/\_/\_/ (__)  \__/ (__/  \_/\_/\_)(_/\_/\_/      \_/\_/(__)   (__) 
"

echo "${SUCCESS}Installation complete! All output generated was stored in $logfile${DEFAULT}"