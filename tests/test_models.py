from django.test import TestCase
from spotify.models import Song, Author
from django.utils import timezone


# models test
class SongTest(TestCase):

    def create_Song(self, title="only a test"):
        return Song.objects.create(song_title=title)

    def test_Song_creation(self):
        w = self.create_Song()
        self.assertTrue(isinstance(w, Song))


class AuthorTest(TestCase):

    def create_Author(self, author_name="only a test", author_surname="yes, this is only a test"):
        return Author.objects.create(author_name=author_name, author_surname=author_surname)

    def test_Author_creation(self):
        w = self.create_Author()
        self.assertTrue(isinstance(w, Author))
        