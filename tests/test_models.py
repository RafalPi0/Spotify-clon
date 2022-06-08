from django.forms import ValidationError
from django.test import TestCase
from django.urls import resolve, reverse
from spotify.models import Song, Author
from django.utils import timezone

from spotify.views import SongDetail, SongList


# models test
class SongTest(TestCase):

    def create_Song(self, title="only a test"):
        return Song.objects.create(song_title=title)

    def test_Song_creation(self):
        w = self.create_Song()
        self.assertTrue(isinstance(w, Song))
    
    def test_list_url_is_resolved(self):
        url= reverse("songs")
        self.assertEquals(resolve(url).func.view_class, SongList )
        
    def test_list_url_is_resolved(self):
        url= reverse("song" ,args=['id-of-song'])
        self.assertEquals(resolve(url).func.view_class, SongDetail )
        
    def test_song_model_validation(self):
        song=Song()
        with self.assertRaises(ValidationError):
            song.full_clean()


class AuthorTest(TestCase):

    def create_Author(self, author_name="only a test", author_surname="yes, this is only a test"):
        return Author.objects.create(author_name=author_name, author_surname=author_surname)

    def test_Author_creation(self):
        w = self.create_Author()
        self.assertTrue(isinstance(w, Author))
        