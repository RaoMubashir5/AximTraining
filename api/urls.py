from django.contrib import admin
from django.urls import path,include

from api.views import *

from rest_framework.routers import DefaultRouter

#create object of the DefaultRouter
routers=DefaultRouter()

#register the route with the ViewSet class

routers.register('user',UserViewSet,basename='bname')

urlpatterns=[
    path('',include(routers.urls)),
]


# urlpatterns = [
#     # #path to the home page
#     # # path('user/', allUserView,name="UserView"),
#     # # path('user/<int:pk>', detailUserView,name="singleUser"),
#     # # path('delete/<int:pk>', deleteUserView,name="delete"),
#     # # path('create/', createUserView,name="create"),
#     # # path('update/<int:pk>', updateView,name="update"),

#     # path('user/', classCreateAndListing.as_view(),name="UserView"),
#     # path('user/<int:pk>', concretelistModelForUserClass.as_view(),name="UserView"),
#     # # path('cr/', concretelistModelForUserClass.as_view(),name="cr"),
#     # # path('del/<int:pk>', concretelistModelForUserClass.as_view(),name="del"),
#     # # path('up/<int:pk>', concretelistModelForUserClass.as_view(),name="up"), 
#     ]
