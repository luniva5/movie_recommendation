from django.urls import path
from . import views

urlpatterns = [
    path('login/',views.loginPage, name= 'login'),
    path('signup/',views.signup, name= 'signup'),
    path('logout/',views.logoutUser, name= 'logout'),
    # path('profile/<str:pk>/',views.profile, name= 'profile'),
    # path('profile/',views.profile, name= 'profile'),
    path('watchlist/',views.watchlist, name= 'watchlist'),

]
