from django.shortcuts import render
from recommendation.views import fetch_poster
import pickle
from django.core.paginator import Paginator

# Create your views here.
movies = pickle.load(open('model/movies_list.pkl','rb'))
 
def display_movies(request):
    movie_id = movies.movie_id
    movie_id = movie_id.tolist()
    # print(movie_id)
    # print(type(movie_id))
    movies_name = []
    movies_poster = []
    for i in movie_id[:12]:
        movies_poster.append(fetch_poster(i))
    movies_title = movies.title.tolist()
    # movies_name.append(movies.title)
    random_movies = list(zip(movie_id, movies_poster, movies_title[:12]))
    # print(random_movies)
    # page = request.GET.get("page", 1)
    # paginator = Paginator(random_movies, per_page=8)
    # page_object = paginator.get_page(page)
    # context = {"page_obj": page_object}
    return render(request, 'movies.html',{'context': random_movies})

def details(request, movie_id):
    id = movie_id
    poster = fetch_poster(id)
    title = movies.title
    
    context = {'poster':poster}
    return render(request, 'detail.html', context)
