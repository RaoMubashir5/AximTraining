from django.db import models

# Create your models here.

class user(models.Model):
    name=models.CharField(max_length=20,unique=True)
    age=models.IntegerField()
    country=models.CharField(max_length=20)

    def __str__(self) -> str:
        return f'{self.name} , {self.age}'
    
  
