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
    path('',homePage.as_view(),name="homePage"),
    path('task_view/<str:para>',task_view,name="task_view"),
    path('add/',AddStudentsClass.as_view(),name="add"),
    path('students/<sort>',studentList.as_view(),name="students"),
    path('search/',searchClass.as_view(),name="search"),
    path('formPost/',searchClass.as_view(),name="formPost"),
     path('update/<student_id>',updateClass.as_view(),name="update"),
    ]
