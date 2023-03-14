from django.db import models


class Movie(models.Model):
    name = models.CharField(max_length=254)
    year = models.IntegerField()
    rating = models.FloatField()

    def __str__(self):
        return f"{self.name}  ({self.year})    rating: {self.rating}"
