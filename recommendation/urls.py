from django.urls import path
from . import views

urlpatterns = [
    path('',views.recommendation, name= 'recommendation'),
]
