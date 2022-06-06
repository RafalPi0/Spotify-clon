from django.contrib import admin
from .models import Song, Author, PlaylistSong

# Register your models here.


admin.site.register(Song)
admin.site.register(Author)
admin.site.register(PlaylistSong)