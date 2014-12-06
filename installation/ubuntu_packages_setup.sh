#!/bin/bash
apifolder="$1"
envname="$2"
DEFAULT="$3"
ATTENTION="$4"
SUCCESS="$5"
ERROR="$6"
LOG="$7
"
# echo "${ATTENTION}Installing Ubuntu packages. This may take a while... ${DEFAULT}"
echo "${ATTENTION}Running sudo apt-get update -qq${DEFAULT}"
sudo apt-get update -y >> "$HOME/$LOG" 2>&1
echo "${ATTENTION}Running sudo apt-get install -y -qq libpq-dev postgresql postgresql-contrib python-setuptools python-dev${DEFAULT}"
sudo apt-get install -y libpq-dev postgresql postgresql-contrib python-setuptools python-dev >> "$HOME/$LOG" 2>&1

echo "${ATTENTION}sudo apt-get build-dep -y -qq python-psycopg2${DEFAULT}"
sudo apt-get build-dep -y python-psycopg2 >> "$HOME/$LOG" 2>&1

sudo easy_install virtualenv >> "$HOME/$LOG" 2>&1
echo "${SUCCESS}Installed all Ubuntu packages! ${DEFAULT}"