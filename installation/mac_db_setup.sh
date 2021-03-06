#!/bin/bash
LOG="$7"
#Postgresql install

brew install postgresql 2>&1
if [ $? -eq 0 ]; then
	echo "Psql installed"
else
	echo "Psql already install, proceed manually"
	exit 1
fi

postgres -D /usr/local/var/postgres &
mkdir -p ~/Library/LaunchAgents
ln -sfv /usr/local/opt/postgresql/*.plist ~/Library/LaunchAgents launchctl
launchctl load ~/Library/LaunchAgents/homebrew.mxcl.postgresql.plist

# Create psql roles and users
# http://forums.enterprisedb.com/posts/list/3447.page
psql -d postgres -c "create role satoyama with login"
psql -d postgres -c "alter role satoyama with superuser"
createdb satoyama_prod;
createdb satoyama_dev;
createdb satoyama_test;

# Migration
cd ..
cp db_config-sample.yml db_config.yml
python migrate_dev.py db upgrade