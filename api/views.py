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
#it is for model creation


class ListModelForUserClass(ListModelMixin,GenericAPIView,CreateModelMixin,RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin):

    #queryset=User.objects.all()    #what is the query for data retrieval,;;we can also do get_queryset() that is better than this
    serializer_class=UserSerializer  #define which class to use for serialization
    
    def get(self, request, *args, **kwargs):
        
        if self.kwargs.get('pk'):
            return self.retrieve(request, *args, **kwargs)
        else:
            return self.list(request, *args, **kwargs)
        
    def put(self,request,*args,**kwargs):

        return self.update(request,*args,**kwargs)
    
    def patch(self,request,*args,**kwargs):

        return self.partial_update(request,*args,**kwargs)
    
    def delete(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


    def get_queryset(self):
        queryset = User.objects.all()
        
        # Get the 'min_age' and 'max_age' query parameters
        min_age = self.request.GET.get('min_age')
        max_age = self.request.GET.get('max_age')
        
        # Filter the queryset based on the age range
        if min_age and max_age:
            queryset = queryset.filter(user_age__gte=min_age, user_age__lte=max_age)
        
        
        return queryset
    
    def post(self,request,*args,**kwargs):
        print(request.data)  
        return self.create(request,*args,**kwargs)
       

     
class UserClassBasedView(APIView):

    def delete(self,request,pk):
        try:
            objects=User.objects.get(id=pk)
        except User.DoesNotExist:
            return Response({'msg': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        print("simple model objects: ",objects)  # simple model objects

        deleted_data=objects.delete()

        print(deleted_data)
        return Response("User is deleted Successfully !!")


    
    def post(self,request):
            serialized=UserSerializer(data=request.data)

            #validation of the de - serialized data

            if serialized.is_valid():
                serialized.save()
                response_ji={'msg':'New User Record Created successfully.'}
                return Response(serialized.data, status=status.HTTP_201_CREATED)
            else:
                response_ji={'msg':'There are error in validation, Record not Created','errors':serialized.errors}
                return Response(response_ji,status=status.HTTP_400_BAD_REQUEST)

   
    def put(self,request,pk):
            try:
                model_instance = User.objects.get(id=pk)
            except User.DoesNotExist:
                return Response({'msg': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

            print("model_instance",model_instance)
            data_received=request.data

            print("Recieved Data:",data_received)
            serialized_object=UserSerializer(model_instance,data=data_received)

            print("serialized:",serialized_object)

            if serialized_object.is_valid():
                serialized_object.save()
                response_ji = {'msg': 'Record is updated successfully.'}
                return Response(response_ji,status=201)
            else:
                response_ji = {'msg': 'There are errors in validation, Record not Updated','errors':serialized_object.errors}
                return Response(response_ji,status=401)   
            

    def patch(self,request,pk):
        try:
            model_instance = User.objects.get(id=pk)
        except User.DoesNotExist:
            return Response({'msg': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        print("model_instance",model_instance)
        data_received=request.data

        print("Recieved Data:",data_received)
        serialized_object=UserSerializer(model_instance,data=data_received)

        print("serialized:",serialized_object)
        serialized_object=UserSerializer(model_instance,data=data_received,partial=True) #partial=True
        
        print("serialized:",serialized_object)

        if serialized_object.is_valid():
            serialized_object.save()
            response_ji = {'msg': 'Record is updated successfully.'}
            return Response(response_ji,status=201)
        else:
            response_ji = {'msg': 'There are errors in validation, Record not Updated','errors':serialized_object.errors}
            return Response(response_ji,status=401)              