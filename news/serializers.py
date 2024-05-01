from rest_framework import serializers
from .models import *

class StorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = ['id', 'title', 'category', 'region', 'details', 'author', 'date']

class NewsAgencySerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsAgency
        fields = ['agency_name', 'url', 'agency_code']