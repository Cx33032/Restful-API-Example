# -*-   Coding with utf-8   -*- #
# -*- Developed by Harryjin -*- #

from django.contrib import admin
from .models import UserInformation, NewsAgency, UserTokens

# Register the Users to make sure website administrator can modify the information
admin.site.register(UserInformation)
admin.site.register(UserTokens)
admin.site.register(NewsAgency)