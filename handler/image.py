from .base import BaseHandler
from model.db_obj import NodeDB
from . import utils
import json
import tornado
from conf.settings import COOKIE_NAME

class ImageList(BaseHandler):
    def get(self, *args, **kwargs):
        online_node = self.db_query(NodeDB).filter_by(state='Online').all()
        image_list = []
        image_list_simple = []
        for node in online_node:
            node_ip = node.ip
            node_port = node.port
            if utils.ping_port(node_ip, node_port) >= 0:
                node_image_url = 'http://' + str(node_ip) + ':' + str(node_port) + '/images/json'
                node_image_data_list = utils.HTTP.get(node_image_url)
                node_image_data_list = json.loads(node_image_data_list)
                for image in node_image_data_list:
                    temp_dict = {}
                    image['node'] = str(node_ip) + ':' + str(node_port)
                    temp_dict['Id'] = str(image['Id'])[7:19]
                    temp_dict['Repository'] = image['RepoTags']
                    temp_dict['Created'] = image['Created']
                    temp_dict['Size'] = image['Size']
                    temp_dict['node'] = image['node']
                    image_list_simple.append(temp_dict)
                image_list.extend(node_image_data_list)
        self.render('docker/image_base.html', image_list=image_list_simple,name=self.get_secure_cookie(COOKIE_NAME))
