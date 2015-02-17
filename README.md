Satoyama API
============
REST API for sensor networks created by <a href="http://fljapan.com/">Future Lab</a> based on <a href="http://www.freaklabsstore.com">Freaklabs open hardware</a>. Satoyama API facilitates the collection of data from sensors attached to Chibi or Saboten devices.

Installation on Ubuntu
===================
The script has been tested on a clean Ubuntu 14.10 x32 machine:

1. Install git: $ sudo apt-get install git
2. Get the code: $ git clone https://github.com/DgFutureLab/satoyama-api.git
3. Run install script: sh satoyama-api/setup_ubuntu.sh

The script installs all the system packages required by the webserver including postgresql, creates databases for test, development and production modes, and creates a new Python environment in your home folder called satoyama-env. To run the webserver in development mode, change into the new environment and run the webserver startup script:

1. source ~/satoyama-env/bin/activate
2. python satoyama-api/run_webserver --env development

If you had problems: <a href="https://github.com/DgFutureLab/satoyama-api/blob/master/UBUNTUINSTALL.md">Detailed manual Ubuntu installation</a>.
For Mac users: <a href="https://github.com/DgFutureLab/satoyama-api/blob/master/MACINSTALL.md">Detailed manual Mac installation</a>.

# Entry point and resources:

The API is hosted on Digital Ocean and the current entry point for production sensor networks is http://satoyamacloud.com, for testing purposes use http://128.199.120.30/

Resource Types: **Site**, each site has many nodes. **Node**, nodes are computing elements gathering data from the environment.
Each node can have 0 or more sensors attached to it. **Sensor**, each sensor belongs to one node. **Sensors** gather information in "readings". **Reading**, each reading belongs to a sensor. You can see more details about the current ERD <a href="https://github.com/DgFutureLab/satoyama-api/blob/master/docs/SatoyamaApiERD.jpg">here</a>.

# API Endpoints
Each of the following are resources that can be accessed via HTTP requests.

* Site [GET, POST, DELETE]
* Sites [GET]
* Node [GET, POST, DELETE]
* Nodes [GET]
* Sensor [GET, POST]
* Sensors [GET]
* Readings [GET]

The following sections documents how to use these endpoints.

## Site resource

Get all nodes belonging to site 1:

`GET /site/1`

Output:
```
{
    "errors": [], 
    "objects": [
        {
            "alias": "hackerfarm", 
            "id": 17, 
            "nodes": [
                {
                    "alias": "garden5", 
                    "id": 7, 
                    "latitude": 35.144828, 
                    "longitude": 139.962516, 
                    "sensors": [
                        {
                            "alias": "temperature", 
                            "id": 18, 
                            "latest_reading": null
                        }, 
                        {
                            "alias": "distance", 
                            "id": 19, 
                            "latest_reading": null
                        }, 
                        {
                            "alias": "humidity", 
                            "id": 20, 
                            "latest_reading": null
                        }, 
                        {
                            "alias": "vbat", 
                            "id": 21, 
                            "latest_reading": null
                        }
                    ]
                }
}
```

Create a new site with no nodes:

`POST /site`

Delete site 1:

`DELETE /site/1`

## Sites resource
Get a list of all sites:

`GET /sites`

## Node resource
Get data for node 1:

`GET /node/1`

Delete node 1:

`DELETE /node/1`

Create a new node at site 1:

`POST /node`

POST parameters are:
* alias: The name of the node
* node_type: The type of the node, e.g. "ricefield"
* site_id: The id of the site that the node will belong to
* latitude
* longitude

## Nodes Resource
Get a list of all nodes in the network.

Request:
`GET /nodes`

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

## Sensor & Sensors Resource
Not implemented yet.

## Readings Resource
There are several ways to access readings using the following query parameters:

Get readings from sensor 10:

`GET /readings?sensor_id=10`

Get readings from the sensor with alias "temperature" attached to node 3:

`GET /readings?sensor_alias=temperature&node_id=3`

### Interval queries
You also can use query parameters to specify a datetime interval for the readings:
* from
* until

For instance, get all readings from sensor 6 from January 1st 2015 to January 10th 2015:

`GET /readings?sensor_id=10&from=2015-1-1&until=2015-1-10`

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

# Current active nodes

## Digital Garage building: 

### NODE ID 18: http://satoyamacloud.com/node/18, Temperature sensor readings from this node: http://satoyamacloud.com/readings?sensor_id=50 , Humidity sensor reading from this sensor: http://satoyamacloud.com/readings?sensor_id=52

# Tests

As this project uses py.test, writing tests is easy. Place your test in a file prefixed 'test_' in the tests package. The actual tests are methods (class or not) beginning with 'test_'.

1. from satoyama-api root folder and simply run py.test -v -s

# <a href="https://github.com/DgFutureLab/satoyama-api/blob/master/LICENSE">The MIT License (MIT)</a>

Hacker Farm - Future Lab
