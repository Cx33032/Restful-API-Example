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

    token = hashlib.sha256(bytes(user, encoding='utf-8'))
    token.update(bytes(str(time.time()), encoding='utf-8'))

    return token.hexdigest()

# Need to be added to the final report
class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        result = {'code': 200, 'msg': None}
        # print(result)
        try:
            username=request._request.POST.get('username')
            password=request._request.POST.get('password')
            user = UserInformation.objects.filter(username=username, password=password).first()

            result['msg'] = 'Welcome, '+ user.name + '!'
            if not user:
                result['code']=401
                result['msg']='Wrong Username or Password'
            else:
                request.session["username"]=username
            token=token_generate(username)
            result['token']=token
            UserTokens.objects.update_or_create(user=user, defaults={'token': token})
            
        except Exception as e:
            result['code']=401
            result['msg']='Bad Request'

        return JsonResponse(result, status=result['code'])

class IsUserAuthenticated(object):

    def authenticate(self, request):
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
        # token = request._request.POST.get('token')
        # token_find = UserTokens.objects.filter(token = token).first()
        if not request.session.get("username"):
            raise exceptions.AuthenticationFailed('Authentication Failed')
        return (request.session.get("username")) 

class LogoutView(APIView):
    authentication_classes = [IsUserAuthenticated, SessionAuthenticated]

    def post(self, request, *args, **kwargs):
        result = {'code': 200, 'msg':'Logout Successfully'}
        token = request._request.POST.get('token')
        UserTokens.objects.filter(token = token).delete()
        return JsonResponse(result, status=result['code'])


class GetStoriesView(APIView):
    def grant_permission(self):
        if self.request.method == 'GET':
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsUserAuthenticated, SessionAuthenticated]

    def get(self, request):
        
        story_cat = request.data.get('story_cat', '*')
        story_region = request.data.get('story_region', '*')
        story_date = request.data.get('story_date', '*')
        
        if story_cat=='*':
            stories = Story.objects.all()
        else:
            stories = Story.objects.filter(category=story_cat)
        if story_region!='*':
            stories = stories.filter(region=story_region)
        if story_date!='*':
            stories = stories.filter(date__gte=story_date)

        if not stories:
            result = {'code': 404, 'result':'News Not Found'}
            return JsonResponse(result, status=result['code'])

        serializer=StorySerializer(stories, many=True)
        return JsonResponse(serializer.data, status=200, safe=False)
    
    def post(self, request, *args, **kwargs):
        token = request._request.POST.get('token')
        user = UserTokens.objects.filter(token=token).first().user.name
        username = UserTokens.objects.filter(token=token).first().user.username
        title = request._request.POST.get('title')
        category = request._request.POST.get('category')
        region = request._request.POST.get('region')
        details = request._request.POST.get('details')

        try:
            Story.objects.update_or_create(title=title,category=category,author=user,region=region,details=details,author_username=username)
            result = {'code': 201, 'result':'News Posted'}
        except Exception as e:
            result = {'code': 404, 'result': 'Invalid Input'}
        return JsonResponse(result, status=result['code'])
    
class DeleteStoryView(APIView):
    # authentication_classes = [IsUserAuthenticated, SessionAuthenticated]

    def delete(self, request, story_id, *args):
        token = request.data.get('token')
        user = UserTokens.objects.filter(token=token).first().user.username
        result = {'code': 200, 'msg': 'Delete Successfully'}
        # return JsonResponse({'token': str(user)})
        try:
            story = Story.objects.filter(id=story_id).first()
            if story.author_username == user:
                story.delete()
                result = {'code': 200, 'msg': 'Delete Successfully'}
                return JsonResponse(result, status=result['code'])
        except Exception as e:
            result = {'code': 404, 'msg': 'Story Not Found'}
            return JsonResponse(result, status=result['code'])

class RegisterView(APIView):
    def get(self, request):
        agencies = NewsAgency.objects.all()
        serializer=NewsAgencySerializer(agencies, many=True)
        return JsonResponse(serializer.data, status=200, safe=False)
    
    def post(self, request, *args):
        agency_name = request._request.POST.get('agency_name')
        url = request._request.POST.get('url')
        agency_code = request._request.POST.get('agency_code')

        try:
            NewsAgency.objects.update_or_create(agency_name=agency_name, url=url, agency_code=agency_code)
            result = {'code': 201, 'msg':'News Agency Created Successfully'}
            return JsonResponse(result, status=result['code'])
        except Exception as e:
            result = {'code': 503, 'msg': str(e.__context__)}
            return JsonResponse(result, status=result['code'])
