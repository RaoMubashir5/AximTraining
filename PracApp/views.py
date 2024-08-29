from django.shortcuts import render,redirect
from django.http import HttpResponse

from PracApp.models import user

# Create your views here.
def userRecord(request):
     if request.method=='GET':
        user_objects=user.objects.all()
        return render(request,'userRecord.html',context={'users':user_objects})


def register(request):
    if request.method=='GET':
        return render(request,'form.html')

    if request.method=='POST':

        name=request.POST.get('name')
        age=request.POST.get('age')
        country=request.POST.get('country')
        
        #created an object of the model of the user .
        user_obj=user.objects.create(name=name,age=age,country=country)

        return redirect('userRecord')


    


