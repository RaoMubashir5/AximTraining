from django.shortcuts import render
from api.models import User
from api.serializers import UserSerializer
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.response import Response
from rest_framework import status
import io #it to parse the bytes objects into stream

# import your authentication here.
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

# we have to import the authentication and permissions decorator as well for this:

from rest_framework.decorators import authentication_classes,permission_classes


# @api_view(['GET'])
# def simpleApi(request):

#     return Response("My name is rao mubashir") #it accepts the python native data, key - value pairs but you can pass string as well

# @api_view(['GET','POST','PUT','PATCH','DELETE'])
# @authentication_classes([BasicAuthentication])
# @permission_classes([IsAuthenticated])
@api_view(['GET'])
def allUserView(request,pk=None):
    if request.method=='GET':
        if pk is not None:
            print("yahan tak to ata ha")
            objects=User.objects.get(id=pk)
            print("simple model objects: ",objects)  # simple model objects
            serializer=UserSerializer(objects,many=False) #serilizing the data
        else:
            objects=User.objects.all()
            print("simple model objects: ",objects)  # simple model objects
            serializer=UserSerializer(objects,many=True) #serilizing the data

        print('serializer : ',serializer.data) #display the serilized data

        # json_data=JSONRenderer().render(serializer.data)  #it would convert the data in bytes object():raw bytes
        # # Convert bytes to strin
        # # json_string = json_data.decode('utf-8')

        # print('json_data : ',json_data)
        # return HttpResponse(json_data,content_type='application/json')

        #rather than all the above code you can return jsonresponse that do convert the serlized data dict in json itself and send it as response.
        return Response(serializer.data) #by default safe= True hota ha
    
@api_view(['GET','POST','PUT','PATCH','DELETE'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def editUserView(request,pk=None):

    if request.method=='GET':
        if pk is not None:
            print("yahan tak to ata ha")
            objects=User.objects.get(id=pk)
            print("simple model objects: ",objects)  # simple model objects
            serializer=UserSerializer(objects,many=False) #serilizing the data
            return Response(serializer.data) #by default safe= True hota ha
    

    if pk is None and request.method =='POST':
   
        serialized=UserSerializer(data=request.data)

        #validation of the de - serialized data

        if serialized.is_valid():
            serialized.save()
            response_ji={'msg':'New User Record Created successfully.'}
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        else:
            response_ji={'msg':'There are error in validation, Record not Created','errors':serialized.errors}
            return Response(response_ji,status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'DELETE':

        objects=User.objects.get(id=pk)

        print("simple model objects: ",objects)  # simple model objects

        deleted_data=objects.delete()

        print(deleted_data)
        return Response("User is deleted Successfully !!")


    if request.method in ['PUT','PATCH']:
   
        model_instance=User.objects.get(id=pk)
        print("model_instance",model_instance)
        data_received=request.data

        print("Recieved Data:",data_received)
        if request.method=='PATCH':
            serialized_object=UserSerializer(model_instance,data=data_received,partial=True) #partial=True
        else:
            serialized_object=UserSerializer(model_instance,data=data_received)

        print("serialized:",serialized_object)

        if serialized_object.is_valid():
            serialized_object.save()
            response_ji = {'msg': 'Record is updated successfully.'}
            return Response(response_ji,status=201)
        else:
            response_ji = {'msg': 'There are errors in validation, Record not Updated','errors':serialized_object.errors}
            return Response(response_ji,status=401)