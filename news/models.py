from django.db import models

class UserInformation(models.Model):
    username = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=64)
    name = models.CharField(max_length=48, default='John Smith')

class UserTokens(models.Model):
    token = models.CharField(max_length=64)
    user = models.OneToOneField(to='UserInformation', on_delete=models.CASCADE)

class Story(models.Model):
    CATEGORY_CHOICES = [
        ('pol', 'Politics'),
        ('art', 'Arts'),
        ('tech', 'New Technology'),
        ('trivia', 'Trivia'),
    ]

    REGION_CHOICES = [
        ('uk', 'UK'),
        ('eu', 'Europe News'),
        ('w', 'World News'),
    ]

    title = models.CharField(max_length=64)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    region = models.CharField(max_length=10, choices=REGION_CHOICES)
    details = models.CharField(max_length=128)
    author = models.CharField(max_length=32)
    author_username = models.CharField(max_length=32)
    date = models.DateTimeField(auto_now_add=True)

class NewsAgency(models.Model):
    agency_name = models.CharField(max_length=64)
    url = models.URLField()
    agency_code = models.CharField(max_length=5)