satoyama-api
============

RESTful (more or less) API for working with sensor networks based on Satoyama (https://github.com/DgFutureLab/satoyama, https://pypi.python.org/pypi/satoyama)

# DEV NOTES
- All data is type-validated instantly upon receival
- Data which is constained by satoyama, such as datetime formats, are validated in satoyama code
- REST resources use flask-restful argparse to get sane messages in the response
- URLs for managing resources (i.e. CRUD actions on satoyama models) are kept as simple as possible. 
- ALL calls to the API return a ApiResponse rendered as json
- ApiResponse.errors do not contain any information about internal server errors, but rather information about what the API couldn't perform given the request.

# DEV QUESTIONS
What should the user see when something goes rotten in the server, like some code throws an unhandled exception?

# API base URLs
## Used by admin tools:
- /node
- /sensor
- /

##
- /batch/readings
- /area?sensortype=