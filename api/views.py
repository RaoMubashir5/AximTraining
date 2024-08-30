from api.models import User
from api.serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status


from rest_framework.authentication import BasicAuthentication

from rest_framework.permissions import IsAuthenticated,AllowAny
#Generic API views

from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from rest_framework import viewsets
#it is for model creation

class UserViewSet(viewsets.ModelViewSet):
    serializer_class=UserSerializer
    queryset=User.objects.all()
   

  
   

   


     