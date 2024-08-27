from django.contrib import admin
from api.models import User

# Register your models here.

class customizeAdminManager(admin.ModelAdmin):
    list_display=['id','user_name','user_email','user_age','user_country']

admin.site.register(User,customizeAdminManager)
