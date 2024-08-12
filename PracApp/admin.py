from django.contrib import admin

# Register your models here.
from PracApp.models import *

class admin_customize(admin.ModelAdmin):
    """"these are the customized functionalities of the django admin site """
    
    # all the instances of the Student model with these Fields
    list_display=('first_name','last_name','date_of_birth',)  

    # Added filters for these two fields
    list_filter = ('date_of_birth','first_name',)    

    #Search option also implemented and Search would be on the basis of "first_name"          
    search_fields=('first_name',)                             

    #apply order listing of the records
    ordering=('-first_name',)                     
    
#regitering the models with the admin site
admin.site.register(Student,admin_customize)                   
