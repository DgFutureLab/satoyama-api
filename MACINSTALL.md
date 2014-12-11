# Satoyama-API Installation on MAC OSX Mavericks

## Python environment installation

1. cd ~/
2. sudo easy_install virtualenv
3. virtualenv env
4. source env/bin/activate

## Repository setup

1. git clone git@github.com:DgFutureLab/satoyama-api.git
2. cd satoyama-api/
3. pip install -r requirements.txt

## Setup database

1. brew install postgresql
2. postgres -D /usr/local/var/postgres
3. Make postgresql run everytime:

mkdir -p ~/Library/LaunchAgents

ln -sfv /usr/local/opt/postgresql/*.plist ~/Library/LaunchAgents

launchctl load ~/Library/LaunchAgents homebrew.mxcl.postgresql.plist

4. psql postgres (To get inside the postgres database console)

5. create role satoyama with login;

6. alter role satoyama with superuser;

(Optional: create database your-macosx-username , this step will allow you to login to postgres just using “psql” instead of “psql postgres”)

7. create database satoyama_production;

8. create database satoyama_development;

9. create database satoyama_test;

10. \q

(Optional: \l to list the the databases)

11. cp db-config-sample.yml db-config.yml

12. Replace the values of “username” and “password” with the ones you have setup on the previous steps. If you have used the default values when creating the psql database and roles you can leave you can skip this step.


13. python manage.py db upgrade (creates database schema)


14. python run_webserver.py --env development




Notes: 
createuser satoyama —login —superuser —pwprompt

pip freeze 
alter user satoyama with password ‘satoyama’;