from .models import Song
from django.db.models import Q

def searchSongs(request):
    search_query = ''
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
    songs = Song.objects.distinct().filter(
        Q(song_title__icontains=search_query)
     
    )
    return songs, search_query