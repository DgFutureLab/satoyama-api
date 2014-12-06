satoyama-api
============

REST API for Satoyama sensor networks based on Freaklabs open hardware.


# Installation on Ubuntu (using install script)
We've made shell script that painlessly handles the installation. The script has been tested on a clean Ubuntu 14.10 x32 machine. Steps:

1. Install git: $ sudo apt-get install git
2. Get the code: $ git clone https://github.com/DgFutureLab/satoyama-api.git
3. Run install script: sh satoyama-api/setup_ubuntu.sh

The script installs all the system packages required by the webserver including postgresql, creates databases for test, development and production modes, and creates a new Python environment in your home folder called satoyama-env. To run the webserver in development mode, change into the new environment and run the webserver startup script:

1. source ~/satoyama-env/bin/activate
2. python satoyama-api/run_webserver --env development

Enjoy!

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

You can make a new environment with all the binaries and python executables
$ virtualenv env
Now change into the new environment:
$ source env/bin/activate

Navigate into the satoyama-api folder and install the webapp dependencies:
$ pip install -r requirements.txt

Now run the migration script 
$ python manage.py db upgrade




API Usage
============

The API is hosted on Digital Ocean and the current entry point IP address is http://128.199.191.249/

Resource Types
===================

Site
----
Not yet implemented

Node
----
Nodes are computing elements gathering data from the environment. Each node can have 0 or more sensors attached to it.

Sensor
-----
Each sensor belongs to one node. Sensors gather information in "readings"


Reading
----
Each reading belongs to a sensor.

API Calls
===================

Get all current nodes in the network /node/all
----

## Get all the nodes in the network

Get the node_ids that belong to the current network

`GET /node/all`

#### Example

Request:
`GET /node/all`

Response:
```
{
    "data": [
        {
            "nodes" : [{"node_id" : 1,
                        "node_alias": "Chris Hatake North side",
                        "sensors" : [{"sensor_alias" : "temperature",
                        "latest_reading" : {"value" : 26.0, "time"}},
                        {"sensor_alias" : "distance"}]}]
        }
    ],
    "errors": [],
    "request": {},
    "warnings": []
}
```

Get  data readings from sensors
----
This is what you will use for storing and accessing readings from sensors.

#### Get the most recent reading from a sensor

In order to address a sensor a node_id and the sensor within that node must be provided.

`GET /reading/node_:node_id/:sensor_alias`

#### Example

Request:
`GET /reading/node_1/inside_temperature`

Response:
```
{
    "data": [
        {
            "timestamp" : 2014-09-10-11:29:41:468362,
            "value": 29.0
        }
    ],
    "errors": [],
    "request": {},
    "warnings": []
}
```


Tests
===================

Still only a few tests have been implemented BUT FEEL FREE TO WRITE MORE.
## Running tests
Go to satoyama-api root folder and simply run py.test -v -s

## Writing tests
As this project uses py.test, writing tests is easy. Place your test in a file prefixed 'test_' in the tests package. The actual tests are methods (class or not) beginning with 'test_'.

Development notes
===================

- All calls to the API returns a serialized instance of ApiResponse. The role of ApiResponse is to provide the client with information about problems with the request, such as wrongly named query parameters etc.
-- ApiResponse.errors do not contain any information about internal server errors, but rather information about what the API couldn't perform given the request.
- All query parameters are type-validated instantly upon receival, and sane error messages are added to the ApiResponse instance
- Data which is constained by satoyama, such as datetime formats, are validated in satoyama code, not in satoyama-api code
- REST resources are created for two cases.
-- REST URLs for all satoyama models, the handlers for which are mostly intended for administration purposes.
-- REST URLs for request types that can be grouped in terms of functionality, such as querying by geolocation, by datetime, and so on.
- As much as possible, functionality in URL handlers is placed in helpers to facilitate unit testing
-- Since a single resource will naturally have to be able to handle different variants of the query for which the resource is defined (for instance, the datetime REST resource should be able to handle queries such as "Give me all readings for some sensor between this and that day", and "give me readings from the last week of that sensor"), each handler will contain code that determines the nature of the request, branches accordingly and then calls helper methods designed to handle each particular case.
- All REST handlers should have a flow as follows:
-- Fetch allowed query parameters, and add an error to ApiResponse for each query parameter that is not allowed for that particular query.
-- Branch according to flavor of query (explained in previous point)
-- Fetch all objects requested by the query and add them to the ApiResponse.
Type validate 

Long term API development
===================

Let’s “draw inspiration” from things speak. What are the main features?

 - Real-time data
 - Data processing converting raw sensor data into meaningful status updates (you left your light on)
 - Data visualization - graphs and stuff. No biggie.
 - Geotagging - but it seems to be manual
 - Channels - A channel can track up to eight sensor values

Which features do we want to copy?

 - Real-time data (don’t know how they do it, but I suggest web sockets)
 - Channels, but slightly different. See below.

Which new features do we want?
- Better geo support - use reverse geocoding to get an address instead of just  longitude and latitude
  - This would enable quires such as “show me temperature measurements in Tokyo 23 wards and show heat map”
  - This could tricky for a system that should be globally useable, but it’s doable for Japan or other countries supported by gmaps
- Two types of node groupings
  - Places, that is nodes grouped by physical location.
    - Places can either be hierarchical (i.e., Kamogawa belongs to Chiba), but I think that's a bad idea because it would require strict supervision to make it correspond with real-worl geography. 
    - Instead I think it's better to just allow a Place to be defined as an arbitrary closed path drawn on a map, a post-code, city name or whatever. 
    - Hence a node can easily belong to several places at once. 
  - Networks (need to come up with a better name), that is nodes grouped not by physical location, but by organization, like the Rice Association of Japan, or something like that. 
