from django.contrib import admin
from .models import *

admin.site.register(Profile)
admin.site.register(Bucket)
admin.site.register(PlayList)
admin.site.register(Song)