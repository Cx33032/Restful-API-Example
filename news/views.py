# -*-   Coding with utf-8   -*- #
# -*- Developed by Harryjin -*- #

from .models import *
from .serializers import *
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework.authentication import *
from rest_framework.permissions import AllowAny

import hashlib
import time

def token_generate(user):
    '''
    The token generation is based on SHA256
    Parameters: 
    1. Username
    2. Time (Keep the token unique)
    '''
    token = hashlib.sha256(bytes(user, encoding='utf-8'))
    token.update(bytes(str(time.time()), encoding='utf-8'))

    return token.hexdigest()

class LoginView(APIView):
    # Only accept POST method in login
    def post(self, request, *args, **kwargs):
        result = {'code': 200, 'msg': None}

        try:
            username=request._request.POST.get('username')
            password=request._request.POST.get('password')
            # Find the applicable user in the database
            user = UserInformation.objects.filter(username=username, password=password).first()

            result['msg'] = 'Welcome, '+ user.name + '!'
            if not user:
                result['code']=401
                result['msg']='Wrong Username or Password'
            else:
                request.session["username"]=username

            # Generate the token for the user
            token=token_generate(username)
            # Transfer the token to the user for identification use
            result['token']=token
            # Add the token to the database
            UserTokens.objects.update_or_create(user=user, defaults={'token': token})
            
        except Exception as e:
            result['code']=401
            result['msg']='Bad Request'

        return JsonResponse(result, status=result['code'])

class IsUserAuthenticated(object):
    # Token Authentication
    def authenticate(self, request):
        # Find the token in the token list
        token=request._request.POST.get('token')
        token_find = UserTokens.objects.filter(token=token).first()
        if not token_find:
            raise exceptions.AuthenticationFailed('Authentication Failed!')
        return (token_find.user, token_find)
    def authenticate_header(self, request):
        pass
    def has_permission(self, request, view):
        pass

class SessionAuthenticated(object):

    def authenticate(self, request):
        if not request.session.get("username"):
            raise exceptions.AuthenticationFailed('Authentication Failed')
        return (request.session.get("username")) 

class LogoutView(APIView):
    # Logout can only happen when the user has signed in
    authentication_classes = [IsUserAuthenticated, SessionAuthenticated]

    def post(self, request, *args, **kwargs):
        result = {'code': 200, 'msg':'Logout Successfully'}
        token = request._request.POST.get('token')
        # Delete the token in the database
        UserTokens.objects.filter(token = token).delete()
        return JsonResponse(result, status=result['code'])


class GetStoriesView(APIView):
    def grant_permission(self):
        if self.request.method == 'GET':
            # Everyone has the permission to find the news
            self.permission_classes = [AllowAny]
        else:
            # The appending of the news can only happen after signing in
            self.permission_classes = [IsUserAuthenticated, SessionAuthenticated]

    # Search news
    def get(self, request):
        
        story_cat = request.data.get('story_cat', '*')
        story_region = request.data.get('story_region', '*')
        story_date = request.data.get('story_date', '*')
        
        # Find the data with the conditions provided by the users
        if story_cat=='*':
            stories = Story.objects.all()
        else:
            stories = Story.objects.filter(category=story_cat)
        if story_region!='*':
            stories = stories.filter(region=story_region)
        if story_date!='*':
            stories = stories.filter(date__gte=story_date)

        # No news match the condition
        if not stories:
            result = {'code': 404, 'result':'News Not Found'}
            return JsonResponse(result, status=result['code'])

        # Use the serializer to output the result
        serializer=StorySerializer(stories, many=True)
        return JsonResponse(serializer.data, status=200, safe=False)
    
    # Append news
    def post(self, request, *args, **kwargs):
        token = request._request.POST.get('token')
        # Get the user
        user = UserTokens.objects.filter(token=token).first().user.name
        username = UserTokens.objects.filter(token=token).first().user.username
        title = request._request.POST.get('title')
        category = request._request.POST.get('category')
        region = request._request.POST.get('region')
        details = request._request.POST.get('details')

        try:
            # Append the news into the database
            Story.objects.update_or_create(title=title,category=category,author=user,region=region,details=details,author_username=username)
            result = {'code': 201, 'result':'News Posted'}
        except Exception as e:
            result = {'code': 404, 'result': 'Invalid Input'}
        return JsonResponse(result, status=result['code'])
    
class DeleteStoryView(APIView):
    # Delete the news
    def delete(self, request, story_id, *args):
        try:
            # Get the user
            token = request.data.get('token')
            user = UserTokens.objects.filter(token=token).first().user.username
            result = {'code': 200, 'msg': 'Delete Successfully'}
        except:
            result = {'code': 401, 'msg': 'Unauthorized'}
            return JsonResponse(result, status=result['code'])

        try:
            story = Story.objects.filter(id=story_id).first()
            # Check whether user can delete the news
            if story.author_username == user:
                story.delete()
                result = {'code': 200, 'msg': 'Delete Successfully'}
                return JsonResponse(result, status=result['code'])
        except Exception as e:
            result = {'code': 404, 'msg': 'Story Not Found'}
            return JsonResponse(result, status=result['code'])

class RegisterView(APIView):
    # Everyone has the access to register and search the news agency

    def get(self, request):
        # Using serializers to output data
        agencies = NewsAgency.objects.all()
        serializer=NewsAgencySerializer(agencies, many=True)
        return JsonResponse(serializer.data, status=200, safe=False)
    
    def post(self, request, *args):
        # Using serializers to append new agency
        agency_name = request._request.POST.get('agency_name')
        url = request._request.POST.get('url')
        agency_code = request._request.POST.get('agency_code')

        try:
            # Add a new news agency
            NewsAgency.objects.update_or_create(agency_name=agency_name, url=url, agency_code=agency_code)
            result = {'code': 201, 'msg':'News Agency Created Successfully'}
            return JsonResponse(result, status=result['code'])
        except Exception as e:
            result = {'code': 503, 'msg': str(e.__context__)}
            return JsonResponse(result, status=result['code'])
