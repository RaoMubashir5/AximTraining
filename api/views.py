from api.models import User
from api.serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status

#Generic API views


from rest_framework import viewsets
#it is for model creation

class UserViewSet(viewsets.ViewSet):
    
    def list(self,request):

        user_obj=User.objects.all()
        serialized=UserSerializer(user_obj,many=True) #PAssing data=user_obj is for the deserializaions
        print(serialized.data)
            #resp={'msg':"here is your data ",'error':serialized.errors}
        return Response(serialized.data,status=status.HTTP_200_OK)
    
    def retrieve(self,request,pk=None):
        id=pk
        if id is not None:
            user_obj=User.objects.get(id=id)
            serialized=UserSerializer(user_obj)
            print(serialized.data)
            #resp={'msg':"here is your data ",'error':serialized.errors}
            return Response(serialized.data)
    

        

    def partial_update(self,request,pk=None):
        id =pk

        if id is not None:
            serialized_data=UserSerializer(data=request.data,partial=True)
            if serialized_data.is_valid():
                serialized_data.save()
                resp={"msg":"User data is updated patch",'error':serialized_data.errors}
                return Response(serialized_data.data)
            else:
                return Response(serialized_data.errors)

    def update(self,request,pk=None):
        id =pk

        if id is not None:
            serialized_data=UserSerializer(data=request.data)
            if serialized_data.is_valid():
                serialized_data.save()
                resp={"msg":"User data is updated put",'error':serialized_data.errors}
                return Response(serialized_data.data,status=status.HTTP_200_OK)
            else:
                return Response(serialized_data.errors)
            

    def create(self,request):
        
        serialized_data=UserSerializer(data=request.data)
        if serialized_data.is_valid():
            serialized_data.save()
            resp={"msg":"User data is created ",'error':serialized_data.errors}
            return Response(serialized_data.data,status=status.HTTP_201_OK)
        else:
            return Response(serialized_data.errors)
        

    def delete(self,request,pk=None):
        id=pk

        if pk is not None:

            User_to_delete=User.objects.get(id=id).delete()
            resp={"msg":"User IS Successfully Deleted",'error':User_to_delete.errors}
            return Response(resp,status=status.HTTP_201_OK)
        else:
            return Response(User_to_delete.errors)


   


     