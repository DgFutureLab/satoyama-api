#!/bin/bash
virtualenv ../env
source ../env/bin/activate

pip install -r requirements.txt
cp db_config_sample.yml db_config.yml
python satoyama-api/manage.py db upgrade