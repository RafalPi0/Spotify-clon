from django.db.models.base import Model
from django.forms import ModelForm, widgets
from django import forms
from .models import PlaylistSong


class PlaylistSongForm(ModelForm):
    class Meta:
        model = PlaylistSong
        fields = '__all__'
        
        AGE_CHOICES = (
                ('', 'Select an age'),
                ('10', '10'), #First one is the value of select option and second is the displayed value in option
                ('15', '15'),
                ('20', '20'),
                ('25', '25'),
                ('26', '26'),
                ('27', '27'),
                ('28', '28'),
                )
        widgets = {
            'list_title': forms.Select(choices=AGE_CHOICES,attrs={'class': 'form-control'}),
        }
        exclude = ('user',"songs",)
       

    # def __init__(self, *args, **kwargs):
    #     super(PlaylistSong, self).__init__(*args, **kwargs)

    #     for name, field in self.fields.items():
    #         field.widget.attrs.update({'class': 'input'})