from .base import BaseHandler
from conf.settings import COOKIE_NAME
import datetime
from model.db_obj import Event as Table_Event
from sqlalchemy import between
import json

class Event(BaseHandler):
    def get(self, *args, **kwargs):
        #online_node = Statics.online_node(self.db_query, NodeDB)
        #online_node_num = len(online_node)
        #up_con = Statics.online_con(online_node)
        #total_images = 0
        self.render('mgt/event_base.html',
                    name=self.get_secure_cookie(COOKIE_NAME))


class EventSearch(BaseHandler):
    def post(self, *args, **kwargs):
        raw_time_range = self.get_argument('time_range')
        start_time, end_time = raw_time_range.split('-')
        start_date = datetime.datetime.strptime(start_time.strip(),"%m/%d/%Y").date()
        end_date = datetime.datetime.strptime(end_time.strip(),"%m/%d/%Y").date()
        event_objs = self.db_query(Table_Event).filter(Table_Event.date>=start_date).filter(Table_Event.date<=end_date).all()
        #self.render('mgt/event_base.html',
        #            name=self.get_secure_cookie(COOKIE_NAME),events=event_objs)
        event_data = []
        for event in event_objs:
            data = {
                'id':event.id,
                'item_id': event.item_id,
                'item_type' : event.item_type,
                'key_action' : event.key_action,
                'date' : event.date.strftime("%Y-%m-%d-%H"),
                'details' : event.details
            }
            event_data.append(data)
        self.write(json.dumps(event_data))