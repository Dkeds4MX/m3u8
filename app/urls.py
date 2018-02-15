from django.urls import path

from app import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('add/', views.CreatePlaylist.as_view(), name='create-playlist'),
    path('channel/<int:pk>/', views.ChannelUpdate.as_view(), name='channel'),
    path('channel/new/', views.ChannelCreate.as_view(), name='new-channel'),
    path('channels', views.ChannelList.as_view(), name='channels'),
    path('public/<slug:public_key>.m3u8', views.public_playlist, name='playlist-public'),
]
