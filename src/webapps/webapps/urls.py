from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import login, logout_then_login
import settings
from django.conf.urls.static import static

urlpatterns = [
	url(r'^', include('youPotify.urls')),
	url(r'^admin', admin.site.urls),
]
