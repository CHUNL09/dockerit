from .base import BaseHandler
from model.db_init import User
from . import utils
from model.db_obj import NodeDB
from .dockercore import Statics
from conf.settings import COOKIE_NAME

class Login(BaseHandler):
    def get(self, *args, **kwargs):
        self.render('user/login.html')

    def post(self, *args, **kwargs):
        input_username = self.get_argument("username")
        input_pass = self.get_argument("password")
        if self.user_validate(input_username,input_pass):
            online_node = Statics.online_node(self.db_query,NodeDB)
            online_node_num = len(online_node)
            up_con = Statics.online_con(online_node)
            total_images = 0
            self.set_secure_cookie(COOKIE_NAME, input_username, expires_days=1)

            self.render('docker/dashboard.html',online_node=online_node_num,up_con=up_con,total_images=total_images,name=self.get_secure_cookie(COOKIE_NAME))
        else:
            self.write('wrong username or password')

    def user_validate(self,username, password):
        user_obj = self.db_query(User).filter_by(name=username).first()
        if not user_obj:
            return
        else:
            user_obj_pass = user_obj.password
            if utils.validate_pass(user_obj_pass,password):
                return True
            else:
                return False