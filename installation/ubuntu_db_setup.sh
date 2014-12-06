#!/bin/bash
apifolder="$1"
envname="$2"
DEFAULT="$3"
ATTENTION="$4"
SUCCESS="$5"
ERROR="$6"


echo "${ATTENTION}Setting up database. ${DEFAULT}"

### ON MAC DO THIS:
# psql -c "create role satoyama with login superuser"
# psql -c "alter role satoyama with password 'satoyama'"
# psql -c "create database satoyama_dev"
# psql -c "create database satoyama_test"
# psql -c "create database satoyama_prod"


sudo -u postgres psql -q -c "create role satoyama with login superuser" >> /dev/null
sudo -u postgres psql -q -c "alter role satoyama with password 'satoyama'" >> /dev/null
sudo -u postgres psql -q -c "create database satoyama_dev" >> /dev/null
sudo -u postgres psql -q -c "create database satoyama_test" >> /dev/null
sudo -u postgres psql -q -c "create database satoyama_prod" >> /dev/null



echo "${SUCCESS}Database setup complete! Created databases satoyama_test, satoyama_dev and satoyama_prod and database user satoyama.${DEFAULT}"