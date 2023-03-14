from django.urls import path
from . import views

urlpatterns = [
    path('<int:pk>/', views.show_genre_movies, name='genre_detail'),
]
