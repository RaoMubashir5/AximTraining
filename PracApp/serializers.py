from PracApp.models import *
from django.core import serializers
import json

class studentSerializer():
    def __init__(self,obj) -> None:
        self.studentobj=obj

    def to_json(self):
        json_object=serializers.serialize("json",[self.studentobj])
        return json_object
    
    # def Custom_fields_to_be_serialized(self,*fields):
    #     json_object=serializers.serialize("json",[self.studentobj],fields=list(fields))
    #     return json_object

    def deserialize(self):
        python_dict=json.loads(self.to_json())
        return python_dict
        

