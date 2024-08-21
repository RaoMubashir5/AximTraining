from django.db import models
from django.db.models import Q
# Create your models here.

class Person(models.Model):
    first_name = models.CharField(max_length=50,verbose_name="First Name")    
    last_name = models.CharField(max_length=50,verbose_name="Last Name")
    date_of_birth = models.DateField(verbose_name="Date of Birth")
    #if we do not use verbose it will automatically capitilized the first alpabet, and remove the '_' underscore.to make it easy readable

    class Meta:
        """"meta class is class that is used to perform many functionalities like,
            ordering the instances on based of any field,adding permissions to the field,
            making any class Abstract(this is just virtual class Would not be in database, but the class that inherits it)."""
        
        abstract=True
        ordering=['first_name']

class Student(Person):
    """This class inheriting the Abstract class and have all that abstract class functionalities ,
       This make the less redundant code, and follow the [Do not repeat youself principle of coding]"""
    
    roll_number=models.IntegerField(verbose_name="Roll Number")

    #if a alumni Category got deleted than the students with that Tag would't be deteled but the :Alumni field would be set to null instead.
    group_lead=models.ForeignKey('self',on_delete=models.SET_NULL, related_name="group_students",null=True,blank=True,verbose_name="Group Head") 
    teacher=models.ForeignKey('teacher',on_delete=models.CASCADE,verbose_name="Teachers",null=True,blank=True,related_name="teachers")  #,verbose_name="Group Leads"
    #course=models.ForeignKey('course',on_delete=models.SET_NULL,related_name="Course",null=True,blank=True)
    
    class Meta:
        verbose_name="Registered Student"
    def __str__(self) -> str:
        return self.first_name
    

class teacher(models.Model):
    """there would be the many to retation between the students and teacher"""
    name=models.CharField(max_length=15,verbose_name="Teachers")
    def __str__(self) -> str:
        return self.name
    

class course(models.Model):
    course_name=models.CharField(max_length=30)
    student=models.ManyToManyField(Student,through='Enrollment',)

    def __str__(self) -> str:
        return self.course_name
    
    # they are allowed in django in many to many relation ,
    # we have defoon a through table to do so

    # class Meta:
    #     unique_together = ('student', 'course_name',) 

   

# Enrollment model as the Through model;;it is now custom django intermediatory table for many to many relation,
class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE,verbose_name="Enrolled Students",related_name="enrolled")
    course = models.ForeignKey(course, on_delete=models.CASCADE,related_name="enrolled")
    enrollment_date=models.DateField(verbose_name="Date of Enrollment")

    class Meta:
        unique_together = ('student', 'course')
        verbose_name = "Enrollment"

    def __str__(self):
        return f"{self.student} in {self.course}"