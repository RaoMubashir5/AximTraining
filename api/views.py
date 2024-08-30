from api.models import User
from api.serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status

#Generic API views


from rest_framework import viewsets
#it is for model creation
# Read only model viewsets

class UserViewSet(viewsets.ReadOnlyModelViewSet):

    """class UserViewSet(viewsets.ModelViewSet): these are the model view sets that are that inherits the genericApiView and ViewSets 
    ReadOnlyModelViewSet is to  only listing and retreiving api not any other actions can be perform by the client.
    and we can perform all operations and there routing would also be done dynaicaly based on the request method , there are the attributes
    that tells us about the which sort of the action is going to be performed like (list,retreive(detail),update,partial_update,destroy)
    suffix are like they tell us the opration is performed on instance or list of  instences(list). basename is useful to creating the reverse URLs
    like if the basename is = 'toy' than the reverse url for each fuction would be : toy-list,toy-detail. 
    there is also  a base Url that is the first paramater of the router's registration function in url.py(it is the base of every url endpoint) like 
    if you whant to see the all users url would be:http://127.0.0.1:8000/user/  ; 'user' is the base url here and for detail view your url would be
    like this :http://127.0.0.1:8000/user/7/   ; again base would remain same for all actions."""

    
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


   


     