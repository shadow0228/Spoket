from __future__ import unicode_literals
from django.db import models
import datetime 
import os
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.
# Data model for Youpotify


class Profile(models.Model):
	owner = models.OneToOneField(User)
	image = models.CharField(max_length=250)
	friends = models.ManyToManyField(User, related_name='friends')
	def __unicode__(self):
		return str(self.owner)


class Bucket(models.Model):
	owner = models.ManyToManyField(User, related_name='owned_bucket')

	def __unicode__(self):
		return str(self.id)


class PlayList(models.Model):
	owner = models.ForeignKey(User, on_delete=models.CASCADE)
	name = models.CharField(max_length=250)
	public = models.BooleanField(default=True)

	def __unicode__(self):
		return str(self.name)


class Song(models.Model):
	spotifyId = models.CharField(max_length=50)
	bucket = models.ForeignKey(Bucket, on_delete=models.CASCADE, blank=True, null=True)
	playList = models.ManyToManyField(PlayList, related_name='owned_by', blank=True)
	creater = models.ForeignKey(User, on_delete=models.CASCADE, related_name='songCreater')
	receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="songReceiver")
	text = models.CharField(max_length=250)
	create_date = models.DateField(blank=True, default=datetime.datetime.now)
	create_time = models.TimeField(blank=True, default=datetime.datetime.now)

	def __unicode__(self):
		return str(self.id)

