from django.shortcuts import render
import pickle
import requests
import pandas as pd
from patsy import dmatrices

# Create your views here.
movies = pickle.load(open('model/movies_list.pkl','rb'))
similarity =pickle.load(open('model/similarity.pkl','rb'))

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    # print(data)
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), key=lambda x:x[1], reverse=True)
    recommended_movies_id = []
    recommended_movies_name = []
    recommended_movies_poster = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        if movie_id:
            recommended_movies_id.append(movie_id)
            recommended_movies_poster.append(fetch_poster(movie_id))
            recommended_movies_name.append(movies.iloc[i[0]].title)
    return recommended_movies_id,recommended_movies_name,recommended_movies_poster 

def recommendation(request):
    movie_list = movies['title'].values
    print(movie_list)
    status = False

    if request.method == "POST":
        if True:
            if request.POST:
                movies_name = request.POST['movies']
                print("movies", movies_name)
                if movies_name:
                    recommended_movies_id,recommended_movies_name,recommended_movies_poster = recommend(movies_name)
                print(recommended_movies_id)
                print(recommended_movies_name)
                print(recommended_movies_poster)
                recommend_list = list(zip(recommended_movies_id,recommended_movies_name, recommended_movies_poster))
                print(recommend_list)
                status = True

                return render(request, 'recommendation.html', {'recommend_list':recommend_list,'movies_name': recommended_movies_name, 'poster':recommended_movies_poster, 'movie_list': movie_list, 'status': status})

        # except Exception as e:
        #     error = {'error': e} 
        #     return render(request, 'recommendation.html', {'error': error,'movie_list': movie_list, 'status': status})

    else:
        return render(request, 'recommendation.html',  {'movie_list': movie_list, 'status': status})
