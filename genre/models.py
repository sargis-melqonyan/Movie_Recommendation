from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Genre(models.Model):
    genre = models.CharField(max_length=255)
    url = models.TextField()

    def __str__(self):
        return self.genre

    def get_absolute_url(self):
        return reverse('genre_detail', args=[str(self.id)])


class Genre_page(models.Model):
    name = models.CharField(max_length=255)
    genre_list = models.TextField()
    description = models.TextField()
    year = models.CharField(max_length=10)
    rating = models.FloatField()
    favourite = models.ManyToManyField(User, related_name='favourite', blank=True)


class FavouriteMovie(models.Model):
    user_id = models.IntegerField()
    name = models.CharField(max_length=255)
    genre_list = models.TextField()
    description = models.TextField()
    year = models.CharField(max_length=10)
    rating = models.FloatField()

    def __str__(self):
        return self.name
