"""
URL configuration for news_api_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# -*-   Coding with utf-8   -*- #
# -*- Developed by Harryjin -*- #

from django.contrib import admin
from django.urls import path, include
from news.views import *

urlpatterns = [
    # Register all of the functions into the urls
    path('admin/', admin.site.urls),
    path('api/login/', LoginView.as_view()),
    path('api/logout/', LogoutView.as_view()),
    path('api/stories/', GetStoriesView.as_view()),
    path('api/stories/<int:story_id>/', DeleteStoryView.as_view()),
    path('api/directory/', RegisterView.as_view()),
]
