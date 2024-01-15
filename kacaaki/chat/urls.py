from django.urls import path,re_path
from .views import *



app_name = 'chat'


urlpatterns = [
    re_path(r'^room/$',ChatRoomListView.as_view(),name='chat-room'),
    re_path(r'^room/(?P<pk>\d+)/$',chat_with_id,name='chat-with-id'),
    re_path(r'^user/(?P<pk>\d+)/$', ChatRoomView.as_view(), name='chatting-room'),
    re_path(r'^load-more-messages/$', load_more_messages, name='load-more-messages'),
    re_path(r'^user-search/$', user_search, name='live-user-search'),
    re_path(r'^room-get-create/$', room_get_create, name='room-get-create'),
    re_path(r'^room/detail/(?P<pk>\d+)/$', room_detail, name='room-detail'),
    
]