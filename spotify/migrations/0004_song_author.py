# Generated by Django 3.2.9 on 2022-06-05 11:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('spotify', '0003_song_release_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='spotify.author'),
        ),
    ]
