from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

from spotify.models import Song, PlaylistSong
from .forms import PlaylistSongForm
from .utils import searchSongs, paginateSongs

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
    form = PlaylistSongForm()
    print(form)
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
            print(request.POST)
            
        
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