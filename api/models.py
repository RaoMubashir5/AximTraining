from django.db import models

# Create your models here.
class User(models.Model):
    user_name=models.CharField(max_length=30)
    user_email=models.EmailField(unique=True,default="user@gmail.com")
    user_age=models.IntegerField()
    user_country=models.CharField(max_length=20,null=True,blank=True)
    
    def __str__(self) -> str:
        return f'{self.user_name}'
    class Meta:
        ordering=['user_age']
    