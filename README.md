satoyama-api
============

RESTful (more or less) API for working with sensor networks based on Satoyama (https://github.com/DgFutureLab/satoyama, https://pypi.python.org/pypi/satoyama)


# DEV NOTES
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


# API base URLs
## Used by admin tools:
- /node
- /sensor
- /

##
- /batch/readings
- /area?sensortype=

#Long term API development

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

