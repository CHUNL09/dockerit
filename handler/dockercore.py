from .base import BaseHandler
from model.db_obj import NodeDB,User,Event
from .utils import HTTP,MyCurl
from conf.settings import COOKIE_NAME
from . import utils
import json
import time
import os
import tarfile

class DashBoardInfo(BaseHandler):
    def get(self, *args, **kwargs):
        online_node = Statics.online_node(self.db_query,NodeDB)
        online_node_num = len(online_node)
        up_con = Statics.online_con(online_node)
        total_images = 0
        self.render('docker/dashboard.html',online_node=online_node_num,up_con=up_con,total_images=total_images,name=self.get_secure_cookie(COOKIE_NAME))

def event_decorator(item):
    def wrapper1(func):
        def wrapper2(self,*args,**kwargs):

            action_type = self.get_argument('action')
            user_name = self.get_secure_cookie(COOKIE_NAME)

            node_ip_port = self.get_argument('node_ip_port')

            item_type = item
            if item_type == "container":
                item_id = 2
            elif item_type == "image":
                item_id = 3

            user_obj = self.db_query(User).filter_by(name=user_name).first()
            detail = "%s Operation|%s|%s" %(item_type,action_type,node_ip_port)

            event_rec = Event(item_id=item_id,item_type=item_type,key_action=action_type,
                              user=user_obj.id,details=detail)
            res = func(self, *args, **kwargs)
            self.db_session.add(event_rec)
            self.db_session.commit()
            return res

        return wrapper2
    return wrapper1


class ContainerAPI(BaseHandler):
    @event_decorator("container")
    def get(self, *args, **kwargs):
        container_id = self.get_argument('con_id')
        node_ip_port = self.get_argument('node_ip_port')
        action = self.get_argument('action')
        if action == 'inspect':
            res = APImethod.get_con_info(container_id,node_ip_port)
            self.write(res)
        if action == 'start':
            print("start container request ------->")
            res = APImethod.start_con(container_id, node_ip_port)
            self.write(res)
        if action == 'stop':
            print("stop container request ------->")
            res = APImethod.stop_con(container_id, node_ip_port)
            self.write(res)
        if action == 'remove':
            print("remove container request ------->")
            res = APImethod.remove_con(container_id, node_ip_port)
            self.write(res)

class ImageAPI(BaseHandler):

    @event_decorator("image")
    def get(self, *args, **kwargs):
        image_id = self.get_argument('image_id')
        node_ip_port = self.get_argument('node_ip_port')
        print("image_id,ip_port-------->", image_id, node_ip_port)
        action = self.get_argument('action')

        if action == 'delete':
            res = APImethod.del_image(image_id, node_ip_port)
            print(res,"-----res-------")
            self.write(res)

    @event_decorator("image")
    def post(self, *args, **kwargs):
        action_type = self.get_argument('action')
        if action_type == 'update_tag':
            image_id = self.get_argument('image_id')
            ip_port = self.get_argument('ip_port')
            tag_name = self.get_argument('tag_name')
            repo_name = self.get_argument('new_repo')
            res= APImethod.update_image_tag(image_id,ip_port,repo_name,tag_name)
            print(res)
        if action_type == 'build_image':
            dockerfile = self.get_argument('dockerfile')
            image_tag = self.get_argument('image_tag')
            ip_port = self.get_argument('ip_port')
            path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            local_file_name = 'Dockerfile'+str(time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(time.time())))
            file_path = path+'/statics/server_files/build/'
            cur_path = os.getcwd()
            if not os.path.exists(file_path):
                os.makedirs(file_path)
            tar_file = local_file_name+'.tar'
            os.chdir(file_path)
            with tarfile.open(tar_file, "w:gz") as tar:
                with open('Dockerfile', 'w') as f:
                    f.write(dockerfile)
                tar.add('Dockerfile')
            os.remove('Dockerfile')
            os.chdir(cur_path)
            APImethod.build_image(ip_port,image_tag,file_path+tar_file)

class APImethod(object):
    @staticmethod
    def get_con_info(container_id,node_ip_port):
        request_url = 'http://'+node_ip_port+'/containers/'+container_id+'/json'
        con_info = HTTP.get(request_url)
        return con_info

    @staticmethod
    def start_con(container_id,node_ip_port):
        request_url = 'http://' + node_ip_port + '/containers/' + container_id + '/start'
        con_info = HTTP.post(request_url)
        return con_info

    @staticmethod
    def stop_con(container_id, node_ip_port):
        request_url = 'http://' + node_ip_port + '/containers/' + container_id + '/stop'
        con_info = HTTP.post(request_url)
        return con_info

    @staticmethod
    def remove_con(container_id, node_ip_port):
        request_url = 'http://' + node_ip_port + '/containers/' + container_id
        con_info = HTTP.delete(request_url)
        return con_info

    @staticmethod
    def del_image(image_id, node_ip_port):
        request_url = 'http://' + node_ip_port + '/images/' + image_id+'?force=true'
        image_info = HTTP.delete(request_url)
        return image_info

    @staticmethod
    def update_image_tag(image_id, node_ip_port, new_repo,new_tag):
        request_url = 'http://' + node_ip_port + '/images/' + image_id + '/tag?repo='+new_repo+'&tag='+new_tag
        print(request_url)
        image_info = HTTP.post(request_url)
        return image_info

    @staticmethod
    def build_image(node_ip_port, name_tag, tar_file):

        request_url = 'http://' + node_ip_port + '/build'  + '?t=' + name_tag
        print(request_url)
        print(tar_file)
        raw_data = open(tar_file,'rb').read()
        file_len = os.path.getsize(tar_file)
        headers = {
            'Content-Type' : 'application/tar',
            'Content-Length': file_len
        }
        image_info = HTTP.post_file(request_url,raw_data,headers)
        return image_info
        # request_url = 'http://' + node_ip_port + '/build' + '?t=' + name_tag
        # MyCurl.post_file(request_url,tar_file)

class Statics(object):
    @staticmethod
    def online_node(db_query,db_table):
        online_node = db_query(db_table).filter_by(state='Online').all()
        return online_node

    @staticmethod
    def online_con(online_node_obj):
        up_con = 0
        for node in online_node_obj:
            node_ip = node.ip
            node_port = node.port
            if utils.ping_port(node_ip, node_port) >= 0:
                node_container_url = 'http://' + str(node_ip) + ':' + str(node_port) + '/containers/json'
                node_con_data_list = utils.HTTP.get(node_container_url)
                node_con_data_list = json.loads(node_con_data_list)
                up_con += len(node_con_data_list)
        return up_con