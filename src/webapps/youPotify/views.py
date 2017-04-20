from django.shortcuts import render, redirect
from django.db import transaction
from django.template import loader, RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.models import User
from youPotify.models import *
from django.contrib.auth import login as auth_login, authenticate, logout
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core import serializers
from .models import *
from django.conf import settings
from django.shortcuts import render_to_response
from .forms import *

import os
import requests
import spotipy
import json
import hashlib

# Create your views here.

###########################
# views
###########################

def debug_404(request):
	context = {}
	return render(request, '404.html', context)

def page_not_found(request):
	response = render_to_response('404.html', context_instance=RequestContext(request))
	response.status_code = 404
	return response


@transaction.atomic
def login(request):

	if request.user.is_authenticated():
		return HttpResponseRedirect("/")
	
	context = {}
	return render(request, 'youPotify/index.html', context)


@login_required
@transaction.atomic
def search(request):

	if 'term' in request.GET:
		search_term = request.GET['term']
	else:
		search_term = ''

	friends = request.user.profile.friends.all()
	playlists = PlayList.objects.filter(owner=request.user)


	context = {
		'search_term': search_term,
		'user': request.user,
		'friends': friends,
		'playlists': playlists,
	}
	return render(request, 'youPotify/search.html', context)


@login_required
@transaction.atomic
def getUser(request):
	context = {'user': request.user.first_name}
	return HttpResponse(json.dumps(context), content_type="application/json")


@login_required
@transaction.atomic
def playlist(request, id):

	try:
		playlist = PlayList.objects.get(id=id)
	except PlayList.DoesNotExist:
		raise Http404

	# get buckets owned by user (for now we assume there is only one bucket)
	bucket = request.user.owned_bucket.all()[0]

	# get songs in the bucket
	songs = Song.objects.filter(playList=playlist)

	tracks = []

	# get spotify info
	for song in songs:

		url = 'https://api.spotify.com/v1/tracks/' + song.spotifyId

		sp = spotipy.Spotify()
		urn = 'spotify:track:' + song.spotifyId
		track = sp.track(urn)

		track['d_id'] = song.id
		track['user'] = request.user
		track['artist'] = track['artists'][0]['name']
		track['songId'] = song.spotifyId

		if song.creater != song.receiver:
			track['sender'] = song.creater
			track['msg'] = song.text

		duration = track['duration_ms']

		x = duration / 1000
		seconds = x % 60
		x /= 60
		minutes = x % 60
		track['duration'] = str(minutes) + ":" + str(seconds)

		tracks.append(track)

	# playlists = PlayList.objects.all()
	playlists = PlayList.objects.filter(owner=request.user)

	playlistForm = PlaylistForm()


	context = {
		'user': request.user,
		'bucket': bucket,
		'tracks': tracks,
		'playlists': playlists,
		'playlist': playlist,
	}
	return render(request, 'youPotify/playlist.html', context)
	# return render(request, 'youPotify/playlist.html', context)


@login_required
@transaction.atomic
def bucket(request):

	friends = request.user.profile.friends.all()

	# get buckets owned by user (for now we assume there is only one bucket)
	bucket = request.user.owned_bucket.all()[0]

	# get songs in the bucket
	songs = bucket.song_set.all()

	tracks = []

	# get spotify info
	for song in songs:

		url = 'https://api.spotify.com/v1/tracks/' + song.spotifyId

		sp = spotipy.Spotify()
		urn = 'spotify:track:' + song.spotifyId
		track = sp.track(urn)

		track['d_id'] = song.id
		track['user'] = request.user
		track['artist'] = track['artists'][0]['name']
		track['songId'] = song.spotifyId

		if song.creater != song.receiver:
			track['sender'] = song.creater
			track['msg'] = song.text

		duration = track['duration_ms']

		x = duration / 1000
		seconds = x % 60
		x /= 60
		minutes = x % 60
		track['duration'] = str(minutes) + ":" + str(seconds)

		tracks.append(track)


	playlists = PlayList.objects.filter(owner=request.user)

	context = {
		'user': request.user,
		'bucket': bucket,
		'tracks': tracks,
		'playlists': playlists,
	}
	return render(request, 'youPotify/bucket.html', context)


@login_required
@transaction.atomic
def friends(request):

	playlists = PlayList.objects.filter(owner=request.user)

	friends = request.user.profile.friends.all()

	friendList = []

	for friend in friends:
		friendList.append({
			'person': friend,
		})

	context = {
		'user': request.user,
		'playlists': playlists,
		'friends': friendList,
	}

	return render(request, 'youPotify/friends.html', context)

@login_required
@transaction.atomic
def friend(request, friendId):

	try:
		friend = User.objects.get(id=friendId)
		isExist = request.user.profile.friends.filter(id=friendId)

		playlists = PlayList.objects.filter(owner=request.user)

		songs = Song.objects.filter(Q(creater=request.user, receiver=friend) | Q(creater=friend, receiver=request.user)).order_by('create_time')

	 
		tracks = []

		# get spotify info
		for song in songs:

			url = 'https://api.spotify.com/v1/tracks/' + song.spotifyId

			sp = spotipy.Spotify()
			urn = 'spotify:track:' + song.spotifyId
			track = sp.track(urn)

			track['d_id'] = song.id
			track['user'] = request.user
			track['artist'] = track['artists'][0]['name']
			track['songId'] = song.spotifyId

			track['sender'] = song.creater
			track['msg'] = song.text

			track['owned'] = (song.creater != request.user)

			duration = track['duration_ms']

			x = duration / 1000
			seconds = x % 60
			x /= 60
			minutes = x % 60
			track['duration'] = str(minutes) + ":" + str(seconds)

			tracks.append(track)

		friendPlaylists = PlayList.objects.filter(owner=friend, public=True)

		context = {
			'friendPlaylists': friendPlaylists,
			'tracks': tracks,
			'user': request.user,
			'playlists': playlists,
			'friend': friend,
		}
		return render(request, 'youPotify/friend.html', context)

	except:
		response = render_to_response('404.html', context_instance=RequestContext(request))
		response.status_code = 404
		return response

	


@login_required
@transaction.atomic
def library(request):

	# get songs owned by a user
	songs = Song.objects.filter(receiver=request.user)

	tracks = []

	# get spotify info
	for song in songs:

		url = 'https://api.spotify.com/v1/tracks/' + song.spotifyId

		sp = spotipy.Spotify()
		urn = 'spotify:track:' + song.spotifyId
		track = sp.track(urn)

		track['d_id'] = song.id
		track['user'] = request.user
		track['artist'] = track['artists'][0]['name']
		track['songId'] = song.spotifyId

		if song.creater != song.receiver:
			track['sender'] = song.creater
			track['msg'] = song.text

		duration = track['duration_ms']

		x = duration / 1000
		seconds = x % 60
		x /= 60
		minutes = x % 60
		track['duration'] = str(minutes) + ":" + str(seconds)

		tracks.append(track)


	playlists = PlayList.objects.filter(owner=request.user)

	context = {
		'user': request.user,
		'tracks': tracks,
		'playlists': playlists,
	}
	return render(request, 'youPotify/library.html', context)




########################
# ajax actions 
########################

########################
# actions for bucket
########################

# pick song from search and add to self library and playlist
@login_required
@transaction.atomic
def addNewSong(request):
	form = AddSongForm(request.POST)
	if form.is_valid():
		songSpotifyId = request.POST['songId']
		playlistId = request.POST['playlistId']

		playlist = PlayList.objects.get(id=playlistId)

		song = Song(
			spotifyId = songSpotifyId,
			creater = request.user,
			receiver = request.user,
		)	

		song.save()
		song.playList.add(playlist)
	return HttpResponse('')


@login_required
@transaction.atomic
def deleteSongFromLibrary(request):
	form = DeleteSongForm(request.POST)
	if form.is_valid():
		# first check if the user actually own this song
		songId = request.POST['songId']
		song = Song.objects.get(id=songId)

		if song.receiver == request.user:
			song.delete()
			return HttpResponse('')
		else:
			return HttpResponse('Invalid operation!')
	return HttpResponse('')

@login_required
@transaction.atomic
def deletePlaylist(request):
	form = PlaylistIdForm(request.POST)
	if form.is_valid():
		playlistId = request.POST['playlistId']
		playlist = PlayList.objects.get(id=playlistId)

		# first check if the user actually own this song
		if playlist.owner == request.user:
			playlist.delete()
			return HttpResponse('')
		else:
			return HttpResponse('Invalid operation!')
	return HttpResponse('')


@login_required
@transaction.atomic
def unpublicPlaylist(request):
	form = PlaylistIdForm(request.POST)
	if form.is_valid():
		playlistId = request.POST['playlistId']
		playlist = PlayList.objects.get(id=playlistId)
		playlist.public = False
		playlist.save()

	return HttpResponse('')


@login_required
@transaction.atomic
def publicPlaylist(request):
	form = PlaylistIdForm(request.POST)
	if form.is_valid():
		playlistId = request.POST['playlistId']
		playlist = PlayList.objects.get(id=playlistId)
		playlist.public = True
		playlist.save()

	return HttpResponse('')


@login_required
@transaction.atomic
def deleteSong(request):
	form = DeleteSongForm(request.POST)
	if form.is_valid():

		songId = request.POST['songId']
		source = request.POST['source']
		sourceId = request.POST['sourceId']

		if source == 'playlist':
			playlist = PlayList.objects.get(id=sourceId)
			song = Song.objects.get(id=songId)
			song.playList.remove(playlist)
			song.save()
		elif source == 'bucket':
			song = Song.objects.get(id=songId)
			song.bucket = None
			song.save()

	return HttpResponse('')


# pick song from search and send to friends' bucket
@login_required
@transaction.atomic
def sendSong(request):
	form = SongForm(request.POST)
	if form.is_valid():
		songId = request.POST['songId']
		to = request.POST['to']
		msg = request.POST['msg'] 

		receiver = User.objects.get(id=to)
		bucket = receiver.owned_bucket.all()[0]

		song = Song(
			spotifyId = songId,
			bucket = bucket,
			creater = request.user,
			receiver = receiver,
			text = msg
		)
		song.save()
		context = {
			'receiver' : receiver.first_name,
			'message' : msg,
			'sender' : request.user.first_name,
			'sondId': sondId
		}
		return HttpResponse(json.dumps(context), content_type="application/json")

	return HttpResponse('')



# action for playlist
@login_required
@transaction.atomic
def createPlaylist(request):
	form = PlaylistForm(request.POST)
	if form.is_valid():
		playlist = PlayList(
			owner = request.user,
			name = request.POST['name']
		)
		playlist.save()
	context = {
		'playlistId': playlist.id
	}
	return HttpResponse(json.dumps(context), content_type="application/json")


@login_required
@transaction.atomic
def getPlaylists(request):
	playlists = PlayList.objects.filter(owner=request.user)
	context = {
		'playlists': playlists,
	}

	return HttpResponse(serializers.serialize("json", playlists), content_type="application/json")



# pick song from bucket and add to playlist
@login_required
@transaction.atomic
def pickSongToPlaylist(request):

	form = AddSongForm(request.POST)
	if form.is_valid():
		songId = request.POST['songId']
		playlistId = request.POST['playlistId']

		song = Song.objects.get(id=songId)
		playlist = PlayList.objects.get(owner=song.receiver, id=playlistId)

		cnt = Song.objects.filter(id=songId, playList__in=[playlist]).distinct().count()

		if cnt > 0:
			context = {'code': 'duplicate'}
			return HttpResponse(json.dumps(context), content_type="application/json")

		else:
			song.playList.add(playlist)
			context = {'code': 'success', 'id':song.id}
			return HttpResponse(json.dumps(context), content_type="application/json")

	return HttpResponse('')


@login_required
@transaction.atomic
def getSongMessage(request):
	form = SongIdForm(request.POST)
	if form.is_valid():
		songId = request.POST['songId']
		song = Song.objects.get(spotifyId=songId)
		context = {}
		context['creater'] = song.creater.username
		context['text'] = song.text
		return HttpResponse(json.dumps(context), content_type="application/json")
	return HttpResponse('')


@transaction.atomic
def addUser(request):
	context = {}
	form = RegistrationForm(request.POST)
	if form.is_valid():
		userId = request.POST['id']
		username = request.POST['name']
		userEmail = request.POST['email']
		firstName = request.POST['firstName']
		lastName = request.POST['lastName']
		picture = request.POST['picture']
		friends = request.POST.getlist('friends[]')
		file = open(os.path.join(settings.BASE_DIR, 'salt.txt'))
		salt = file.read()
		file.close()
		userPassword = hashlib.sha256(userId + salt).hexdigest()


		if len(User.objects.filter(username = userId)) == 0:


			new_user = User.objects.create_user(username=userId, \
											password=userPassword, \
											first_name=firstName, \
											last_name=lastName, \
											email=userEmail )
			new_user.save()

			# create profile for the new user
			new_user_profile = Profile(owner=new_user, image=picture)
			new_user_profile.save()

			# create bucket for the new user
			bucket = Bucket()
			bucket.save()
			bucket.owner.add(new_user)

		user = User.objects.get(username=userId)

		new_user_profile = Profile.objects.get(owner = user)

		# update user profile pic url

		new_user_profile.image = picture
		new_user_profile.save()

		# update friend list
		for a in friends:
			if len(User.objects.filter(username = a)) > 0:
				user = User.objects.get(username = a)
				new_user_profile.friends.add(user)
				new_user_profile.save()

		user = authenticate(username=userId, password=userPassword)
		
		auth_login(request, user)


	return HttpResponse("")


