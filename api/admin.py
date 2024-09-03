from django.contrib import admin
from api.models import Webuser

# Register your models here.

class customizeAdminManager(admin.ModelAdmin):
    list_display=['id','username','email','created_by']

admin.site.register(Webuser,customizeAdminManager)


