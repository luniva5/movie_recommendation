from django.shortcuts import render, redirect
from recommendation.views import fetch_poster
import pickle
from django.core.paginator import Paginator
import requests
from accounts.models import Comment
# Create your views here.
movies = pickle.load(open('model/movies_list.pkl','rb'))
 
def display_movies(request):
    movie_id = movies.movie_id
    movie_id = movie_id.tolist()
    # print(movie_id)
    # print(type(movie_id))
    movies_name = []
    movies_poster = []
    for i in movie_id[:24]:
        movies_poster.append(fetch_poster(i))
    movies_title = movies.title.tolist()
    # movies_name.append(movies.title)
    random_movies = list(zip(movie_id, movies_poster, movies_title[:24]))
    paginator = Paginator(random_movies, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # print(random_movies)
    # page = request.GET.get("page", 1)
    # paginator = Paginator(random_movies, per_page=8)
    # page_object = paginator.get_page(page)
    # context = {"page_obj": page_object}
    return render(request, 'movies.html',{'context': page_obj})

def details(request, movie_id):

    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    title = data['original_title']
    overview = data['overview']

    genres_list = data['genres']
    genres = [d['name'] for d in genres_list]
    genre = ', '.join(genres)

    prod_list = data['production_companies']
    prods = [d['name'] for d in prod_list]
    prod = ', '.join(prods)

    release_date = data['release_date']
    link = data['homepage']
    imdb = data['vote_average']
    status = data['status']
    
    movie_comments = Comment.objects.filter(movie_id=movie_id)
    print(movie_comments)
    context = {
            'poster':full_path, 
            'title': title, 
            'overview': overview, 
            'genre':genre, 
            'release_date':release_date, 
            'link': link,
            'prod': prod,
            'imdb': imdb,
            'status': status,
            'movie_id': movie_id,
            'movie_comments': movie_comments   
        }
    return render(request, 'detail.html', context)


def deleteComment(request, comment_id):
    Comment.objects.filter(id=comment_id).delete()
    movie_id = request.POST.get('movie_id')
    return redirect('/movies/details/'+movie_id)

# cd .venv/scripts
#  py manage.py runserver