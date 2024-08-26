"""
URL configuration for MyFirstAtAxim project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

#import views from PracApp

from PracApp.views import*

urlpatterns = [
    #path to the home page
    path('admin/', admin.site.urls),
    path('',HomePageView.as_view(extra_context={"mentor":"Salman Bhai"}),name="homePage"),#we are passwing extra contexts as well.
    #this will intansiate the HomePageView class instance.
    #and call respective methods fot the corresponding request.

    path('task_view/<str:para>',task_view,name="task_view"),
    path('add/',AddStudentsClass.as_view(),name="add"),
    path('students/',studentsListView.as_view(),name="students"),#slug accepts any data type keyword arg
    path('search/',searchClass.as_view(),name="search"),
    path('formPost/',searchDetailView.as_view(),name="formPost"),
    path('update/<slug_paramater>',updateStudentDetail.as_view(),name="update"),
    path('updateStudent/<int:pk>/', StudentUpdateView.as_view(), name='update_student'),
    path('LeadtDetailView/<slug_paramater>', LeadtDetailView.as_view(), name='LeadtDetailView'),
    
    
    path('createClassView/', createClassView.as_view(), name='createClassView'),
    # Add other URL patterns here
    ]
