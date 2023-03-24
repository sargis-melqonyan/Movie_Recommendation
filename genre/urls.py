from django.urls import path
from . import views

urlpatterns = [
    path('<int:pk>/', views.show_genre_movies, name='genre_detail'),
    path('favourite/', views.favourite_page, name='favourite_movies'),
    path('add_to_favourite/<int:pk>/', views.add_to_favorites, name='add_to_favorites'),
    path('removing_from_favorites/<int:pk>', views.removing_from_favorites, name='removing_from_favorites'),
]
