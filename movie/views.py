from django.shortcuts import render

from genre.models import Genre
from .models import Movie
from bs4 import BeautifulSoup
import requests


def scr_top(request):
    # Top 250 scraping

    url = "https://www.imdb.com/chart/top/?ref_=nv_mp_mv250"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    tbody = soup.find("tbody", class_="lister-list").find_all('tr')
    for item in tbody:
        name = item.find('td', class_="titleColumn").a.text
        year = int(item.find("span", class_="secondaryInfo").text.strip('()'))
        rating = float(item.find("strong").text)

        try:
            movie = Movie.objects.get(name=name)
        except Movie.DoesNotExist:
            movie = Movie.objects.create(name=name, year=year, rating=rating)
        finally:
            if movie.rating != rating:
                movie.rating = rating
                movie.save()

    # Genre scraping

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    root = soup.find("ul", class_="quicklinks").find_all("li", class_="subnav_item_main")

    for item1 in root:
        genre = item1.find('a').text.replace("\n", "")
        url = item1.find('a').get("href")

        try:
            genre1 = Genre.objects.get(genre=genre)
        except Genre.DoesNotExist:
            genre1 = Genre.objects.create(genre=genre, url=url)
        finally:
            if genre1.url != url:
                genre1.url = url
                genre1.save()

    genres = Genre.objects.all()
    movies = Movie.objects.all()

    return render(request, 'movie/home.html', {"movie": movies, "genres": genres})


def about(request):
    return render(request, 'movie/about.html')
