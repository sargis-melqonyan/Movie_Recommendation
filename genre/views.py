from django.shortcuts import render, redirect
from .models import Genre, Genre_page, FavouriteMovie
from bs4 import BeautifulSoup
from django.contrib import messages
import requests
from django.contrib.auth.decorators import login_required


def scr_genre_page(request, url):
    data = Genre_page.objects.all()
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
            genre = Genre_page.objects.create(name=name, genre_list=genre_list, description=description, year=year,
                                              rating=rating)
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


@login_required
def favourite_page(request):
    user_id = request.user.id
    fav_movies = FavouriteMovie.objects.all()
    return render(request, "genre/favourite_movies.html", {'fav_movies': fav_movies, 'user_id': user_id})


def add_to_favorites(request, pk):
    # pk1 = Genre.objects.get()
    mov_item = Genre_page.objects.get(pk=pk)
    user_id = request.user.id

    try:
        FavouriteMovie.objects.get(user_id=user_id, name=mov_item.name)
        messages.success(request, f'Already in Favourite!')

    except FavouriteMovie.DoesNotExist:
        fav_mov = FavouriteMovie.objects.create(user_id=user_id,
                                                name=mov_item.name,
                                                genre_list=mov_item.genre_list,
                                                description=mov_item.description,
                                                year=mov_item.year,
                                                rating=mov_item.rating)
        messages.success(request, f'Add in Favourite')
        fav_mov.save()

    return redirect("genre_detail", pk=1)


def removing_from_favorites(request, pk):

    fav_mov = FavouriteMovie.objects.get(pk=pk)
    fav_mov.delete()
    messages.success(request, 'Movie deleted in Favorite')

    return redirect('favourite_movies')

