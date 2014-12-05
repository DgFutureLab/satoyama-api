#!/bin/bash
apifolder="$1"
envname="$2"
echo "Creating new Python environment named $envname"

virtualenv "~/$envname"
if [ -e "~/$envname/bin/activate" ]; then
	. "~/$envname/bin/activate"
	echo "Environment changed successfully! Now using Python interpreter: `which python`"
else
	echo "\n\n\n Something went wrong. Could not find activate script for new environment. Exitting..."
	exit 1
fi



if [ -e "$apifolder/requirements.txt" ]; then
	echo "Installing Python modules in new environment..."
	pip install -r "$apifolder/requirements.txt"
else
	echo "\nCould not find requirements.txt. Exitting..."
	exit 1
fi

if [ -e "$apifolder/db_config_sample.yml" ]; then
	echo "\n Copying db_config_sample.yml to db_config.yml"
	echo "****** ATTENTION! You can db_config.yml with your own settings, but it is not necessarry."
	cp "$apifolder/db_config_sample.yml" "$apifolder/db_config.yml"
else
	echo "Could not find db_config_sample.yml. Exitting..."
	exit 1
fi


#python satoyama-api/manage.py db upgrade