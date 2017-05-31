from tornado import web
from conf import settings
from sqlalchemy.orm import sessionmaker,scoped_session

class BaseHandler(web.RequestHandler):
    def initialize(self):
        self.db_session = scoped_session(sessionmaker(bind=settings.engine))
        self.db_query = self.db_session().query
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Methods","POST,GET" )

    def on_finish(self):
        self.db_session.remove()
