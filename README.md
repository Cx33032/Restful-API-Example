# Restful-API-Example
This project is using Django and rest framework from python to build the news api for news agencies and news writers to use. 

## Table of Contents
1. [Preparation](#preparation)  
2. [Functions Included](#functions-included)

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

## Functions Included
1. [User Identification](#user-identification)  
2. [News Lookup](#news-lookup)  
3. [News Modification](#news-modification) (Add / Delete)  
4. [News Agency Registration](#news-agency-registration)  

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
This will create the users' basic information 

### News Lookup

### News Modification

### News Agency Registration