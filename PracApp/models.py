from django.db import models

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

    class Meta:
        verbose_name="Registered Student"
