from django.contrib import admin
from api.models import Webuser

# Register your models here.

class customizeAdminManager(admin.ModelAdmin):
    list_display=['id','user_name','user_email','user_age','user_country','created_by']

admin.site.register(Webuser,customizeAdminManager)


