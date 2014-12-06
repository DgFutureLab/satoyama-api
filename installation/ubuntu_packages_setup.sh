#!/bin/bash
apifolder="$1"
envname="$2"
DEFAULT="$3"
ATTENTION="$4"
SUCCESS="$5"
ERROR="$6"

# echo "${ATTENTION}Installing Ubuntu packages. This may take a while... ${DEFAULT}"
echo "${ATTENTION}Running sudo apt-get update -qq${DEFAULT}"
sudo apt-get update -qq
echo "${ATTENTION}Running sudo apt-get install -y -qq libpq-dev postgresql postgresql-contrib python-setuptools python-dev${DEFAULT}"
sudo apt-get install -y -qq libpq-dev postgresql postgresql-contrib python-setuptools python-dev

echo "${ATTENTION}sudo apt-get build-dep -y -qq python-psycopg2${DEFAULT}"
sudo apt-get build-dep -y -qq python-psycopg2

sudo easy_install virtualenv
echo "${SUCCESS}Installed all Ubuntu packages! ${DEFAULT}"