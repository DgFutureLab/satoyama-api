#!/bin/bash
apifolder="$1"
envname="$2"
DEFAULT="$3"
ATTENTION="$4"
SUCCESS="$5"
ERROR="$6"



sudo -u postgres psql -c "create role root with superuser login"
sudo -u postgres psql -c "create database root"
sudo -u postgres psql -c "create role satoyama with login superuser"
sudo -u postgres psql -c "alter role satoyama with password 'satoyama'"
sudo -u postgres psql -c "create database satoyama_test"

echo "${SUCCESS} Database setup complete!"