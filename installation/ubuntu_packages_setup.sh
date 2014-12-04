#!/bin/bash
sudo apt-get update
sudo apt-get install -y libpq-dev postgresql postgresql-contrib
sudo apt-get install python-psycopg2
sudo apt-get install -y git
sudo apt-get install -y python-setuptools python-dev
sudo easy_install virtualenv