#!/bin/bash
apifolder="$1"
envname="$2"
DEFAULT="$3"
ATTENTION="$4"
SUCCESS="$5"
ERROR="$6"


if [ -d "~/$envname" ]; then
	# if [ -e "~/$envname/"]
	
	virtualenv -q "$HOME/$envname"
	echo "${SUCCESS} Created new Python environment in $HOME/$envname ${DEFAULT}"
fi

if [ -e "$HOME/$envname/bin/activate" ]; then
	. "$HOME/$envname/bin/activate"
	echo "${SUCCESS} Now using Python interpreter: `which python` ${DEFAULT}"
else
	echo "${ERROR} Something went wrong. ${DEFAULT} Could not find activate script for new environment. Exitting... ${DEFAULT}"
	exit 1
fi


if [ -e "$apifolder/requirements.txt" ]; then
	echo "${ATTENTION} Installing Python modules. This may take a while."
	pip install -q -r "$apifolder/requirements.txt"
	echo "${SUCCESS} Installed Python modules in $HOME/$envname/lib/python2.7/site-packages/ ${DEFAULT}"
else
	echo "${ERROR} Could not find requirements.txt. Exitting..."
	exit 1
fi

if [ -e "$apifolder/db_config_sample.yml" ]; then
	if [ -e "$apifolder/db_config.yml" ]; then
		echo "${SUCCESS} Found existing db_config.yaml. ${DEFAULT}"
	else
		
		cp "$apifolder/db_config_sample.yml" "$apifolder/db_config.yml"
		echo "${DEFAULT} Copied db_config_sample.yml to db_config.yml"
		echo "${ATTENTION} You can edit db_config.yml with your own settings if you do not like the default settings. ${DEFAULT}"
	fi
else
	echo "${ERROR} Could not find db_config_sample.yml. Exitting... ${DEFAULT}"
	exit 1
fi


if [ -e "$apifolder/manage.py" ]; then
	cd "$apifolder"
	python manage.py db upgrade
	echo "${SUCCESS} Database migration complete! ${DEFAULT}"
else
	echo "${ERROR} Could not find manage.py. Cannot migrate database. Exitting... ${DEFAULT}"
	exit 1
fi


#python satoyama-api/manage.py db upgrade