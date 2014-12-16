satoyama-api
============
REST API for sensor networks based on Freaklabs open hardware. Satoyama-api facilitates the collection of data from sensors attached to Chibi or Saboten devices.

Installation on Ubuntu
===================
We've made shell script that painlessly handles the installation. The script has been tested on a clean Ubuntu 14.10 x32 machine. Steps:

1. Install git: $ sudo apt-get install git
2. Get the code: $ git clone https://github.com/DgFutureLab/satoyama-api.git
3. Run install script: sh satoyama-api/setup_ubuntu.sh

The script installs all the system packages required by the webserver including postgresql, creates databases for test, development and production modes, and creates a new Python environment in your home folder called satoyama-env. To run the webserver in development mode, change into the new environment and run the webserver startup script:

1. source ~/satoyama-env/bin/activate
2. python satoyama-api/run_webserver --env development

Enjoy!

If you had problems: <a href="https://github.com/DgFutureLab/satoyama-api/blob/master/UBUNTUINSTALL.md">Detailed manual Ubuntu installation</a>.
For Mac users: <a href="https://github.com/DgFutureLab/satoyama-api/blob/master/MACINSTALL.md">Detailed manual Mac installation</a>.

API
===================
The API is hosted on Digital Ocean and the current entry point IP address is http://128.199.191.249/

Resource Types: **Site**, each site has many nodes. **Node**, nodes are computing elements gathering data from the environment.
Each node can have 0 or more sensors attached to it. **Sensor**, each sensor belongs to one node. **Sensors** gather information in "readings".
**Reading**, each reading belongs to a sensor.

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

## Get data readings from sensors

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