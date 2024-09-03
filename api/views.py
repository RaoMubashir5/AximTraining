from api.models import Webuser
from api.serializers import WebUserSerializer
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render,redirect
from django.http import  JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.authentication import BasicAuthentication,SessionAuthentication,TokenAuthentication

from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser,IsAuthenticatedOrReadOnly
from rest_framework.permissions import DjangoModelPermissions,DjangoModelPermissionsOrAnonReadOnly
#Generic API views

from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import logout
from django.http import HttpResponseRedirect,Http404,HttpResponse
from rest_framework import viewsets
#it is for model creation
from rest_framework.views import APIView
from django.contrib.auth import authenticate
#import custom permissions class
from rest_framework.decorators import authentication_classes,permission_classes,api_view
from api.customPermissions import CustomizeAPIPermissions

@csrf_exempt
def registerUser(request):
    if request.method=='POST':
        username=request.POST.get('username')
        useremail=request.POST.get('email')
        password=request.POST.get('password1')
        password2=request.POST.get('password2')
        if password != password2:
            return HttpResponse("Confiem password does not match")
        try:
            user=Webuser.objects.create(username=username,email=useremail)
            user.set_password(password)
            user.created_by=user   #user.created.created_by=self.instance
            user.save()
            return HttpResponse("User is created successfully.")
        except Exception as e:
            # Handle other exceptions
            return HttpResponse(f"email should be unique.")
       
    else:
        return Http404()





       
@csrf_exempt
def loginUser(request):
    if request.method=='POST':
       
       username=request.POST.get('username')
       password=request.POST.get('password')
       print(username,password)
       user=authenticate(username=username,password=password)
       print(user)
       if user is not None:
           refresh_and_access_token=RefreshToken.for_user(user)
           access_token = str(refresh_and_access_token.access_token)
           refresh_token = str(refresh_and_access_token)
           response_to_be_send={
               'username':username,
               'access': access_token,
               'refresh':refresh_token,
           }
           return JsonResponse(response_to_be_send,status=status.HTTP_200_OK)
       else:
           response_to_be_send={
               'response':"Invalid crededentials.!!",
           }
           return JsonResponse(response_to_be_send,status=status.HTTP_400_BAD_REQUEST)  
    

@api_view(['GET','PUT','PATCH','OPTIONS'])
@authentication_classes([JWTTokenUserAuthentication])
@permission_classes([CustomizeAPIPermissions])
def get_register_users(request,pk=None):

    if request.method=='GET':
        if pk is None:
            user=Webuser.objects.all()
            serialized=WebUserSerializer(user,many=True)
            return Response({'user':serialized.data})
        
        else:
            user=Webuser.objects.get(id=pk)
            serialized=WebUserSerializer(user,many=False)
            return Response({'user':serialized.data})
    if request.method == 'PUT':
        if pk is not None:
           instance=Webuser.objects.get(id=pk)
           data= request.data
           serialized=WebUserSerializer(instance,data=data)
           if serialized.is_valid():
                serialized.save()
                return Response(serialized.data,status=status.HTTP_200_OK)
        return Response("You are not adding the pk")

    if request.method=='PATCH':
        if pk is not None:
            instance=Webuser.objects.get(id=pk)
            data= request.data
            serialized=WebUserSerializer(instance,data=data,partial=True)
            if serialized.is_valid():
                    print("validete nhi hoa")
                    serialized.save()
                    return Response(serialized.data,status=status.HTTP_200_OK)
            else:
                return Response(serialized.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response("You are not adding the pk")

    if request.method=='DELETE':
            if pk is not None:
                instance=Webuser.objects.get(id=pk).delete()
                return Response(serialized.data,status=status.HTTP_200_OK)
            return Response("You are not adding the pk")

        
    




















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

   

   


     