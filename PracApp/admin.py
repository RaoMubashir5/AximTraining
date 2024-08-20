from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.contrib.auth.models import User
# from django.contrib.auth.models import get_user_model

# Register your models here.
from PracApp.models import *

# User=get_user_model()

class customize_filter_for_students_under_eache_lead(admin.SimpleListFilter):
    """This class is customize the filter options in the filter of the admin site.
       We would override the lookup(is to define the options name, and the url send back to the queryset function).
       and queryset(which filters the data accroding to the lookup function names/options in actual ) functions in this regard."""
    
    title='Student Under Each Lead'
    parameter_name='students_under_lead'

    def lookups(self, request, model_admin) -> list[tuple[Any, str]]:

        group_leads=Student.objects.filter(group_lead__isnull=True)
        options=[
                 (g_lead.id,g_lead.first_name) for g_lead in group_leads]  
        """the first value of the tuple would be pass to queryset:
           self.value()=first Parameter"""
        new_filter=('group_leads','Group Leads')
       
        # index 0 element si stored to be appended again at the end
        return options.append(new_filter)
    def queryset(self, request: Any, queryset: QuerySet[Any]) -> QuerySet[Any] | None:

        # check what option is clicked that is defined in the lookups
        if self.value():
            print(type(self.value()),self.value())
            if self.value() == 'group_leads':
                # it return the queryset with only that student Table records that has group_lead id only 
                return queryset.filter(group_lead__isnull=True) 
            #it will filter the records of the student table with only this group_lead that's id id in self.value()
            return  queryset.filter(group_lead_id=self.value())                  
class admin_customize(admin.ModelAdmin):
    """"these are the customized functionalities of the django admin site """
    
    # all the instances of the Student model with these Fields
    list_display=('first_name','last_name','date_of_birth','group_lead','teacher',)  

    # Added filters for these two fields
    list_filter = ('date_of_birth','first_name',)   

    list_filter=(customize_filter_for_students_under_eache_lead,'teacher',) 

    #Search option also implemented and Search would be on the basis of "first_name"          
    search_fields=('first_name',)                             

    #apply order listing of the records
    ordering=('-first_name',)                

    #add another button
    list_editable=("group_lead",'teacher')     
   
class cutomize_Teacher_model(admin.ModelAdmin):
    list_display=('name',)
    

class customize_course_model(admin.ModelAdmin):
   
    list_display=('course_name',)
 
class customize_enroll_model(admin.ModelAdmin):
   
    list_display=('student','course','enrollment_date')
    list_filter=('student','course','enrollment_date')
    # def get_students(self, obj):
    #     # Filter students by the course
    #     # Return student names, each on a new line
    #     return ",".join([str(student) for student in obj.student.all()])
    # get_students.short_description = 'Enrolled Students'

#regitering the models with the admin site
admin.site.register(Student,admin_customize)
admin.site.register(teacher,cutomize_Teacher_model)   
admin.site.register(course,customize_course_model)                   
admin.site.register(Enrollment,customize_enroll_model) 