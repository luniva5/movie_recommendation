from django.db import models
from django.contrib.auth.models import User
# Create your models here.
# class Account(models.Model):
#     name = models.CharField(max_length=100, null = True)
#     email = models.EmailField(max_length=100, null = True)
#     date_created = models.DateTimeField(auto_now_add = True, null = True)

#     def __str__(self):
#         return self.name

class Movie(models.Model):
    STATUS = (
            ('To Watch', 'To Watch'),
            ('Watching', 'Watching'),
            ('Watched', 'Watched'),
        )

    title = models.CharField(max_length=200, null = True)
    account = models.ForeignKey(User, null = True, on_delete = models.SET_NULL)
    status = models.CharField(max_length=200, null = True, choices = STATUS)
    date_created = models.DateTimeField(auto_now_add = True, null = True)

    def __str__(self):
        return '{} {}'.format(self.title, self.account)

class Comment(models.Model):
    movie_id = models.IntegerField()
    user = models.ForeignKey(User, null = True, on_delete = models.SET_NULL)
    comments = models.CharField(max_length = 500, null = True)
    created_at = models.DateTimeField(null = True)

class WatchList(models.Model):
    user = models.ForeignKey(User, null = True, on_delete = models.SET_NULL)
    movie_id = models.IntegerField()
    


    
