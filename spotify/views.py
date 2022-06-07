
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
 
from spotify.models import Song, PlaylistSong
from .forms import PlaylistSongForm
from .utils import searchSongs


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
    # print(form)
    if request.method == 'POST':
        if request.user.is_authenticated:
            list_title=request.POST['list_title']
            # list_song_user= PlaylistSong.objects.filter(user=request.user).filter(list_title=list_title)
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


# def project(request, pk):
#     projectObj = Project.objects.get(id=pk)
#     form = ReviewForm()

#     if request.method == 'POST':
#         form = ReviewForm(request.POST)
#         review = form.save(commit=False)
#         review.project = projectObj
#         review.owner = request.user.profile
#         review.save()

#         projectObj.getVoteCount

#         messages.success(request, 'Your review was successfully submitted!')
#         return redirect('project', pk=projectObj.id)

#     return render(request, 'projects/single-project.html', {'project': projectObj, 'form': form})