# Installation on Ubuntu (manual)
## Setup database
First, install postgresql

1. $ sudo apt-get update
2. $ sudo apt-get install libpq-dev postgresql postgresql-contrib

First, let's download the app from github. If you don't already have git, install it:
$ sudo apt-get install git
Then clone the app
$ git clone https://github.com/DgFutureLab/satoyama-api.git

$ cp db_config_sample.yml db_config.yml

Now let's create the user that the webapp will use. You will be asked to enter a password, so make 

$ createuser satoyama --login --superuser --pwprompt

Log into psql and change the password for the new user

\# alter user satoyama with password 'satoyama';

We also have to create the databases for the webapp

$ createdb satoyama_test;

$ createdb satoyama_dev;

$ createdb satoyama_prod;

## Setup app environment

Now we install the tools required to make a standalone environment for the app:

$ sudo apt-get install python-setuptools python-dev
$ sudo easy_install virtualenv

You can make a new environment with all the binaries and python executables:

$ virtualenv env
Now change into the new environment:
$ source env/bin/activate

Navigate into the satoyama-api folder and install the webapp dependencies:
$ pip install -r requirements.txt

Now run the migration script 
$ python manage.py db upgrade
