#!/bin/bash
apifolder="$1"
envname="$2"
DEFAULT="$3"
ATTENTION="$4"
SUCCESS="$5"
ERROR="$6"

echo "${ATTENTION} Installing Ubuntu packages. This may take a while. ${DEFAULT}"
sudo apt-get update -qq
sudo apt-get install -y -qq libpq-dev postgresql postgresql-contrib
sudo apt-get install -y -qq python-psycopg2
sudo apt-get install -y -qq git
sudo apt-get install -y -qq python-setuptools python-dev
sudo apt-get build-dep -y -qq python-psycopg2
sudo easy_install virtualenv
echo "${SUCCESS} Installed Ubuntu packages. ${DEFAULT}"