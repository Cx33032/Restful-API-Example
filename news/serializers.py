# -*-   Coding with utf-8   -*- #
# -*- Developed by Harryjin -*- #

from rest_framework import serializers
from .models import *

'''
Serializers for the Story
'''
class StorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        # Author's username is not included
        fields = ['id', 'title', 'category', 'region', 'details', 'author', 'date'] 

'''
Serializers for the News Agency
'''
class NewsAgencySerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsAgency
        fields = ['agency_name', 'url', 'agency_code']