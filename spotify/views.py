
from django.shortcuts import render, redirect
# Create your views here.
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
 
from spotify.models import Song, PlaylistSong
from spotify.forms import PlaylistSongForm
from spotify.utils import searchSongs

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
        return self.render_to_response(context)

class SongDetail(DetailView):
    model = Song
    template_name = 'spotify/single-song.html'
    context_object_name = 'song'   

    def get_context_data(self, **kwargs):
        context = super(SongDetail, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['user_list']= PlaylistSong.objects.filter(user=self.request.user)
            context['list_albyms']=  PlaylistSong.objects.filter(user=self.request.user).filter(songs = self.get_object())
            print(context['list_albyms'])  
        context['form'] = PlaylistSongForm()
        return context 
    
    def post(self, request, *args, **kwargs): 
        self.object = self.get_object()
        print()
        context = self.get_context_data(object=self.object)
        list_title= request.POST['list_title']
        if request.user.is_authenticated:
            list_title=request.POST['list_title']            
            try:
                list_song_user= PlaylistSong.objects.get(user=request.user, list_title=list_title)
                print(list_song_user)
                list_song_user.songs.add(self.object)            
            except PlaylistSong.DoesNotExist:                
                form = PlaylistSongForm(request.POST)
                listSong = form.save(commit=False)
                listSong.user= request.user
                listSong.save()
                listSong.songs.add(self.object)
        return self.render_to_response(context)
 
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
    def post(self, request, *args, **kwargs): 
        self.object = self.get_object()
        print(self.object)
        

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



class CustomLoginView(LoginView):
    template_name = 'spotify/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('songs')


class RegisterPage(FormView):
    template_name = 'spotify/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('songs')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)