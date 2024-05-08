# Restful-API-Example
This project is using Django and rest framework from python to build the news api for news agencies and news writers to use. 

## Table of Contents
- [Preparation](#preparation)  
- [To-Do List](#to-do-list)
- [Functions Included](#functions-included)

## Preparation

### Install the R equirements
```shell
pip install -r requirements.txt
```

### Add Super User
```shell
python manage.py createsuperuser
```

### Run the Server
```shell
python manage.py runserver
```

## To-Do List
- [x] Token authentication
- [ ] Finish README.md
- [ ] User registration
- [ ] Password encryption

## Functions Included
- [User Identification](#user-identification)  
- [News Lookup](#news-lookup)  
- [News Modification](#news-modification) (Add / Delete)  
- [News Agency Registration](#news-agency-registration)  

### User Identification
For the User Identification, we need a database to store users' information, so creating a model in model.py is needed.
```python
'''
news/models.py
'''
class UserInformation(models.Model):
    # The username for the users to sign in
    username = models.CharField(max_length=32, unique=True)
    # The password of the user
    password = models.CharField(max_length=64)
    # The real name of the user, to be included in the news information
    name = models.CharField(max_length=48, default='John Smith')
```
This will be used to store basic information of users  

The authentication of users is mainly depend on the token. After users log in, the token will be stored into the database
```python
'''
news/models.py
'''
class UserTokens(models.Model):
    # The token for the user, to be created after signing in
    token = models.CharField(max_length=64)
    # The user information from the UserInformation class
    user = models.OneToOneField(to='UserInformation', on_delete=models.CASCADE)
```
The token is automatically generated and totally unique  

The token generation is based on SHA-256 with the username and the login time
```python
'''
news/views.py
'''
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

```

The user login with the payload of username and password, then the program will look up the information in the database
```python
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
```
If the user can successfully log in, the program will return a welcome message instead of 401 UNAUTHORIZED


### News Lookup
Every one has the permission to lookup the news in the database  
Firstly, the ```grant_permission```function helps to give GET request open to everyone  

```python
'''
news/views.py
'''
def grant_permission(self):
        if self.request.method == 'GET':
            # Everyone has the permission to find the news
            self.permission_classes = [AllowAny]
        else:
            # The appending of the news can only happen after signing in
            self.permission_classes = [IsUserAuthenticated, SessionAuthenticated]
```
  
Secondly, the get method helps to load the choices and the return the search reasult
```python
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
```

### News Modification
#### Append new stories
When appending new stories, users need to send a post request with the required information to the designated url which required to login first  
So still need ```grant_permission``` method to switch the permission class  
```python
'''
news/views.py
'''
def grant_permission(self):
        if self.request.method == 'GET':
            # Everyone has the permission to find the news
            self.permission_classes = [AllowAny]
        else:
            # The appending of the news can only happen after signing in
            self.permission_classes = [IsUserAuthenticated, SessionAuthenticated]
```
In the ```post``` method, the program will fetch all the data transferred in the request and append those into the database  
```python
'''
news/views.py
'''
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
```

### News Agency Registration