
from sqlalchemy.ext.declarative import declarative_base
import inspect
from app import flapp
Base = declarative_base()

def nuke_db():
	# assert isinstance(engine )
	import models
	flapp.db_session.close()
	Base.metadata.drop_all(bind=flapp.engine)

def init_db():
	import models
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
	Base.query = flapp.db_session.query_property()
	Base.metadata.create_all(bind=flapp.engine)

def recreate():
	nuke_db()
	init_db()


def get_defined_models():
	import models
	import sqlalchemy
	members = dict(inspect.getmembers(models))
	members.pop('Base')
	models = list()
	for name, member in members.items():
		if isinstance(member, sqlalchemy.ext.declarative.api.DeclarativeMeta):
			models.append(member)
	return models