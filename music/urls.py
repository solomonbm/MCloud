from django.conf.urls import url
from . import views

app_name = 'music'

urlpatterns = [	
	# /music/
	url(r'^$', views.index, name='index'),
	# /music/register
	url(r'^register/$', views.UserFormView.as_view(), name='register'),
	# /music/login_user
	url(r'^login_user/$', views.login_user, name='login_user'),
	# /music/logout_user
	url(r'^logout/$', views.logout_user, name='logout_user'),
	# /music/<album_id>/
	url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
	# /music/songs/filter_by/
	url(r'^songs/(?P<filter_by>[a-zA_Z]+)/$', views.songs, name='songs'),
	# /music/album/add/
	url(r'album/add/$', views.AlbumCreate.as_view(), name='album-add'),
	# /music/album/pk/
	url(r'album/(?P<pk>[0-9]+)/$', views.AlbumUpdate.as_view(), name='album-update'),
	# /music/album/pk/delete/
	url(r'album/(?P<pk>[0-9]+)/delete/$', views.AlbumDelete.as_view(), name='album-delete'),
	# /music/album_id/favorite_album/
	url(r'^(?P<album_id>[0-9]+)/favorite_album/$', views.favorite_album, name='favorite_album'),
	# /music/album_id/create_song/
	url(r'^(?P<album_id>[0-9]+)/create_song/$', views.create_song, name='create_song'),
	# /music/song_id/favorite_song/
	url(r'^(?P<song_id>[0-9]+)/favorite_song/$', views.favorite_song, name='favorite_song'),
	# /music/song/song_id/delete/
	url(r'song/(?P<song_id>[0-9]+)/delete/$', views.song_delete, name='song-delete'),
]

