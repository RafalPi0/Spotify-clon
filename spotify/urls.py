"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path

from . import views

urlpatterns = [
    # path('', views.index, name="songs" ),
    path('', views.SongList.as_view(), name='songs'),
    path('song/<str:pk>/', views.SongDetail.as_view(), name='song'),
    path('playlist/<int:pk>/', views.PlaylistSongDetail.as_view(), name='playlist'),
    path('playlist-create/', views.PlaylistSongCreate.as_view(), name='playlist-create'),
    path('playlist-update/<int:pk>/', views.PlaylistSongUpdate.as_view(), name='playlist-update'),
    path('playlist-delete/<int:pk>/',views.PlaylistSongDeleteView.as_view(), name='playlist-delete'),
    path('playlist', views.PlaylistSongList.as_view(), name='playlists'),
    # path('song/<str:pk>/', views.song, name="song"),
]
