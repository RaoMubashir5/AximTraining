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
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError


@csrf_exempt
def registerUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        useremail = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        print(f"Username: {username}, Email: {useremail}, Password: {password}, Confirm Password: {confirm_password}")

        if password != confirm_password:
            return JsonResponse({'error': 'Confirm password does not match'}, status=400)
        
        try:
            user = Webuser(username=username, email=useremail)
            user.set_password(password)
            user.save()
            user.created_by = user  # Assuming self-referencing user as creator
            user.save()
            return JsonResponse({'message': 'User is created successfully.'}, status=201)
        except IntegrityError:
            return JsonResponse({'error': 'Email should be unique or another integrity issue occurred.'}, status=400)
        except ValidationError as e:
            return JsonResponse({'error': f'Validation error: {e}'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'An unexpected error occurred: {e}'}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed.'}, status=405)


       
@csrf_exempt
def loginUser(request):
    if request.method=='POST':
       
       username=request.POST.get('username')
       password=request.POST.get('password')
       print(username,password)
       user=authenticate(request,username=username,password=password)
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
    


class get_register_users(APIView):
    authentication_classes=[JWTTokenUserAuthentication]
    permission_classes=[CustomizeAPIPermissions]

    def get(self,request,pk=None):
        if pk is None:
            user=Webuser.objects.all()
            serialized=WebUserSerializer(user,many=True)
            return Response({'user':serialized.data})
        
        else:
            instance=Webuser.objects.get(id=pk)
            self.check_object_permissions(request,instance)
            user=Webuser.objects.get(id=pk)
            serialized=WebUserSerializer(user,many=False)
            return Response({'user':serialized.data})
    def put(self,request,pk=None):
        
        if pk is not None:
           instance=Webuser.objects.get(id=pk)
           self.check_object_permissions(request,instance)
           data= request.data
           serialized=WebUserSerializer(instance,data=data)
           if serialized.is_valid():
                serialized.save()
                return Response(serialized.data,status=status.HTTP_200_OK)
        return Response("You are not adding the pk")

    def patch(self,request,pk=None):
        
        if pk is not None:
            instance=Webuser.objects.get(id=pk)
            self.check_object_permissions(request,instance)
            data= request.data
            serialized=WebUserSerializer(instance,data=data,partial=True)
            if serialized.is_valid():
                    print("validete nhi hoa")
                    serialized.save()
                    return Response(serialized.data,status=status.HTTP_200_OK)
            else:
                return Response(serialized.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response("You are not adding the pk")

    def delete(self,request,pk=None):
            if pk is not None:
                instance=Webuser.objects.get(id=pk)
                self.check_object_permissions(request,instance)
                instance.delete()
                return Response(status=status.HTTP_200_OK)
            return Response("You are not adding the pk")

        
    


















