from .base import BaseHandler
from model.db_obj import NodeDB
from . import utils
import json
import tornado
from conf.settings import COOKIE_NAME

class ContainerList(BaseHandler):
    def get(self, *args, **kwargs):
        online_node = self.db_query(NodeDB).filter_by(state='Online').all()
        con_list = []
        con_list_simple = []
        for node in online_node:
            node_ip = node.ip
            node_port = node.port
            if utils.ping_port(node_ip, node_port) >= 0:
                node_container_url = 'http://' + str(node_ip) + ':' + str(node_port) + '/containers/json?all=1'
                node_con_data_list = utils.HTTP.get(node_container_url)
                node_con_data_list = json.loads(node_con_data_list)
                for container in node_con_data_list:
                    temp_dict = {}
                    container['node'] = str(node_ip) + ':' + str(node_port)
                    temp_dict['Id'] = str(container['Id'])[:8]
                    if len(container['Image']) >24:
                        temp_dict['Image'] = str(container['Image'])[:24]
                    else:
                        temp_dict['Image'] = container['Image']
                    temp_dict['Command'] = container['Command']
                    temp_dict['Created'] = container['Created']
                    temp_dict['Status'] = container['Status']
                    temp_dict['node'] = container['node']
                    con_list_simple.append(temp_dict)
                con_list.extend(node_con_data_list)
        #print(con_list)
        self.render('docker/container_base.html', con_list=con_list_simple,substr=getattr(utils.TemplateFunc,'substr'),
                    name=self.get_secure_cookie(COOKIE_NAME))


class Container(BaseHandler):
    pass
