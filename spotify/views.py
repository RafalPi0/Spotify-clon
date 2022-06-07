
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
 
from spotify.models import Song, PlaylistSong
from .forms import PlaylistSongForm
from .utils import searchSongs


from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


class SongList(ListView):
    model = Song
    template_name = 'spotify/home.html'
    context_object_name = 'songs'
    paginate_by = 5
    ordering = ['-create']
    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        songs, search_query = searchSongs(request)
        context['songs']=songs
        context['search_query']=search_query   
        allow_empty = self.get_allow_empty()
        if not allow_empty:
        # When pagination is enabled and object_list is a queryset,
        # it's better to do a cheap query than to load the unpaginated
        # queryset in memory.
            if self.get_paginate_by(self.object_list) is not None and hasattr(self.object_list, 'exists'):
                is_empty = not self.object_list.exists()
            else:
                is_empty = not self.object_list
            if is_empty:
                raise Http404(_('Empty list and “%(class_name)s.allow_empty” is False.') % {
                    'class_name': self.__class__.__name__,
                })     
        return self.render_to_response(context)

class SongDetail(DetailView):
    model = Song
    template_name = 'spotify/single-song.html'
    context_object_name = 'song'   
    def get_context_data(self, **kwargs):
        context = super(SongDetail, self).get_context_data(**kwargs)
        context['user_list']= PlaylistSong.objects.filter(user=self.request.user)
        context['form'] = PlaylistSongForm()
        return context 
    
    def post(self, request, *args, **kwargs): 
        self.object = self.get_object()
        print()
        context = self.get_context_data(object=self.object)
        list_title= request.POST['list_title']
        if request.user.is_authenticated:
            list_title=request.POST['list_title']
            # list_song_user= PlaylistSong.objects.filter(user=request.user).filter(list_title=list_title)
            try:
                list_song_user= PlaylistSong.objects.get(user=request.user, list_title=list_title)
                print(list_song_user)
                list_song_user.songs.add(self.object)
            # list_title
            except PlaylistSong.DoesNotExist:                
                form = PlaylistSongForm(request.POST)
                listSong = form.save(commit=False)
                listSong.user= request.user
                listSong.save()
                listSong.songs.add(self.object)
        return self.render_to_response(context)
	

def index(request):
    songs, search_query = searchSongs(request)
    custom_range, songs = paginateSongs(request, songs, 6)
    print(songs)
    context = {'songs': songs,
               'search_query': search_query, 'custom_range': custom_range}
    # songs = Song.objects.all()
    # context = { 'songs': songs}    
    return render(request , 'spotify/home.html' ,context)


def song(request, pk):
    songObj = Song.objects.get(id=pk)    
    user_list= PlaylistSong.objects.filter(user=request.user)
    form = PlaylistSongForm()    
    if request.method == 'POST':
        if request.user.is_authenticated:
            list_title=request.POST['list_title']
            
            try:
                list_song_user= PlaylistSong.objects.get(user=request.user, list_title=list_title)
                print(list_song_user)
                list_song_user.songs.add(songObj)
            # list_title
            except PlaylistSong.DoesNotExist:                
                form = PlaylistSongForm(request.POST)
                listSong = form.save(commit=False)
                listSong.user= request.user
                listSong.save()
            # review = form.save(commit=False)
            # print(request.POST)
            
        
    return render(request, 'spotify/single-song.html', {'song': songObj,'form': form
    })

class PlaylistSongList(LoginRequiredMixin, ListView):
    model = PlaylistSong
    context_object_name = 'playlists'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['playlists'] = context['playlists'].filter(user=self.request.user)  
        return context

class PlaylistSongDetail(LoginRequiredMixin, DetailView):
    model = PlaylistSong
    context_object_name = 'playlist'
    template_name = 'spotify/playlist_detail.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        context['songs'] = self.object.songs.all()
        return context

class PlaylistSongCreate(LoginRequiredMixin, CreateView):
    model = PlaylistSong
    fields = ["list_title"]
    success_url = reverse_lazy('playlists')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(PlaylistSongCreate, self).form_valid(form)

class PlaylistSongUpdate(LoginRequiredMixin, UpdateView):
    model = PlaylistSong
    fields = ["list_title" , ]
    success_url = reverse_lazy('playlists')


class PlaylistSongDeleteView(LoginRequiredMixin, DeleteView):
    model = PlaylistSong
    context_object_name = 'playlist'
    success_url = reverse_lazy('playlists')
    def get_queryset(self):
        owner = self.request.user
        return self.model.objects.filter(user=owner)

