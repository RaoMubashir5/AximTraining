from api.models import User
from api.serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status


from rest_framework.authentication import BasicAuthentication,SessionAuthentication,TokenAuthentication

from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser,IsAuthenticatedOrReadOnly
from rest_framework.permissions import DjangoModelPermissions,DjangoModelPermissionsOrAnonReadOnly
#Generic API views

from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from rest_framework import viewsets
#it is for model creation

class UserViewSet(viewsets.ModelViewSet):
    serializer_class=UserSerializer
    queryset=User.objects.all()

    #overriding the global authenticationa and permission to allow any.
    authentication_classes=[SessionAuthentication]
    #permission_classes=[IsAdminUser]
      #permission_classes=[IsAuthenticatedOrReadOnly]
      #permission_classes=[IsAuthenticated]
    #django permissions that are only aplicable after authorization, and you manually assign the functionality for Use that it can perform.]
    #permission_classes=[DjangoModelPermissions]  #super user have all the permissions by default

    #anon readonly is variation of the django model permissions as it alow user to view only functionlity without authenticating. but othe ,
    #would be added manualy
    permission_classes=[DjangoModelPermissionsOrAnonReadOnly] 

   

   


     