from django.shortcuts import render, redirect
from . models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from . forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from . decorators import unauthenticated_user
from django.utils import timezone
from recommendation.views import fetch_poster
import requests
# Create your views here.

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or Password is incorrect')

    return render(request, 'accounts/login.html')


def logoutUser(request):
    logout(request)
    return redirect('login')

@unauthenticated_user
def signup(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account created successfully for '+ user)
            return redirect('login')

    context = {'form': form}
    return render(request, 'accounts/register.html', context)

def profile(request, pk):
    user = Account.objects.get(id = pk)
    movies = Account.order_set.all()
    towatch = movies.filter(status='To Watch').count()
    watching = movies.filter(status='Watching').count()
    watched = movies.filter(status='Watched').count()
    context = {'user': user, 'towatch' : towatch, 'watching': watching, 'watched': watched}

    # To make a dynamic view for customer 
    return render(request, 'accounts/profile.html',context)

def watchlist(request):
    # movies = Account.order_set.all()
    # towatch = Movies.filter(status='To Watch').count()
    # watching = movies.filter(status='Watching').count()
    # watched = movies.filter(status='Watched').count()
    # context = {'user': user, 'towatch' : towatch, 'watching': watching, 'watched': watched}
# Entry.objects.filter(myfilter).values(columname).distinct()
    movie_id = WatchList.objects.filter(user=request.user).values('movie_id').distinct()
    watchlist_id = list(WatchList.objects.filter(user=request.user).values('id'))
    print(watchlist_id)
    movie_id = list(movie_id)
    movies_name = []
    movies_poster = []
    movies_id = []
    id = []
    for i in movie_id:
        # print(i['movie_id'])
        movies_poster.append(fetch_poster(i['movie_id']))
        url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(i['movie_id'])
        data = requests.get(url)
        data = data.json()
        movies_name.append(data['original_title'])
        movies_id.append(i['movie_id'])
    movies = list(zip(movies_id, movies_poster, movies_name))
    return render(request, 'accounts/watchlist.html',{'context': movies})


def saveComment(request):
    if request.method == 'POST':
        comments = request.POST.get('comments')
        user = User.objects.get(username= request.POST.get('user'))
        movie_id = request.POST.get('movie_id')
        created_at = timezone.now()
        Comment.objects.create(comments=comments, user=user, movie_id=movie_id, created_at=created_at)
        return redirect('/movies/details/'+movie_id)
    
def addToWatchList(request):
     if request.method == 'POST':
        movie_id = request.POST.get('movie_id')
        user = User.objects.get(username= request.POST.get('user'))

        WatchList.objects.create( user=user, movie_id=movie_id)
        return redirect('/movies/details/'+movie_id)