#!/bin/bash
#Postgresql install
brew install postgresql
postgres -D /usr/local/var/postgres &
mkdir -p ~/Library/LaunchAgents
ln -sfv /usr/local/opt/postgresql/*.plist ~/Library/LaunchAgents launchctl
launchctl load ~/Library/LaunchAgents/homebrew.mxcl.postgresql.plist

# Create psql roles and users
# http://forums.enterprisedb.com/posts/list/3447.page
createuser satoyama —login —superuser —pwprompt
createdb satoyama_production;
createdb satoyama_development;
createdb satoyama_test;

# Migration
cd ..
cp db-config-sample.yml db-config.yml
python manage.py db upgrade
