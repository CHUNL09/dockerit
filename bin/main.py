import tornado.web
import tornado.ioloop
import tornado.options
import tornado.httpserver
from conf import urls
import os,sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from tornado.options import define,options,parse_command_line
define('port',default=8888,type=int,help="run on this port")

class MyApplication(tornado.web.Application):
    def __init__(self):
        handlers = urls.url
        settings = {
            'template_path': os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates"),
            'static_path': os.path.join(os.path.dirname(os.path.dirname(__file__)), "statics"),
            'login_url': "/login",
            'cookie_secret': "235lksjfASKJFlks=jdfGLKS=JDFLKSsfjlk234dsjflksdjffj/=sf",
        }
        super(MyApplication,self).__init__(handlers,**settings)

if __name__ == '__main__':
    parse_command_line()
    http_server = tornado.httpserver.HTTPServer(MyApplication())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()