# dockerit
a docker management system based on python
实现对docker进行基本的管理，包括node, container, image等。采用了tornado框架。

* Dashboard  
  用来展示容器，镜像等数据统计信息
* 节点管理
  实现对节点的管理，包括节点的新增、修改、查看，刷新、删除。
* 容器管理
  实现对节点上容器的管理，包括容器的查看，启动，停止和删除。
* 镜像管理
  实现对节点上docker镜像的管理，包括build镜像，export/tag/删除镜像。
* 事件管理
  实现对重要操作event进行查询
  
* summary
  容器相关的操作都可扩展，需要使用docker RemoteAPI
  事件管理作为查询管理的一部分，后期可增加更多查询条件
  用户/权限的管理后期可添加扩展

## 展示
* Dashboard

![image](https://github.com/CHUNL09/dockerit/blob/master/show_pics/login.png)
![image](https://github.com/CHUNL09/dockerit/blob/master/show_pics/dashboard.png)

* 节点管理

![image](https://github.com/CHUNL09/dockerit/blob/master/show_pics/node_mgt.png)
![image](https://github.com/CHUNL09/dockerit/blob/master/show_pics/view_node.png)

* 容器管理

![image](https://github.com/CHUNL09/dockerit/blob/master/show_pics/container_mgt.png)

* 镜像管理

![image](https://github.com/CHUNL09/dockerit/blob/master/show_pics/image_mgt.png)

* 事件管理

![image](https://github.com/CHUNL09/dockerit/blob/master/show_pics/event_mgt.png)
