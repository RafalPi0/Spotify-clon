from django.db.models.base import Model
from django.forms import ModelForm, widgets
from django import forms
from .models import PlaylistSong


class PlaylistSongForm(ModelForm):
    
    class Meta:
        model = PlaylistSong
        fields = '__all__'
        
       
        exclude = ('user',"songs",)
    
       

    # def __init__(self, *args, **kwargs):
    #     super(PlaylistSong, self).__init__(*args, **kwargs)

    #     for name, field in self.fields.items():
    #         field.widget.attrs.update({'class': 'input'})