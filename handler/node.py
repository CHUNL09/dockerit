from .base import BaseHandler
from model.db_obj import NodeDB,User,Event
from model.db_ops import DBCRUD
import tornado
from . import utils
from .utils import HTTP
from conf.settings import COOKIE_NAME
import os,sys
import json

def event_decroator(func):
    def wrapper(self,*args,**kwargs):

        action_type = self.get_argument('action')
        user_name = self.get_secure_cookie(COOKIE_NAME)

        try:
            node_id = self.get_argument('node_id')
        except Exception as e:
            node_id = None

        if node_id:
            node_obj = self.db_query(NodeDB).filter_by(id=node_id).first()
            node_ip = node_obj.ip
            node_port = node_obj.port
        else:
            node_ip = self.get_argument('node_ip')
            node_port = self.get_argument('node_port')
        item_id = 1
        item_type = "node"
        user_obj = self.db_query(User).filter_by(name=user_name).first()
        detail = "Node Operation|%s|%s:%s" %(action_type,node_ip,node_port)
        event_rec = Event(item_id=item_id,item_type=item_type,key_action=action_type,
                          user=user_obj.id,details=detail)
        res = func(self, *args, **kwargs)
        self.db_session.add(event_rec)
        self.db_session.commit()
        return res

    return wrapper


class NodeCRUD(BaseHandler):

    def get(self, *args, **kwargs):  # view node item
        pass

    @event_decroator
    def post(self, *args, **kwargs): # create/update/delete node item
        action_type = self.get_argument('action')
        if action_type == 'delete':
            node_id = self.get_argument('node_id')
            node_ins = Node(self.db_session,self.db_query,node_id=node_id)
            node_ins._delete()
            print("delete success")
        if action_type == 'add':
            node_ip = self.get_argument('node_ip')
            node_port = self.get_argument('node_port')
            node_ins = Node(self.db_session,self.db_query,node_ip=node_ip,node_port=node_port)
            node_ins._add()

        if action_type == 'update':
            node_ip = self.get_argument('node_ip')
            node_port = self.get_argument('node_port')
            Node(self.db_session, self.db_query, node_ip=node_ip, node_port=node_port)
            print('online update finished')

        if action_type == 'modify':
            node_id = self.get_argument('node_id')
            node_ip = self.get_argument('node_ip')
            node_port = self.get_argument('node_port')
            node_state = self.get_argument('node_state')
            node_group = self.get_argument('node_group')
            node_ins = Node(self.db_session, self.db_query, node_id=node_id)
            modified_dic={
                'id': node_id,
                'ip': node_ip,
                'port': node_port,
                'state': node_state,
                'node_group':node_group
            }
            node_ins._update(ip=node_ip,port=node_port,state=node_state,node_group=node_group)


class NodeInfo(BaseHandler):
    def get(self, *args, **kwargs):
        all_node = self.db_query(NodeDB).all()
        node_list = []
        for single_node in all_node:
            node_ip = single_node.ip
            node_port = single_node.port
            node = Node(self.db_session,self.db_query,node_ip=node_ip,node_port=node_port)
            node_info = {}
            node_info["id"] = node.current_node_info.id
            node_info["name"] = node.current_node_info.hostname
            node_info["node_ip"] = node.current_node_info.ip
            node_info["port"] = node.current_node_info.port
            node_info["cpus"] = node.current_node_info.cpus
            node_info["mem"] = node.current_node_info.mem
            node_info["images"] = node.current_node_info.images
            node_info["state"] = node.current_node_info.state
            node_info["node_group"] = node.current_node_info.node_group
            node_info["containers"] = node.current_node_info.containers
            node_info["os_version"] = node.current_node_info.os_version
            node_info["kernel_version"] = node.current_node_info.kernel_version
            node_info["docker_version"] = node.current_node_info.docker_version
            node_list.append(node_info)
        self.render('docker/node_base.html',node_list = node_list,node_str=tornado.escape.json_encode(node_list),
                    name=self.get_secure_cookie(COOKIE_NAME))

class Node(object):
    def __init__(self,db_session,db_query,**kwargs):
        if 'node_ip' in kwargs:
            self.ip = kwargs['node_ip']
        else:
            self.ip = None
        if 'node_port' in kwargs:
            self.port = kwargs['node_port']
        else:
            self.port = None
        if 'node_id' in kwargs:
            self.node_id = kwargs['node_id']
        self.db_query = db_query
        self.db_session = db_session
        if self.port and self.ip:
            self.self_node = self.db_query(NodeDB).filter_by(ip=self.ip,port=self.port).first()

            if utils.ping_port(self.ip, self.port) >= 0:  # update node info online
                node_req_url = 'http://' + str(self.ip) + ':' + str(self.port) + '/info'
                self._onlineupdate(node_req_url)
        else:
            self.self_node = self.db_query(NodeDB).filter_by(id=self.node_id).first()
        self.current_node_info = self.self_node

    def _onlineupdate(self,req_url):
        raw_node_info = HTTP.get(req_url)
        node_info_dict = json.loads(raw_node_info)
        tmp_dict={}
        tmp_dict["hostname"] = node_info_dict['Name']
        tmp_dict["ip"] = self.ip
        tmp_dict["port"] = self.port
        tmp_dict["cpus"] = node_info_dict['NCPU']
        tmp_dict["mem"] = node_info_dict['MemTotal']
        tmp_dict["images"] = node_info_dict['Images']
        tmp_dict["state"] = 'Online'
        #tmp_dict["node_group"] = ''
        tmp_dict["containers"] = node_info_dict['Containers']
        tmp_dict["os_version"] = node_info_dict['OperatingSystem']
        tmp_dict["kernel_version"] = node_info_dict['KernelVersion']
        tmp_dict["docker_version"] = node_info_dict['ServerVersion']

        if DBCRUD.update_record(tmp_dict,self.self_node) >=0:
            self.db_session.commit()
        else:
            print("update node record failed")
        self.current_node_info = self.db_query(NodeDB).filter_by(ip=self.ip,port=self.port).first()

    def _delete(self):
        self.db_session.delete(self.self_node)
        self.db_session.commit()

    def _add(self):
        new_node = NodeDB(ip=self.ip,port=self.port)
        self.db_session.add(new_node)
        self.db_session.commit()
        self.current_node_info = self.db_query(NodeDB).filter_by(ip=self.ip,port=self.port).first()

    def _update(self,**kwargs):
        for key in kwargs.keys():
            if getattr(self.self_node,key)!=kwargs[key]:
                print(key,kwargs[key])
                setattr(self.self_node, key, kwargs[key])
                print(self.self_node.state,"----->")
                print(self.self_node.node_group,"----->")
                self.db_session.commit()
        self.current_node_info = self.db_query(NodeDB).filter_by(id=self.node_id).first()

