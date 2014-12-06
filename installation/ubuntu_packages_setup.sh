#!/bin/bash
apifolder="$1"
envname="$2"
DEFAULT="$3"
ATTENTION="$4"
SUCCESS="$5"
ERROR="$6"

echo "${ATTENTION}Installing Ubuntu packages. This may take a while... ${DEFAULT}"
sudo apt-get update -q
sudo apt-get install -y -q libpq-dev postgresql postgresql-contrib python-setuptools python-dev
sudo apt-get build-dep -y -q python-psycopg2
sudo easy_install virtualenv
echo "${SUCCESS}Installed Ubuntu packages. ${DEFAULT}"