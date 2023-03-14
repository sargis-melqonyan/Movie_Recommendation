from django.urls import path
from movie import views

urlpatterns = [
    path('', views.scr_top, name="site-home"),
    path('about/', views.about, name='site-about')
]
