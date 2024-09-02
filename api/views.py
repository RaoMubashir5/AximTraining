from api.models import Webuser
from api.serializers import WebUserSerializer
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
from rest_framework.views import APIView
from django.contrib.auth import authenticate
#import custom permissions class


class registerUser(APIView):

    def post(self, request, *args, **kwargs):

        request_data=request.data
        
        serailized=WebUserSerializer(data=request_data)

        if serailized.is_valid():
            serailized.save

            Response(serailized.data,status=status.HTTP_201_CREATED)


       

class loginUser(APIView):

    def post(self, request, *args, **kwargs):
        request_data=request.data
        
        serailized=WebUserSerializer(data=request_data)

        if serailized.is_valid():
            serailized.save

            Response(serailized.data,status=status.HTTP_201_CREATED)























from .customPermissions import CustomizeAPIPermissions


class UserViewSet(viewsets.ModelViewSet):
    
    serializer_class=WebUserSerializer
    queryset=Webuser.objects.all()
    
    #overriding the global authenticationa and permission to allow any.
    authentication_classes=[TokenAuthentication]
    permission_classes=[CustomizeAPIPermissions]


    def perform_create(self, serializer):
        
        serializer.save(created_by=self.request.user)

      #permission_classes=[IsAuthenticatedOrReadOnly]
      #permission_classes=[IsAuthenticated]
    #django permissions that are only aplicable after authorization, and you manually assign the functionality for Use that it can perform.]
    #permission_classes=[DjangoModelPermissions]  #super user have all the permissions by default

    #anon readonly is variation of the django model permissions as it alow user to view only functionlity without authenticating. but othe ,
    #would be added manualy
    #permission_classes=[DjangoModelPermissionsOrAnonReadOnly] 

   

   


     