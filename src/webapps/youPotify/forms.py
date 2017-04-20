from django import forms

class PlaylistForm(forms.Form):
    name = forms.CharField(max_length=20, required = True)

class SongForm(forms.Form):
	songId = forms.CharField(max_length=200)
	to = forms.CharField(max_length=200)
	msg = forms.CharField(max_length=250)

class PlaylistIdForm(forms.Form):
	playlistId = forms.IntegerField()

class DeleteSongForm(forms.Form):
	songId = forms.CharField(max_length=200)
	source = forms.CharField(max_length=20)
	sourceId = forms.CharField(max_length=200)

class AddSongForm(forms.Form):
	songId = forms.CharField(max_length=200)
	playlistId = forms.IntegerField()

class SongIdForm(forms.Form):
	songId = forms.CharField(max_length=200)

class RegistrationForm(forms.Form):
    id = forms.CharField(max_length = 20)
    name = forms.CharField(max_length = 20)
    firstName = forms.CharField(max_length = 20)
    lastName = forms.CharField(max_length = 20)
    email = forms.CharField(max_length = 200)
    picture = forms.URLField(max_length = 200)


