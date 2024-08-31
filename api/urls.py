from django.contrib import admin
from django.urls import path,include

from api.views import *

from rest_framework.routers import DefaultRouter

#create object of the DefaultRouter
routers=DefaultRouter()

#register the route with the ViewSet class

routers.register('user',UserViewSet,basename='bname')

urlpatterns=[
    path('',include(routers.urls)),
]
