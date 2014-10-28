from flask import Flask

flapp = Flask('sensor_api')

from helpers import UrlHelper, RequestHelper
UrlHelper(flapp)
RequestHelper(flapp)
# def register_helper(self, func):
# 	setattr(self, func.func_name, func)	
# flapp.register_helper = register_helper

### Use Twitter Bootstrap
from flask_bootstrap import Bootstrap
Bootstrap(flapp)

### Restify the app
from flask.ext import restful
rest_api = restful.Api(flapp)

### Adds websocket to app
from flask.ext.socketio import SocketIO
socketio = SocketIO(flapp)

from flask_limiter import Limiter
limiter = Limiter(flapp, global_limits=["1 per second"])

### Before importing other modules, import and setup run configuration
import conf
flapp.config.update(conf.module_config)
conf.configure_flapp('dev')
import satoyama


### Import modules containing statements that must be executed when the webapp is started (such as adding routes for the REST api)
import resources, views, conf





@flapp.teardown_appcontext
def shutdown_session(exception=None):
    flapp.db_session.remove()

# from resources import ApiResponse
# @flapp.after_request
# def create_response():
# 	response = ApiResponse()
# 	return response