#!/bin/bash
apifolder="$1"
envname="$2"
DEFAULT="$3"
ATTENTION="$4"
SUCCESS="$5"
ERROR="$6"


if [ -d "$HOME/$envname" ]; then
	# if [ -e "~/$envname/"]
	echo "${ATTENTION}Found existing Python environment in $HOME/$envname ${DEFAULT}"
else
	sudo virtualenv "$HOME/$envname"  >> "$HOME/log.txt"
	if [ $? -eq 0 ]; then
		echo "${SUCCESS}Created new Python environment in $HOME/$envname ${DEFAULT}"
	else
		echo "${ERROR}Could not create new Python environment. Exitting... ${DEFAULT}"
		exit 1
	fi
fi

if [ -e "$HOME/$envname/bin/activate" ]; then
	. "$HOME/$envname/bin/activate" >> "$HOME/log.txt"
	if [ $? -eq 0 ]; then
		echo "${SUCCESS}Now using Python interpreter: `which python` ${DEFAULT}"
	else
		echo "${ERROR}Could not activate new Python environment. Exitting... ${DEFAULT}"
		exit 1
	fi
else
	echo "${ERROR}Something went wrong. ${DEFAULT} Could not find activate script for new environment. Exitting... ${DEFAULT}"
	exit 1
fi


if [ -e "$apifolder/requirements.txt" ]; then
	echo "${ATTENTION}Installing Python modules. This may take a while... ${DEFAULT}"
	pip install -r "$apifolder/requirements.txt"  >> "$HOME/log.txt"
	if [ $? -eq 0 ]; then
		echo "${SUCCESS}Installed Python modules in $HOME/$envname/lib/python2.7/site-packages/ ${DEFAULT}"
	else
		echo "${ERROR}Failed to install python packages. Exitting... ${DEFAULT}"
		exit 1
	fi
else
	echo "${ERROR}Could not find requirements.txt. Exitting... ${DEFAULT}"
	exit 1
fi

if [ -e "$apifolder/db_config_sample.yml" ]; then
	if [ -e "$apifolder/db_config.yml" ]; then
		echo "${SUCCESS}Found existing db_config.yaml. ${DEFAULT}"
	else
		cp "$apifolder/db_config_sample.yml" "$apifolder/db_config.yml"
		echo "${SUCCESS}Copied db_config_sample.yml to db_config.yml ${DEFAULT}"
		echo "${ATTENTION}You can edit db_config.yml with your own settings if you do not like the default settings. ${DEFAULT}"
	fi
else
	echo "${ERROR}Could not find db_config_sample.yml. Exitting... ${DEFAULT}"
	exit 1
fi


if [ -e "$apifolder/manage.py" ]; then
	cd "$apifolder"
	python manage.py db upgrade >> "$HOME/log.txt"
	if [ $? -eq 0 ]; then
		echo "${SUCCESS}Database migration complete! ${DEFAULT}"
	else
		echo "${ERROR}Failed to migrate database. Exitting... ${DEFAULT}"
		exit 1
	fi
else
	echo "${ERROR}Could not find manage.py. Cannot migrate database. Exitting... ${DEFAULT}"
	exit 1
fi


#python satoyama-api/manage.py db upgrade