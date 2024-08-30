from api.models import User
from api.serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status

#Generic API views


from rest_framework import viewsets
#it is for model creation

class UserViewSet(viewsets.ModelViewSet):

    serializer_class=UserSerializer
    # queryset=User.objects.all()  it is attribute btu we can use the function as well to customize 

    def get_queryset(self):
        query=User.objects.all()
        min=self.request.GET.get('min_age')
        max=self.request.GET.get('max_age')
        if min and max:
            query=query.filter(user_age__gt=min,user_age__lte=max)
        return query

    # def list(self,request):
    #     print('basename: ',self.basename)
    #     print('action: ',self.action)
    #     print('detail: ',self.detail)
    #     print('description: ',self.description)
    #     print('suffix: ',self.suffix)
    #     print('name: ',self.name)

    #     user_obj=User.objects.all()
    #     serialized=UserSerializer(user_obj,many=True) #PAssing data=user_obj is for the deserializaions
    #     print(serialized.data)
    #         #resp={'msg':"here is your data ",'error':serialized.errors}
    #     return Response(serialized.data)
    
    # def retrieve(self,request,pk=None):

    #     print('basename: ',self.basename)
    #     print('action: ',self.action)
    #     print('detail: ',self.detail)
    #     print('description: ',self.description)
    #     print('suffix: ',self.suffix)
    #     print('name: ',self.name)

    #     id=pk
    #     if id is not None:
    #         user_obj=User.objects.get(id=id)
    #         serialized=UserSerializer(user_obj)
    #         print(serialized.data)
    #         #resp={'msg':"here is your data ",'error':serialized.errors}
    #         return Response(serialized.data)
    

        

    # def partial_update(self,request,pk=None):

    #     print('basename: ',self.basename)
    #     print('action: ',self.action)
    #     print('detail: ',self.detail)
    #     print('description: ',self.description)
    #     print('suffix: ',self.suffix)
    #     print('name: ',self.name)


    #     id =pk

    #     if id is not None:
    #         user_instance=User.objects.get(id=id)
    #         serialized_data=UserSerializer(user_instance,data=request.data,partial=True)
    #         if serialized_data.is_valid():
    #             serialized_data.save()
    #             resp={"msg":"User data is updated patch",'error':serialized_data.errors}
    #             return Response(serialized_data.data)
    #         else:
    #             return Response(serialized_data.errors)

    # def update(self,request,pk=None):

    #     print('basename: ',self.basename)
    #     print('action: ',self.action)
    #     print('detail: ',self.detail)
    #     print('description: ',self.description)
    #     print('suffix: ',self.suffix)
    #     print('name: ',self.name)

    #     id =pk

    #     if id is not None:
    #         user_instance=User.objects.get(id=id)
    #         serialized_data=UserSerializer(user_instance,data=request.data)
    #         if serialized_data.is_valid():
    #             serialized_data.save()
    #             resp={"msg":"User data is updated put",'error':serialized_data.errors}
    #             return Response(serialized_data.data)
    #         else:
    #             return Response(serialized_data.errors)
            

    # def create(self,request):

    #     print('basename: ',self.basename)
    #     print('action: ',self.action)
    #     print('detail: ',self.detail)
    #     print('description: ',self.description)
    #     print('suffix: ',self.suffix)
    #     print('name: ',self.name)
        
    #     serialized_data=UserSerializer(data=request.data)
    #     if serialized_data.is_valid():
    #         serialized_data.save()
    #         resp={"msg":"User data is created ",'error':serialized_data.errors}
    #         return Response(serialized_data.data)
    #     else:
    #         return Response(serialized_data.errors)
        

    # def destroy(self,request,pk=None):
        
    #     print('basename: ',self.basename)
    #     print('action: ',self.action)
    #     print('detail: ',self.detail)
    #     print('description: ',self.description)
    #     print('suffix: ',self.suffix)
    #     print('name: ',self.name)



    #     id=pk

    #     if pk is not None:

    #         User_to_delete=User.objects.get(id=id).delete()
    #         resp={"msg":"User IS Successfully Deleted"}
    #         return Response(resp)
    #     else:
    #         return Response(User_to_delete.errors)


   


     