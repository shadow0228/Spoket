from django.test import TestCase, Client
from youPotify.models import *


# Create your tests here.


# Models test
# User Model Test
class UserModelsTest(TestCase):
	def test_simple_add(self):
		new_user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
		new_user.save()
		self.assertTrue(User.objects.all().count() == 1)
		self.assertTrue(User.objects.filter(username='john'))



# Profile Model Test
class ProfileModelsTest(TestCase):
	def test_simple_add(self):
		new_user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
		new_user.save()

		profile = Profile(owner=new_user)
		profile.save()
		self.assertTrue(User.objects.all().count() == 1)

	def test_add_friend(self):
		new_user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
		new_user.save()

		new_user2 = User.objects.create_user('jane', 'lennon@thebeatles.com', 'johnpassword')
		new_user2.save()

		profile = Profile(owner=new_user)
		profile.save()
		profile.friends.add(new_user2)
		self.assertTrue(Profile.objects.filter(owner=new_user).count() == 1)
		self.assertTrue(Profile.objects.filter(owner=new_user)[0].friends.filter(username='jane').count() == 1)



# Bucket Model Test
class BucketModelsTest(TestCase):
	def test_simple_add(self):
		bucket = Bucket()
		bucket.save()
		self.assertTrue(Bucket.objects.all().count() == 1)		

	def test_add_user_relation(self):
		new_user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
		new_user.save()

		bucket = Bucket()
		bucket.save()
		bucket.owner.add(new_user)
		self.assertTrue(bucket.owner.filter(username='john').count() == 1)		


# Song Model Test
class PlaylistModelsTest(TestCase):
	def test_simple_add(self):
		new_user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
		new_user.save()

		playlist = PlayList(owner=new_user)
		playlist.save()
		self.assertTrue(PlayList.objects.filter(owner=new_user).count() == 1)



# Song Model Test
class SongModelsTest(TestCase):
	def test_simple_add(self):
		new_user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
		new_user.save()

		song = Song(creater=new_user, receiver=new_user)
		song.save()
		self.assertTrue(Song.objects.all().count() == 1)

	def test_add_playlist(self):
		new_user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
		new_user.save()

		playlist = PlayList(owner=new_user)
		playlist.save()

		song = Song(creater=new_user, receiver=new_user)
		song.save()
		song.playList.add(playlist)

		self.assertTrue(song.playList.all().count() == 1)


	def test_add_bucket(self):
		new_user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
		new_user.save()

		bucket = Bucket()
		bucket.save()

		song = Song(creater=new_user, receiver=new_user, bucket=bucket)
		song.save()

		self.assertTrue(song.bucket.id == bucket.id)




# Client test

class ClientTest(TestCase):

	def test_login_page(self):   
		client = Client()	   
		response = client.get('/login')
		self.assertEqual(response.status_code, 200)

	def test_home_page(self):   
		client = Client()	   
		response = client.get('/search')
		self.assertEqual(response.status_code, 302)

	def test_home_page_with_login(self):   
		# client = Client()	   
		self.user = User.objects.create_user(username='testuser', password='12345') 
		self.user.save() 

		profile = Profile(owner=self.user)
		profile.save()

		login = self.client.login(username='testuser', password='12345')

		response = self.client.get('/search')
		self.assertEqual(response.status_code, 200)



# class AjaxTest(TestCase):
	def test_addNewSong(request):
		pass


	def test_deleteSongFromLibrary(request):
		pass


	def test_deletePlaylist(request):
		pass


	def test_unpublicPlaylist(request):
		pass


	def test_publicPlaylist(request):
		pass


	def test_deleteSong(request):
		pass


	def test_sendSong(request):
		pass


	def test_createPlaylist(request):
		pass


	def test_getPlaylists(request):
		pass


	def test_pickSongToPlaylist(request):
		pass


	def test_getSongMessage(request):
		pass


	 # def test_add_student(self):	# Tests the to-do list add-item function.
		#  client = Client()	   # add-item expects a POST request with one
		# 						 # query parameter, item, the text of the to-do
		# 						 # list item.
		#  sample_item = 'This is the text for my sample todo list item'
		#  response = client.post('/shared-todo-list/add-item', {'item':sample_item})
		#  self.assertTrue(response.content.find(sample_item.encode()) >= 0)