from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import Permission, User
from django.conf import settings

def content_file_name(instance, filename):
	return '/'.join([instance.user.username, filename])
	
class Album(models.Model):
	user = models.ForeignKey(User, default=1)
	artist = models.CharField(max_length=250)
	album_title = models.CharField(max_length=500)
	genre = models.CharField(max_length=100)
	album_logo = models.FileField(upload_to=content_file_name, default='default.jpg')
	is_favorite = models.BooleanField(default=False)

	def __str__(self):
		return self.album_title + ' - ' + self.artist
	
	def get_absolute_url(self):
		return reverse('music:detail', kwargs={'pk' : self.pk})

class Song(models.Model):
	album = models.ForeignKey(Album, on_delete=models.CASCADE)
	song_title = models.CharField(max_length=250)
	audio_file = models.FileField(default='', blank=True)
	is_favorite = models.BooleanField(default=False)

	def	__str__(self):
		return self.song_title

	def get_absolute_url(self):
		return reverse('music:detail', kwargs={'pk' : self.pk})