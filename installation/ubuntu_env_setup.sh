#!/bin/bash
startpath="/root/satoyama-api"
echo $startpath
envpath="/root/"
envname="satoyama-env"
cd $envpath
virtualenv $envname
echo $envpath$envname"/bin/activate"
. $envpath$envname"/bin/activate"
cd $startpath
pip install -r requirements.txt
#cp db_config_sample.yml db_config.yml
#python satoyama-api/manage.py db upgrade