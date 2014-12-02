#!/bin/bash
sudo -u postgres psql -c "create role root with superuser login"
sudo -u postgres psql -c "create database root"
sudo -u postgres psql -c "create role satoyama with login superuser"
sudo -u postgres psql -c "alter role satoyama with password 'satoyama'"
sudo -u postgres psql -c "create database satoyama_test"