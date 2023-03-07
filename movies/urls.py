from django.urls import path
from . import views

urlpatterns = [
    path('',views.display_movies, name= 'movies'),
    path('details/<str:movie_id>', views.details, name='details'),
]
