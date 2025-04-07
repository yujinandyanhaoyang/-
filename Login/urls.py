"""
URL configuration for 研友集 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from Login.api import login, task
from Login.api.group import create_group, join_group, discussions, get_member, add_discussion
from Login.api.resource import upload, get_resource_detail, likes,addcomments


urlpatterns = [
    # 添加登录路由
    path('api/register/', login.register),
    path('api/login/', login.signin),
    path('api/user/', login.listusermassage),

    #添加学习资料的路由
    path('api/resources/upload/', upload),
    path('api/resources/getmsg/', get_resource_detail),
    path('api/resources/addcomments/', addcomments),
    path('api/resources/like/', likes),

    # 添加学习小组的路由
    path('api/groups/addgroup/', create_group),
    path('api/groups/members/', get_member),
    path('api/groups/join/', join_group),
    path('api/groups/discussions/', discussions),
    path('api/groups/add_discussion/', add_discussion),

    #添加学习任务路由
    path('api/tasks/person/addtask/',task.personlTask),
    path('api/tasks/person/listTask/',task.listTask),
    path('api/tasks/person/update/',task.updatestatus),

]
