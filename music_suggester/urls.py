from django.contrib import admin
from django.urls import path
from api.views import get_playlist

urlpatterns = [
    path('playlist/<str:city>/', get_playlist, name='get_playlist'),
]
