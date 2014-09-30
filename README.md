satoyama-api
============

RESTful (more or less) API for working with sensor networks based on Satoyama (https://github.com/DgFutureLab/satoyama, https://pypi.python.org/pypi/satoyama)

#Long term API development

Let’s “draw inspiration” from things speak. What are the main features?


 * Real-time data
 * Data processing converting raw sensor data into meaningful status updates (you left your light on)
 * Data visualization - graphs and stuff. No biggie.
 * Geotagging - but it seems to be manual
 * Channels - A channel can track up to eight sensor values

Which features do we want to copy?

   * Real-time data (don’t know how they do it, but I suggest web sockets)
   * Chan

Which new features do we want?
- Better geo support - use reverse geocoding to get an address instead of just  longitude and latitude
  - This would enable quires such as “show me temperature measurements in Tokyo 23 wards and show heat map”
  - This could tricky for a system that should be globally useable, but it’s doable for Japan or other countries supported by gmaps
- Two types of node groupings
  - asd


