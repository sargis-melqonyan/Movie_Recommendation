from django.urls import path
from movie import views

urlpatterns = [
    path('', views.home, name="site-home"),
    path('about/', views.about, name='site-about'),
    path('scraping/', views.scraping, name="scraping"),
]
