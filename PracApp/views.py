from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.shortcuts import render,redirect
from datetime import datetime

from PracApp.models import*
from django.views.decorators.http import require_http_methods,require_GET,require_POST
from django.http import HttpRequest, HttpResponse,StreamingHttpResponse,HttpResponseNotFound,HttpResponseServerError,HttpResponseForbidden
import random,time
from django.utils import timezone
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from django.views.generic import TemplateView,ListView,DetailView,CreateView

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
           
            return render(request,'student_details.html',{'students':students_query_Set,
                          'student_name':name,'records':records,'massage_send':massage_to_send})
        else:
            massage_to_send="There are No Students named : "
            records=False
            return render(request,'student_details.html',{'massage_send':massage_to_send,
                                                          'student_name':name,'records':records})
        


# It is not good to use hte POSt with the Lisview attribute 
class searchDetailView(ListView):
    model=Student
    context_object_name='students'
    template_name='student_details.html'


    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        return context
    def post(self,request,*args,**kwargs):
        # print(self.get_context_data(**kwargs))
        # Manually setting the object_list attribute(because Listview does not handle POST request)  
        self.object_list = self.get_queryset()
        context=self.get_context_data(**kwargs)
        context['student_name']=self.request.POST.get('name')
        # if self.model.objects.filter('name').exists():print("query set: ",self.get_queryset())
        
        # Manually setting the object_list attribute
        
        if self.object_list.exists():
            context['records']=True
            context['massage_send']="Credidentils of the student are following : "
        else:
            context['records']=False
            context['massage_send']="There are No Students named : "
        print(context)
        return self.render_to_response(context)
    def get_queryset(self):
            # Filter the queryset based on the student's first name from POST data
            print(self.request.POST)
            name = self.request.POST.get('first_name')
            print("Name:",name)
            if name:
                return self.model.objects.filter(first_name=name)
            else:
                # Return an empty queryset if no name is provided in POST
                return self.model.objects.none()
        

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

        
class studentsList(TemplateView):
    """templateview inherits the TemplateResponsemixin , contextmixins ,and View(as_view to instanciate class instance,and using 
     dispatch function to check which type of request it is  . and than send it to that method)"""

#     #it is data memeber of the TemplateResponsemixin
    template_name='studentsData.html'

#it is conntextmixins's method
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        all_objects=Student.objects.all().order_by("-date_of_birth")
        context['students']=all_objects

        print(kwargs)
        getparam=self.request.GET
        print(getparam)
        return context
    
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)
    
    # def get(self,request,sort):
    #     if request.method=="GET" and sort == 'asc':
    #         all_objects=Student.objects.all().order_by("-date_of_birth")
    #         return render(request,'studentsData.html',{"students":all_objects})
    #     elif request.method=="GET" and sort == 'desc':
    #         all_objects=Student.objects.all().order_by("date_of_birth")
    #         return render(request,'studentsData.html',{"students":all_objects})
    #     else:
    #         all_objects=Student.objects.all()
    #         return render(request,'studentsData.html',{"students":all_objects})
    #     return HttpResponseForbidden("only get requests are handled",headers={"content-length":20})
 
    def post(self,request):
        lead=None
        sort=self.request.GET.get('pk')
        print("sort :",sort)
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


        date_of_birth_str=request.POST.get('date_of_birth')
        date_of_birth_obj = datetime.strptime(date_of_birth_str, '%b. %d, %Y') 
        
        # Step 2: Format the datetime object into 'YYYY-M-D' format
        date_of_birth = date_of_birth_obj.strftime('%Y-%m-%d')

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

        print("slug:name :",sort)
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
                enrollment=Enrollment.objects.create(student=updated_student,course=course_obj,enrollment_date='2000-1-1')
            elif course_obj.course_name not in updated_course_name_list and (course_obj.course_name in already_enrolled_courses):
                print(updated_student.enrolled.get(course=course_obj.id).delete())

        print(updated_student)
        return redirect('homePage')




        
        
class updateClass(View):
    def get(self,request,student_id):
        student_obj=Student.objects.filter(id=student_id)
        enrolled_courses=[enroll.course.course_name for enroll in student_obj[0].enrolled.all()]
        print("Student object: ",student_obj)
        if student_obj.exists():
            return render(request,'update.html',{'student':student_obj[0],'enrolled_courses':enrolled_courses,
                                                  'courses_to_enroll':course.objects.all()})

#detail view to that returns a object id as url paramater and used to get only 1 object
class updateStudentDetail(DetailView):
    model=Student
    context_object_name='student'
   #by default: pk_url_kwarg='pk'
    slug_field='id'
    slug_url_kwarg='slug_paramater'
    template_name='update.html'

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        student_To_update=self.model.objects.get(id=self.kwargs.get('slug_paramater'))
        enrolled_courses=[enroll.course.course_name for enroll in student_To_update.enrolled.all()]
        context['enrolled_courses']=enrolled_courses
        context['courses_to_enroll']=course.objects.all()
        print(context)
        return context
    def get_queryset(self) :
        return super().get_queryset()



#it is wrong technoque to do a work of detail view with the List view class inheritence.
class updateListView(ListView):
    model=Student
    context_object_name='student'
    template_name='update.html'

    def get_queryset(self):
        student_id=self.request.GET.get('student_id')
        
        query=Student.objects.get(id=student_id)
        print(query)
        return query
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        idd=self.request.GET.get('student_id')
        print("idd:",idd)
        student_obj=Student.objects.get(id=idd)
        enrolled_courses=[enroll.course.course_name for enroll in student_obj.enrolled.all()]
        context['enrolled_courses']=enrolled_courses
        context['courses_to_enroll']=course.objects.all()
        return context


class courseListView(ListView):
    model=course
    context_object_name='course'





class enrollmentListView(ListView):
    model=Enrollment
    context_object_name='enrollments'

class HomePageView(TemplateView):
    template_name = 'homePage.html'
    def get_context_data(self, **kwargs):#this is send any customize context to the template.
        context_funct=super().get_context_data(**kwargs)
        context_funct['name']='Mubashir Qadeer'
        students=Student.objects.all()
        context_funct['students']=students
        return context_funct

class studentsListView(ListView):

    model=Student
    template_name="studentsData.html"
    context_object_name='students'
    paginate_by = 12

    # def get_ordering(self):
    #    # order = self.kwargs.get('sort')  #it is access the url parameter for dict : self.kwargs

    #     order=self.request.GET.get('sort')
    #     print("order: ",order)  # Debugging to ensure the 'sort' parameter is being read correctly
    #    # parameters = self.request.GET #it to get all the dict of key value pairs of {query params that are passed in url}
    #    # print(parameters)
       
    def get_ordering(self):
        order = self.request.GET.get('sort')
        print(f"Retrieved order parameter: {order}")
        if order is not None:
            if order == 'asc':
                print("Ordering by date_of_birth ascending")
                return ['date_of_birth']
            elif order == 'desc':
                print("Ordering by date_of_birth descending")
                return ['-date_of_birth']
        # else:
        #     print("No ordering specified")
        #     return []
    def get_queryset(self):
        print("...",self.request.GET.get('display'))
        if self.request.GET.get('display')=='lead':
            query=self.model.objects.filter(group_lead__isnull=True)
            print("query:  ",query)
            return query
        else:
            print("Not recied")
            return super().get_queryset()
    # def get_queryset(self):
    #     print(self.kwargs)
    #     query=Student.objects.all()
    # #     # if  kwargs=='asc':
    # #     #     query=Student.objects.all().order_by('-date_of_birth')
    # #     # else:
    # #    # query=Student.objects.all().order_by('date_of_birth')
    #     return query

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['display']=self.kwargs.get('display')
        context['display']=self.request.GET.get('display')       
        return context
    
class updateStudent(UpdateView):
    model=Student
    template_name='newUpdateviewClass.html'
    fields=['first_name','last_name','roll_number','teacher','date_of_birth']
    success_url = reverse_lazy('students') 
    # def get_context_data(self, **kwargs):
    #         context=super().get_context_data(**kwargs)
    #         student_To_update=self.model.objects.get(id=self.kwargs.get('pk'))
    #         enrolled_courses=[enroll.course.course_name for enroll in student_To_update.enrolled.all()]
    #         context['enrolled_courses']=enrolled_courses
    #         context['courses_to_enroll']=course.objects.all()
    #         print(context)
    #         return context    
    # def form_valid(self, form):
    #     # Debug: Print form data to ensure it's being processed
    #     print("Form data:", form.cleaned_data)
    #     return super().form_valid(form)   
class StudentUpdateView(UpdateView):
    model = Student
    fields = ['first_name', 'last_name', 'date_of_birth', 'roll_number', 'teacher']
    template_name = 'newUpdateviewClass.html'
    success_url = reverse_lazy('students') 

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['teachers']=teacher.objects.all()
        student_To_update=self.model.objects.get(id=self.kwargs.get('pk'))
        enrolled_courses=[enroll.course.course_name for enroll in student_To_update.enrolled.all()]
        context['enrolled_courses']=enrolled_courses
        context['courses_to_enroll']=course.objects.all()
        print(context)
        return context  
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        student_object = self.object  # The current student object
        #student_obj_original=Student.objects.get(id=student_object.id)
        print("Form data:", form)
        # Print statements to debug
        print("Student Name:", student_object, "Retrieved Student:", self.get_object())
        print("Assigned Group Lead:", student_object.group_lead)  # Check if group_lead is initially None
        
        updated_course_name_list = self.request.POST.getlist('Avail_course_name')
        already_enrolled_courses = [enroll.course.course_name for enroll in student_object.enrolled.all()]

        print("Already Enrolled Courses:", already_enrolled_courses)
        print("Updated Course Name List:", updated_course_name_list)

        for course_obj in course.objects.all():
            if course_obj.course_name in updated_course_name_list and (course_obj.course_name not in already_enrolled_courses):
                Enrollment.objects.create(student=student_object, course=course_obj, enrollment_date='2000-1-1')
            elif course_obj.course_name not in updated_course_name_list and (course_obj.course_name in already_enrolled_courses):
                enrollment_instance = student_object.enrolled.get(course=course_obj.id)
                print("Deleting Enrollment:", enrollment_instance)
                enrollment_instance.delete()

        # Assigning a team lead to the student if none exists
        print("Checking if group lead needs assignment...")
        if student_object.group_lead is None:
            all_students = Student.objects.all()
            if all_students.exists():
                students_without_group_leads = Student.objects.filter(group_lead__isnull=True)
                print("Students without group leads:", students_without_group_leads)

                if students_without_group_leads.exists():
                    students_list = list(students_without_group_leads)
                    
                    while True:
                        lead = random.choice(students_list)
                        if lead == student_object.group_lead:
                            continue
                        else:
                            student_object.group_lead = lead
                            student_object.save()  # Save immediately after assignment
                            student_object.refresh_from_db() 
                            print("Assigned Group Lead:", student_object.group_lead)
                            break
                else:
                    print("All students have group leads.")

        # Verify the final state of the student object
        print("Final Group Lead for Student:", student_object.group_lead)

        return super().form_valid(form)
    

#detail view to that returns a object id as url paramater and used to get only 1 object
class LeadtDetailView(DetailView):
    model=Student
    context_object_name='student'
   #by default: pk_url_kwarg='pk'
    slug_field='id'
    slug_url_kwarg='slug_paramater'
    template_name='lead_detail.html'

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        student_To_update=self.model.objects.get(id=self.kwargs.get('slug_paramater'))
        enrolled_courses=[enroll.course.course_name for enroll in student_To_update.enrolled.all()]
        context['enrolled_courses']=enrolled_courses
        context['courses_to_enroll']=course.objects.all()
        # The student instance is already provided by the DetailView
        print(context['student'])
        student_instance = context['student']
        
        # Get all students who are under the current group lead
        context['group_members'] = student_instance.group_students.all()
        print(context,self.get_object().id)
        return context
    def get_queryset(self) :
        # group_lead_is=self.get_object()
        # query=group_lead_is.group_students.all()
        # print(query)
        return super().get_queryset()
    

class createClassView(CreateView):
    model=course
    fields=['course_name']
    template_name='addCourse.html'
    success_url = '/'
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        #it is  called when the form is submittd correctly.
        #you can define the after submission logic, By default, it saves the form and then redirects the user to a success URL.
        print(form.cleaned_data)
        print("kya baat ha bhai naya course aagya ha")
        return super().form_valid(form)
