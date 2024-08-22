from django.shortcuts import render,redirect
import datetime
from PracApp.models import*
from django.views.decorators.http import require_http_methods,require_GET,require_POST
from django.http import HttpResponse,StreamingHttpResponse,HttpResponseNotFound,HttpResponseServerError,HttpResponseForbidden
import random,time
from django.utils import timezone

#import built in view class and then we will customize it .
from django.views import View

#First there are function based views,
#after that we will go through the class base view

    

def task_view(request,para):
    if para == '34':
        print(para)
    # Example: Current time minus 1 day for demonstration
    updated = timezone.now() - timezone.timedelta(days=1)
    return render(request, 'test.html', {'updated': updated})


            
class searchClass(View):
    def get(self,request):
        return render(request,'search.html',)
    
    def post(self,request):
        print("POST request: ",request.POST)
        name=request.POST.get('first_name')
        students_query_Set=Student.objects.filter(first_name__iexact=name)
        print(students_query_Set)
        if students_query_Set.exists():
            records=True
            massage_to_send="Here is the Details of the Students against"
            return render(request,'student_details.html',{'students':students_query_Set,
                          'student_name':name,'records':records,'massage_send':massage_to_send})
        else:
            massage_to_send="There are No Students named : "
            records=False
            return render(request,'student_details.html',{'massage_send':massage_to_send,
                                                          'student_name':name,'records':records})
def returnUniqueRollNo(ramdom,start,end):
    while True:
        roll_number=random.randint(start,end)
        if roll_number in ramdom:
            continue
        else:
            return roll_number

class homePage(View):

    def get(self,request):
        return render(request,'homePage.html')
        


class AddStudentsClass(View):
    """In class based views we will extend the functionalities of the 
       view class and than implement customization in it."""
    def get(self,request):
        courses_obj=course.objects.all()
        return render(request,'addStudents.html',{'courses':courses_obj})
    

    def post(self,request):
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

        
class studentList(View):
    
    def get(self,request,sort):
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
 
    def post(self,request,sort):
        lead=None
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
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        date_of_birth=request.POST.get('date_of_birth')
        updated_teacher=request.POST.get('teacher_name')
        updated_roll=request.POST.get('roll_number')
        updated_course_name_list=request.POST.getlist('course_name')
       # lead=request.POST.getlist('group_lead')
        updated_teach=None
        print("teacher :",updated_teacher)
        if updated_teacher is None:
            updated_teach=None
        else:   
            updated_teach=teacher.objects.get(name=updated_teacher)

            
        if len(updated_roll) <= 0:updated_roll=Student.objects.get(id=sort).roll_number
        if lead is None:updated_teacher=None
        if len(first_name) <= 0:updated_teacher=Student.objects.get(id=sort).first_name
        if len(last_name) <= 0:updated_teacher=Student.objects.get(id=sort).last_name


        updated_student=Student.objects.get(id=sort)
        print(updated_teach)
        updated_student.first_name=first_name
        updated_student.last_name=last_name
        updated_student.roll_number=updated_roll
        updated_student.date_of_birth=date_of_birth
        updated_student.teacher=updated_teach
        
        updated_student.save()
        print(updated_course_name_list)
        already_enrolled_courses=[course_reg.course.course_name for course_reg in updated_student.enrolled.all()]
        print(already_enrolled_courses)
        for course_obj in course.objects.all():
            if course_obj.course_name in updated_course_name_list and (course_obj.course_name not in already_enrolled_courses):
                enrollment=Enrollment.objects.create(student=updated_student,course=course_obj,enrollment_date=datetime.date.today())
            elif course_obj.course_name not in updated_course_name_list and (course_obj.course_name in already_enrolled_courses):
                print(updated_student.enrolled.get(course=course_obj.id).delete())

        print(updated_student)
        return redirect('add')




        
        
class updateClass(View):
    def get(self,request,student_id):
        student_obj=Student.objects.filter(id=student_id)
        enrolled_courses=[enroll.course.course_name for enroll in student_obj[0].enrolled.all()]
        print("Student object: ",student_obj)
        if student_obj.exists():
            return render(request,'update.html',{'student':student_obj[0],'enrolled_courses':enrolled_courses,
                                                  'courses_to_enroll':course.objects.all()})
    

