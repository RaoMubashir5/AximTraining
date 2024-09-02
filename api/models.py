from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Webuser(models.Model):
    user_name=models.CharField(max_length=30,null=False,blank=False)
    user_email=models.EmailField(unique=True,default="user@gmail.com",blank=False)
    phone_number=models.CharField(unique=True,null=False,blank=False)
    user_age=models.IntegerField()
    user_country=models.CharField(max_length=20,null=True,blank=True)
    created_by=models.OneToOneField('self',on_delete=models.CASCADE)   # it is  the built in User class that 
    passwordpassword = models.CharField(null=False,blank=False)
    confirm_password = models.CharField(null=False,blank=False)
    
    def __str__(self) -> str:
        return f'{self.user_name} , {self.phone_number}'
    class Meta:
        ordering=['user_age']
        verbose_name="User Model"
    