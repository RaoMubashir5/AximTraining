from django.shortcuts import render,redirect
import datetime
from PracApp.models import*
from django.views.decorators.http import require_http_methods,require_GET
from django.http import HttpResponse,StreamingHttpResponse,HttpResponseNotFound,HttpResponseServerError,HttpResponseForbidden
import random,time
from django.utils import timezone
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
             



#redering template using render and redirect shortcuts.@require_http_methods(["GET","POST"],)
def student_views(request,sort):
     if request.method=="GET" and sort == 'asc':
        all_objects=Student.objects.all().order_by("-date_of_birth")
        return render(request,'studentsData.html',{"students":all_objects})
     elif request.method=="GET" and sort == 'desc':
        all_objects=Student.objects.all().order_by("date_of_birth")
        return render(request,'studentsData.html',{"students":all_objects})
     else:
        all_objects=Student.objects.all()
        return render(request,'studentsData.html',{"students":all_objects})
     return HttpResponseForbidden("only get requests are handled",headers={"content-length":20})
     
##Unique roll number generator:def generate_unique_roll_number(existing_roll_numbers, lower_bound=100, upper_bound=1000):
def returnUniqueRollNo(existing_roll_numbers,lower_bound,upper_bound):
    while True:
        roll_number = random.randint(lower_bound, upper_bound)
        if roll_number not in existing_roll_numbers:
            return roll_number

@require_http_methods(["GET","POST"],)
def Add_Student(request):
    if request.method=="GET":
        courses_obj=course.objects.all()
        return render(request,'addStudents.html',{'courses':courses_obj})
    
      #check if POST request is not empty.
    elif request.method=="POST":
        rand_roll=100
        lead=None
        teacher=None
        all_student= Student.objects.all()
        if all_student.exists():
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
            if len(teachers)>0:
                teacher=random.choice(teachers)
            ramdom_roll=[name.roll_number for name in all_student]
            rand_roll=returnUniqueRollNo(ramdom_roll,100,1000)
        
       

        #receiving data from POST request.
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        date_of_birth=request.POST.get('date_of_birth')

        course_name_list=request.POST.getlist('course_name')

        if (first_name and last_name) and date_of_birth:
            new_student=Student.objects.create(
                         first_name=first_name,last_name=last_name,
                         roll_number=rand_roll,date_of_birth=date_of_birth,
                         group_lead=lead,teacher=teacher,)
            for course_names in course_name_list:
                course_obj=course.objects.get(course_name=course_names)
                enrollment=Enrollment.objects.create(student=new_student,course=course_obj,enrollment_date=datetime.date.today())
            print(new_student)
            return redirect('add')
    

def task_view(request,para):
    if para == '34':
        print(para)
    # Example: Current time minus 1 day for demonstration
    updated = timezone.now() - timezone.timedelta(days=1)
    return render(request, 'lala.html', {'updated': updated})
