#!/bin/bash
virtualenv env
source env/bin/activate

git clone https://github.com/DgFutureLab/satoyama-api.git
pip install -r satoyama-api/requirements.txt
cp satoyama-api/db_config_sample.yml satoyama-api/db_config.yml
python satoyama-api/manage.py db upgrade