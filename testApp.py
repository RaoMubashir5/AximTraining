import requests
import json

#URL='http://127.0.0.1:8000/user/2'

# response=requests.get(url=URL)

# json_Response=response.json()

# print(json_Response)


#...........Post .............request to create user

URL='http://127.0.0.1:8000/api/create/'


user_Data= {'user_name': 'Emmanuel Macron','user_email':'macron@gmail.com','user_age': 31, 'user_country': 'franCe'}

#use dumps fucntion to conver the python to json and use the . To convert a JSON string back into a Python object, you use json.loads().

json_data=json.dumps(user_Data)

responsed_data=requests.post(url=URL,data=json_data)
print("Status Code:", responsed_data.status_code)
data=responsed_data.json()

print("Response received :")
print(data.get('msg'))
print(data.get('errors'))


# .................PUT.........................

# URL='http://127.0.0.1:8000/api/update/6'


# user_Data= {'user_name': 'Kakashi','user_age': 21, 'user_country': 'Japan'}

# #use dumps fucntion to conver the python to json and use the . To convert a JSON string back into a Python object, you use json.loads().

# json_data=json.dumps(user_Data)

# responsed_data=requests.put(url=URL,data=json_data)
# print("Status Code:", responsed_data.status_code)
# data=responsed_data.json()

# print("Response received :",data)



# .................PATCH.........................

# URL='http://127.0.0.1:8000/api/update/12'


# user_Data= {'user_email': 'France@gmail.com'}

# #use dumps fucntion to conver the python to json and use the . To convert a JSON string back into a Python object, you use json.loads().

# json_data=json.dumps(user_Data)

# responsed_data=requests.patch(url=URL,data=json_data)
# print("Status Code:", responsed_data.status_code)
# data=responsed_data.json()

# print("Response received :",data)