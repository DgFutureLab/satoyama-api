#!/bin/bash
apifolder="$1"
envname="$2"
DEFAULT="$3"
ATTENTION="$4"
SUCCESS="$5"
ERROR="$6"
LOG="$7"


echo "${ATTENTION}Setting up database. ${DEFAULT}"

### ON MAC DO THIS:
# psql -c "create role satoyama with login superuser"
# psql -c "alter role satoyama with password 'satoyama'"
# psql -c "create database satoyama_dev"
# psql -c "create database satoyama_test"
# psql -c "create database satoyama_prod"


sudo -u postgres psql -c "create role satoyama with login superuser" >> "$HOME/$LOG" 2>&1
sudo -u postgres psql -c "alter role satoyama with password 'satoyama'" >> "$HOME/$LOG" 2>&1
sudo -u postgres psql -c "create database satoyama_dev" >> "$HOME/$LOG" 2>&1
sudo -u postgres psql -c "create database satoyama_test" >> "$HOME/$LOG" 2>&1
sudo -u postgres psql -c "create database satoyama_prod" >> "$HOME/$LOG" 2>&1



echo "${SUCCESS}Database setup complete! Created databases satoyama_test, satoyama_dev and satoyama_prod and database user satoyama.${DEFAULT}"