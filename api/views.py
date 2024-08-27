from django.shortcuts import render
from api.models import User
from api.serializers import UserSerializer
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
import io #it to parse the bytes objects into stream


from rest_framework.parsers import JSONParser  #it is used to parse the json data to python native data

# Create your views here.

def allUserView(request):

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
    return JsonResponse(serializer.data,safe=False) #by default safe= True hota ha


def detailUserView(request,pk):

    objects=User.objects.get(id=pk)
    print("simple model objects: ",objects)  # simple model objects

    serializer=UserSerializer(objects,many=False) #serilizing the data

    print('serializer : ',serializer.data) #display the serilized data

    json_data=JSONRenderer().render(serializer.data)  #it would convert the data in bytes object():raw bytes
    # Convert bytes to strin
    # json_string = json_data.decode('utf-8')

    print('json_data : ',json_data)
    return HttpResponse(json_data,content_type='application/json')

def deleteUserView(request,pk):

    objects=User.objects.get(id=pk)

    print("simple model objects: ",objects)  # simple model objects

    deleted_data=objects.delete()

    print(deleted_data)

    return HttpResponse("successfully Deleted!",content_type='text')


def deleteUserView(request,pk):

    objects=User.objects.get(id=pk)

    print("simple model objects: ",objects)  # simple model objects
    

    deleted_data=objects.delete()

    print(deleted_data)

    return HttpResponse("successfully Deleted!",content_type='text')

# @csrf_exempt
# def createUserView(request):
#     if request.method=='POST':
#         request_data=request.body
#         print("request_body:",request_data)
#         stream=io.BytesIO(request_data)# changes the bytes objects in to stream
#         print("stream:",stream)
#         python_object=JSONParser().parse(stream) #it converts the json data into python native objects
#         print("python_object_native:",python_object)

#         #de - serilaize the data:(conversion of python native  object into model object and create another row in database)

#         serialized=UserSerializer(data=python_object)

#         #validation of the de - serialized data

#         if serialized.is_valid():
#             serialized.save()
#             response_ji={'msg':'New User Record Created successfully.'}

#             #why not serializing it : because data is already in python native dictionary format.

#             #convert it back into json
#             return JsonResponse(response_ji,safe=False)
#         else:
#             response_ji={'msg':'There are error in validation, Record not Created'}
#             #convert it back into json
#             return JsonResponse(response_ji, safe=False, status=400)
#     return JsonResponse({'msg': 'Invalid request method'}, status=405)

        
import traceback

@csrf_exempt
def createUserView(request):
    if request.method == 'POST':
        try:
            request_data = request.body
            print("request_body:", request_data)
            stream = io.BytesIO(request_data)
            python_object = JSONParser().parse(stream)
            print("python_object_native:", python_object)

            serialized = UserSerializer(data=python_object)
            if serialized.is_valid():
               
                serialized.save()
                response_ji = {'msg': 'New User Record Created successfully.'}
                return JsonResponse(response_ji, safe=False)
            else:
                response_ji = {'msg': 'validation Error!!' ,'errors':serialized.errors}
                return JsonResponse(response_ji, safe=False, status=400)
        except Exception as e:
            print("Error:", str(e))
            traceback.print_exc()
            return JsonResponse({'msg': 'Internal Server Error'}, status=500)
    return JsonResponse({'msg': 'Invalid request method'}, status=405)

@csrf_exempt
def updateView(request,pk):
    if request.method in ['PUT','PATCH']:
        model_instance=User.objects.get(id=pk)
        print("model_instance",model_instance)
        data_received=request.body

        stream=io.BytesIO(data_received)

        python_object = JSONParser().parse(stream)
        print("python_object:",python_object)
        if request.method=='PATCH':
            serialized_object=UserSerializer(model_instance,data=python_object,partial=True) #partial=True
        else:
            serialized_object=UserSerializer(model_instance,data=python_object)
        print("serialized:",serialized_object)
        if serialized_object.is_valid():
            serialized_object.save()
            response_ji = {'msg': 'Record is updated successfully.'}
            return JsonResponse(response_ji,safe=False,status=201)
        else:
            response_ji = {'msg': 'There are errors in validation, Record not Updated','errors':serialized_object.errors}
            return JsonResponse(response_ji,safe=False,status=400)
        
    return JsonResponse({'msg': 'Invalid request method'}, status=405)