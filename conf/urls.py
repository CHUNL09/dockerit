from handler.user import Login
from handler.node import NodeInfo
from handler.node import NodeCRUD
from handler.mgt import Event,EventSearch
from handler.dockercore import DashBoardInfo,ContainerAPI,ImageAPI
from handler.container import ContainerList
from handler.image import ImageList
url = [
    (r'/',  Login),
    (r'/login',  Login),
    (r'/dashboard',  DashBoardInfo),
    (r'/nodeinfo',  NodeInfo),
    (r'/nodecrud',  NodeCRUD),
    (r'/containerinfo',  ContainerList),
    (r'/api/con',  ContainerAPI),
    (r'/imageinfo',  ImageList),
    (r'/api/image',  ImageAPI),
    (r'/mgt/event',  Event),
    (r'/mgt/event/search',  EventSearch),

]