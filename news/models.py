# -*-   Coding with utf-8   -*- #
# -*- Developed by Harryjin -*- #

from django.db import models

class UserInformation(models.Model):
    # The username for the users to sign in
    username = models.CharField(max_length=32, unique=True)
    # The password of the user
    password = models.CharField(max_length=64)
    # The real name of the user, to be included in the news information
    name = models.CharField(max_length=48, default='John Smith')

class UserTokens(models.Model):
    # The token for the user, to be created after signing in
    token = models.CharField(max_length=64)
    # The user information from the UserInformation class
    user = models.OneToOneField(to='UserInformation', on_delete=models.CASCADE)

class Story(models.Model):
    # Choices for the news category
    CATEGORY_CHOICES = [
        ('pol', 'Politics'),
        ('art', 'Arts'),
        ('tech', 'New Technology'),
        ('trivia', 'Trivia'),
    ]

    # Choices for the news region
    REGION_CHOICES = [
        ('uk', 'UK'),
        ('eu', 'Europe News'),
        ('w', 'World News'),
    ]

    title = models.CharField(max_length=64)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    region = models.CharField(max_length=10, choices=REGION_CHOICES)
    details = models.CharField(max_length=128)
    # News Author (Auto set in views)
    author = models.CharField(max_length=32)
    # Author's username (Auto set in views)
    author_username = models.CharField(max_length=32)
    date = models.DateTimeField(auto_now_add=True)

class NewsAgency(models.Model):
    agency_name = models.CharField(max_length=64)
    url = models.URLField()
    # Agency 5 letters code
    agency_code = models.CharField(max_length=5)