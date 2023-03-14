from django.shortcuts import render
from .models import Genre, Genre_page
from bs4 import BeautifulSoup
import requests


def scr_genre_page(request, url):

    data = Genre_page.objects.all()  # arac sra krknorinakuma
    data.delete()

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    root = soup.find('div', class_="lister-list").find_all('div', class_='lister-item mode-advanced')

    for item in root:
        name = item.find('h3', class_="lister-item-header").a.text
        genre_list = item.find('span', class_="genre").text.replace("\n", "")
        description = item.find_all('p')[1].get_text().replace("\n", "")
        year = item.find("span", class_="lister-item-year text-muted unbold").text
        rating = float(item.find("strong").text)

        try:
            genre = Genre_page.objects.get(name=name)
        except Genre_page.DoesNotExist:
            genre = Genre_page.objects.create(name=name, genre_list=genre_list, description=description, year=year, rating=rating)
        finally:
            if genre.rating != rating:
                genre.rating = rating
                genre.save()


def show_genre_movies(request, pk):
    fas = Genre.objects.get(pk=pk)
    finally_url = f"https://www.imdb.com{fas.url}"
    scr_genre_page(request, finally_url)

    genre_page = Genre_page.objects.all()
    genres = Genre.objects.all()
    return render(request, 'genre/genre_detail.html', {"genre_page": genre_page, "genres": genres})


