from django.urls import path,re_path
from .views import *



app_name = 'chat'


urlpatterns = [
    re_path(r'^room/list/$',ChatRoomListView.as_view(),name='chatroom-list'),
    re_path(r'^user/(?P<pk>\d+)/$', ChatRoomView.as_view(), name='chatting-room'),
    re_path(r'^load-more-messages/$', load_more_messages, name='load-more-messages'),
]