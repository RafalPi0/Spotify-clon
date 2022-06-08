"""core URL Configuration

The `urlpatterns` list routes URLs to  For more information please see:
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

from .views import SongList, SongDetail ,PlaylistSongDetail ,PlaylistSongCreate, PlaylistSongUpdate, PlaylistSongDeleteView ,PlaylistSongList, CustomLoginView,  RegisterPage

from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('accounts/login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='songs'), name='logout'),
    path('register/', RegisterPage.as_view(), name='register'),
    # path('', views.index, name="songs" ),
    path('', SongList.as_view(), name='songs'),
    path('song/<str:pk>/', SongDetail.as_view(), name='song'),

    path('playlist/<int:pk>/', PlaylistSongDetail.as_view(), name='playlist'),
    path('playlist-create/', PlaylistSongCreate.as_view(), name='playlist-create'),
    path('playlist-update/<int:pk>/', PlaylistSongUpdate.as_view(), name='playlist-update'),
    path('playlist', PlaylistSongList.as_view(), name='playlists'),
    path('playlist-delete/<int:pk>/',PlaylistSongDeleteView.as_view(), name='playlist-delete'),


    
]
