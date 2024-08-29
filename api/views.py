from django.shortcuts import render
from api.models import User
from api.serializers import UserSerializer
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

#Generic API views

from rest_framework.generics import GenericAPIView #it is for generic methods and attributes
from rest_framework.mixins import ListModelMixin  #it is for model listing
from rest_framework.mixins import CreateModelMixin,RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin
from django.db.models import Max
from rest_framework.generics import ListAPIView,RetrieveAPIView,CreateAPIView,UpdateAPIView,DestroyAPIView
#it is for model creation

#collective views:

from rest_framework.generics import RetrieveUpdateDestroyAPIView,ListCreateAPIView  # (combi of three)


class concretelistModelForUserClass(RetrieveUpdateDestroyAPIView):

    serializer_class=UserSerializer  #define which class to use for serialization

    def get_queryset(self):
        queryset = User.objects.all()
        
        # Get the 'min_age' and 'max_age' query parameters
        min_age = self.request.GET.get('min_age')
        max_age = self.request.GET.get('max_age')
        
        # Filter the queryset based on the age range
        if min_age and max_age:
            queryset = queryset.filter(user_age__gte=min_age, user_age__lte=max_age)
        return queryset    

class classCreateAndListing(ListCreateAPIView):

    serializer_class=UserSerializer
    def get_queryset(self):
        queryset = User.objects.all()
        
        # Get the 'min_age' and 'max_age' query parameters
        min_age = self.request.GET.get('min_age')
        max_age = self.request.GET.get('max_age')
        
        # Filter the queryset based on the age range
        if min_age and max_age:
            queryset = queryset.filter(user_age__gte=min_age, user_age__lte=max_age)
        return queryset
     