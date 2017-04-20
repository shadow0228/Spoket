from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import login, logout_then_login

from django.conf.urls import (
	handler400, handler403, handler404, handler500
)

import youPotify.views

urlpatterns = [
    url(r'^$', youPotify.views.library, name='index'),
	url(r'^login', youPotify.views.login, name='login'),
    url(r'^logout', logout_then_login, name='logout'),

	url(r'^bucket', youPotify.views.bucket, name='bucket'),
	url(r'^playlist/(?P<id>\d+)$', youPotify.views.playlist, name='playlist'),
	url(r'^search', youPotify.views.search, name='search'),
	url(r'^library', youPotify.views.library, name='library'),
	url(r'^friends', youPotify.views.friends, name='friends'),
	url(r'^friend/(?P<friendId>\d+)$', youPotify.views.friend, name='friend'),
	url(r'^getUser', youPotify.views.getUser, name='getUser'),

	# action
	url(r'^add_new_song', youPotify.views.addNewSong, name='addNewSong'),
	url(r'^delete_song', youPotify.views.deleteSong, name='deleteSong'),
	url(r'^delete_playlist', youPotify.views.deletePlaylist, name='deletePlaylist'),
	url(r'^unpublic_playlist', youPotify.views.unpublicPlaylist, name='unpublicPlaylist'),
	url(r'^public_playlist', youPotify.views.publicPlaylist, name='publicPlaylist'),
	url(r'^send_song', youPotify.views.sendSong, name='sendSong'),
	url(r'^delete_from_library', youPotify.views.deleteSongFromLibrary, name='deleteSongFromLibrary'),
	url(r'^create_playlist', youPotify.views.createPlaylist, name='createPlaylist'),
	url(r'^pick_song_to_playlist', youPotify.views.pickSongToPlaylist, name='pickSongToPlaylist'),
	url(r'^get_song_message', youPotify.views.getSongMessage, name='getSongMessage'), 
	url(r'^get_playlists', youPotify.views.getPlaylists, name='getPlaylists'), 

	url(r'^add_user', youPotify.views.addUser, name='addUser'),

	url(r'^404', youPotify.views.debug_404, name='debug_404'),

	]

