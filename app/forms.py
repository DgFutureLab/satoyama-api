from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired

class NodeForm(Form):
	uuid = StringField('uuid')
	alias = StringField('alias')