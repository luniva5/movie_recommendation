from django.db import models

# Create your models here.
class Account(models.Model):
    name = models.CharField(max_length=100, null = True)
    email = models.EmailField(max_length=100, null = True)
    date_created = models.DateTimeField(auto_now_add = True, null = True)

    def __str__(self):
        return self.name

class Movie(models.Model):
    STATUS = (
            ('To Watch', 'To Watch'),
            ('Watching', 'Watching'),
            ('Watched', 'Watched'),
        )

    title = models.CharField(max_length=200, null = True)
    account = models.ForeignKey(Account, null = True, on_delete = models.SET_NULL)
    status = models.CharField(max_length=200, null = True, choices = STATUS)
    date_created = models.DateTimeField(auto_now_add = True, null = True)

    def __str__(self):
        return '{} {}'.format(self.title, self.account)
