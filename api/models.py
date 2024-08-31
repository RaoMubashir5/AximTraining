from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Webuser(models.Model):
    user_name=models.CharField(max_length=30)
    user_email=models.EmailField(unique=True,default="user@gmail.com")
    user_age=models.IntegerField()
    user_country=models.CharField(max_length=20,null=True,blank=True)
    created_by=models.ForeignKey(User,on_delete=models.CASCADE,unique=True)   # it is  the built in User class that 
    
    def __str__(self) -> str:
        return f'{self.user_name}'
    class Meta:
        ordering=['user_age']
        verbose_name="User Model"
    