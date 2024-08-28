import rest_framework
from rest_framework import serializers
from rest_framework.renderers import JSONRenderer #it is to convert the python dictionry into json as in api only json reponse will be sent.
from api.models import User

# ...........................validator().............................
# def checkFirstLetter(value):
#     if not value[0].isupper():
#         raise serializers.ValidationError("country name's first letter should be capital")
#     else:
#         return value
    
allowed_countries = [ 'united states', 'canada', 'united kingdom', 'germany', 'france', 'australia',
                      'japan', 'india', 'china', 'brazil', 'russia', 'south korea', 'mexico',
                      'italy', 'spain', 'netherlands', 'turkey', 'sweden', 'saudi arabia', 'pakistan', 'poland']

#Modelserializer shortcut:

class UserSerializer(serializers.ModelSerializer):
     #do not need to declare the fields

     #for validators you have to do only dor the global that is defined above .
   # user_country=serializers.CharField(max_length=20,style={'placeholder':'pakistan','required':True},validators=[checkFirstLetter]) 
   
    class Meta:
        model=User
        fields='__all__'  # exclude=['roll_number']   ;;; fields=['user_name','roll_number'] 
        #validations
        #read_only_fields=['user_email']
        #we can do  itlike this as well >> extra_kwargs=['user_email':{read_only=True},]

       ###NOte other object validations and field validation works as in the serializers.
        #.............................validate_<field_real_name>.................................
            # There are the validations fro each field this method  would be called when the serialized.is_valid() function is called.

    def validate_user_country(self,value):
        if value:
            if  value.lower() not in allowed_countries:
                raise serializers.ValidationError(f"Sorry,Your country is not allowed!! <....> allowed_countries:> {str(allowed_countries)} .")
            else:
                return value.capitalize()  
        else:
            return value.capitalize()   

            # .............................validate(self,data).................................
            # There are the validations for an object that there would be multiple fields to validate, when the serialized.is_valid() function is called.
    def validate(self,data):
        country=data.get('user_country')
        age=data.get('user_age')
        if country:
            if (country.lower() in ['united states', 'canada', 'united kingdom', 'germany', 'france']) and age > 30:
                raise serializers.ValidationError('Your country does not Allow Candidate with this Age greater than 30')
            else:
                return data
        else:
            return data

    
    

    
































# # ...........................validator().............................
# def checkFirstLetter(value):
#     if not value[0].isupper():
#         raise serializers.ValidationError("country name's first letter should be capital")
#     else:
#         return value

# allowed_countries = [ 'united states', 'canada', 'united kingdom', 'germany', 'france', 'australia',
#                       'japan', 'india', 'china', 'brazil', 'russia', 'south korea', 'mexico',
#                       'italy', 'spain', 'netherlands', 'turkey', 'sweden', 'saudi arabia', 'pakistan', 'poland']

# class UserSerializer(serializers.Serializer):
#     user_name=serializers.CharField(max_length=30,)
#     user_email=serializers.EmailField(default="user@gmail.com",)
#     user_age=serializers.IntegerField()
#     user_country=serializers.CharField(max_length=20,style={'placeholder':'pakistan','required':True},validators=[checkFirstLetter]) 
#     #style is core arguments part,
#     #that how the data field would be rendered in template

#     #de-serializer:(create,delete and update we use it )


#     #if the request is post than after validation data woud be stored in validate_data .
#     #if the serailizer.save() is called than the :POST request bases the create function would be called.
#     def create(self, validated_data):
#         return User.objects.create(**validated_data)
    

#     #if the serailizer.save() is called than the :if the request is PUT(partial=False) and PATCH(partial=True) request,
#     #than call the update function would be called.
#     def update(self,instance,validated_data):
#         print(instance.user_name)

#         #it means if there is data in the user_name than update, else instance.user_name(data before update) is saved.
#         # get(updated data or already saved)
#         instance.user_name=validated_data.get('user_name',instance.user_name)  

#         print(instance.user_name)

#         instance.user_email=validated_data.get('user_email',instance.user_email)
#         instance.user_age=validated_data.get('user_age',instance.user_age)
#         instance.user_country=validated_data.get('user_country',instance.user_country)
       
#         instance.save()
#         return instance
    
#     # .............................validate_<field_real_name>.................................
#     # There are the validations fro each field this method  would be called when the serialized.is_valid() function is called.

#     def validate_user_country(self,value):
#         if  value.lower() not in allowed_countries:
#             raise serializers.ValidationError("Sorry,Your country is not allowed!!")
#         else:
#             return value.capitalize()

#     # .............................validate(self,data).................................
#     # There are the validations for an object that there would be multiple fields to validate, when the serialized.is_valid() function is called.
#     def validate(self,data):
#         country=data.get('user_country')
#         age=data.get('user_age')

#         if (country.lower() in ['united states', 'canada', 'united kingdom', 'germany', 'france']) and age > 30:
#             raise serializers.ValidationError('Your country does not Allow Candidate with this Age greater than 30')
#         else:
#             return data


    
    

    