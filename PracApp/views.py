from django.shortcuts import render,redirect
import datetime
from PracApp.models import*
from django.views.decorators.http import require_http_methods,require_GET
from django.http import HttpResponse,StreamingHttpResponse,HttpResponseNotFound,HttpResponseServerError,HttpResponseForbidden
import random,time
# Create your views here.

@require_http_methods(["GET"],)
def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" %now
    print(html)
    return HttpResponse(html)


@require_GET
def readAndSendBookContent(request):
    
    file_iterator=open('simpletextFile.txt')
    response=HttpResponse(file_iterator,content_type="text/plain",headers={"team":"axim"},) #headers can be set at instanciation
    response.headers["religion"]="Islam"
    #print(response.content)
    response["content-length"]=1000
    
    response["name"]="Rao Mubashir"
    response.headers["age"]=21
    print(response)
    file_iterator.close()
    #return HttpResponseForbidden("Hn bhai hogi request saphall")
    return response


"""Streamlineresponse send data in chunks , by making the server response more efficient,
   this is good when there is large data to be responded."""
def yield_file_content(file_name,chunk_size=64):

        #with open the file and closes it itself.(rb means = raw byte)
        with open(file_name,'rb') as file:
            while True:
                chunk=file.read(chunk_size)
                if chunk:
                    yield chunk   #Sends each chunk of data to the StreamingHttpResponse
                else: break

def streamlineResponse(request):
    response=StreamingHttpResponse(yield_file_content('simpletextFile.txt'), content_type="text/plain")
    print(response.content)
    # response['Content-Disposition']:This is like a note you attach to your file when you send it from the server to the user’s browser.
    # filename="report.pdf" This suggests a name for the file when the user saves it.
    # attachment: This tells the browser to treat the file as something that should be downloaded, not displayed in the browser window.
    #response['content-disposition']=f'attachment;file_name="chunkFileDownload.pdf"'
    return response
             



#redering template using render and redirect shortcuts.
@require_http_methods(["GET","POST"],)
def student_views(request):
     if request.method=="GET":
        all_objects=Student.objects.all()
        return render(request,'studentsRecords.html',{"students":all_objects})
     if request.method=="POST":
        if len(request.POST.get('name')) > 0:
            name=request.POST.get('name')
            print(name)
            return redirect('student_views')
        return HttpResponseForbidden("Kuch bhajo to sahi bhai",headers={"content-length":20})
     
##Unique roll number generator:def generate_unique_roll_number(existing_roll_numbers, lower_bound=100, upper_bound=1000):
def returnUniqueRollNo(existing_roll_numbers,lower_bound,upper_bound):
    while True:
        roll_number = random.randint(lower_bound, upper_bound)
        if roll_number not in existing_roll_numbers:
            return roll_number

@require_http_methods(["GET","POST"],)
def Add_Student(request):
    if request.method=="GET":
        return render(request,'add_Student.html')
    
      #check if POST request is not empty.
    elif request.method=="POST":
        all_student= Student.objects.all()
        students_without_group_leads= Student.objects.filter(group_lead__isnull=True)

        if students_without_group_leads.exists():
            print(students_without_group_leads)

            # Extract the students who don't have a group_lead
            students_list = [student for student in students_without_group_leads]
            print(students_list)
            lead=random.choice(students_list)
            print(lead)
        else:
            print("All students have group leads.")
            

        teachers=[name.teacher for name in all_student]
        
        if teachers:
            as_teacher=random.choice(teachers)
        else: teacher=None
        ramdom_roll=[name.roll_number for name in all_student]
        rand_roll=returnUniqueRollNo(ramdom_roll,100,1000)

        #receiving data from POST request.
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        date_of_birth=request.POST.get('date_of_birth')

        if (first_name and last_name) and date_of_birth:
            new_student=Student.objects.create(
                         first_name=first_name,last_name=last_name,
                         roll_number=rand_roll,date_of_birth=date_of_birth,
                         group_lead=lead,teacher=as_teacher,)
            print(new_student)
            return redirect('Add_Student')
from django.utils import timezone
def task_view(request):
    # Example: Current time minus 1 day for demonstration
    updated = timezone.now() - timezone.timedelta(days=1)
    return render(request, 'lala.html', {'updated': updated})
