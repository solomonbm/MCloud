from django.views.generic import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.views import generic
from django.db.models import Q
from django.views.generic import View
from .models import Album, Song
from .forms import UserForm, AlbumForm, SongForm
from django.http import HttpResponseRedirect

AUDIO_FILE_TYPES = ['wav', 'mp3', 'ogg']
IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']

def index(request):
	if not request.user.is_authenticated():
		return render(request, 'music/login.html')
	else:
		albums = Album.objects.filter(user=request.user)
		song_results = Song.objects.all()
		query = request.GET.get("q")
		if query:
			albums = albums.filter(
				Q(album_title__icontains=query) |
				Q(artist__icontains=query)
			).distinct()
			song_results = song_results.filter(
				Q(song_title__icontains=query)
			).distinct()
			return render(request, 'music/index.html', {'albums': albums, 'songs': song_results})
		else:
			return render(request, 'music/index.html', {'albums': albums})

class DetailView(generic.DetailView):
	model = Album
	template_name = 'music/detail.html'
	
class AlbumCreate(CreateView):
	model = Album
	fields = ['artist', 'album_title', 'genre', 'album_logo']
	
	def post(self, request):
		if not request.user.is_authenticated():
			return render(request, 'music/login.html')
		else:
			form = AlbumForm(request.POST or None, request.FILES or None)
			if form.is_valid():
				album = form.save(commit=False)
				album.user = request.user
				album.album_logo = request.FILES['album_logo']
				file_type = album.album_logo.url.split('.')[-1]
				file_type = file_type.lower()
				if file_type not in IMAGE_FILE_TYPES:					
					return render(request, 'music/create_album.html', {'album': album, 'form': form, 'error_message': 'Image file must be PNG, JPG, or JPEG'})
				album.save()
				return render(request, 'music/detail.html', {'album': album})
			
			return render(request, 'music/create_album.html', {"form": form})
	
class AlbumUpdate(UpdateView):
	model = Album
	fields = ['artist', 'album_title', 'genre', 'album_logo']

class AlbumDelete(DeleteView):	
	model = Album
	success_url = reverse_lazy('music:index')
	
	def post(self, request, *args, **kwargs):
		if "cancel" in request.POST:
			return HttpResponseRedirect(self.success_url)
		else:
			return super(AlbumDelete, self).post(request, *args, **kwargs)

class UserFormView(View):
	form_class = UserForm
	template_name = 'music/registration_form.html'
	
	# display blank form
	def get(self, request):
		form = self.form_class(None)
		return render(request, self.template_name, {'form': form})
	
	# process form data
	def post(self, request):
		form = self.form_class(request.POST)
		
		if form.is_valid():
			
			user = form.save(commit=False)
			
			# cleaned (normalized) data
			user_name = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user.set_password(password)
			user.save()
			
			# returns User objects if credentials are correct
			user = authenticate(username=user_name, password=password)
			
			if user is not None:
				
				if user.is_active:
					login(request, user)
					return redirect('music:index')
					
		return render(request, self.template_name, {'form': form})

def favorite_album(request, album_id):
	album = get_object_or_404(Album, pk=album_id)
	if album.is_favorite:
		album.is_favorite = False
	else:
		album.is_favorite = True

	album.save()
	return redirect('music:index')


def logout_user(request):
	logout(request)
	
	form = UserForm(request.POST or None)
	
	return render(request, 'music/login.html', {"form": form})
	
def login_user(request):
	if request.method == "POST":		
		user_name = request.POST['username']		
		password = request.POST['password']		
		user = authenticate(username=user_name, password=password)							
		if user is not None:
			if user.is_active:
				login(request, user)
				albums = Album.objects.filter(user=request.user)
				return render(request, 'music/index.html', {'albums': albums})
			else:				
				return render(request, 'music/login.html', {'error_message': 'Your account has been disabled'})
		else:
			return render(request, 'music/login.html', {'error_message': 'Invalid login'})
	
	return render(request, 'music/login.html')	

def create_song(request, album_id):
	form = SongForm(request.POST or None, request.FILES or None)
	album = get_object_or_404(Album, pk=album_id)
	if form.is_valid():
		albums_songs = album.song_set.all()
		for s in albums_songs:
			if s.song_title == form.cleaned_data.get("song_title"):
				context = {	
							'album': album,
							'form': form,
							'error_message': "You've already added that song",
						}
				return render(request, 'music/create_song.html', context)
		song = form.save(commit=False)
		song.album = album
		song.audio_file = request.FILES['audio_file']
		file_type = song.audio_file.url.split('.')[-1]
		file_type = file_type.lower()
		if file_type not in AUDIO_FILE_TYPES:		
			context = {
						'album': album,
						'form': form,
						'error_message': 'Audio file must be WAV, MP3, or OGG',
					}
			return render(request, 'music/create_song.html', context)
		song.save()
		return render(request, 'music/detail.html', {'album': album})
		
	context = {
				'album': album,
				'form': form,
			}
	return render(request, 'music/create_song.html', context)

def favorite_song(request, song_id):
	song = get_object_or_404(Song, pk=song_id)
	if song.is_favorite:
		song.is_favorite = False
	else:
		song.is_favorite = True

	song.save()
	album = song.album
	
	return render(request, 'music/detail.html', {'album': album})

def song_delete(request, song_id, template_name='music/song_confirm_delete.html'):
	song= get_object_or_404(Song, pk=song_id)
	album = song.album
	if request.method=='POST':
		song.delete()
		return render(request, 'music/detail.html', {'album': album})
	ctx = {}
	ctx["song"] = song
	return render(request, template_name, ctx)
	
def songs(request, filter_by):
	if not request.user.is_authenticated():
		return render(request, 'music/login.html')
	else:
		try:
			song_ids = []
			for album in Album.objects.filter(user=request.user):
				for song in album.song_set.all():
					song_ids.append(song.pk)
			users_songs = Song.objects.filter(pk__in=song_ids)
			query = request.GET.get("q")
			if query:
				users_songs = users_songs.filter(Q(song_title__icontains=query)).distinct()
			if filter_by == 'favorites':
				users_songs = users_songs.filter(is_favorite=True)
		except Album.DoesNotExist:
			users_songs = []
		return render(request, 'music/songs.html', {
			'song_list': users_songs,
			'filter_by': filter_by,
		})	
