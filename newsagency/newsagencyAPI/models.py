from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Story(models.Model):
    storyCategories = {
        'pol' : 'Politics',
        'art' : 'Art',
        'tech' : 'Tech',
        'trivia' : 'Trivial News'
    }

    storyRegions = {
        'uk' : 'UK',
        'eu' : 'Europe',
        'w' : 'World wide' 
    }

    headline = models.CharField(max_length=64)
    category = models.CharField(max_length=6, choices=storyCategories)
    region = models.CharField(max_length=2, choices=storyRegions)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    details = models.CharField(max_length=256)

    def __str__(self):
        return self.headline