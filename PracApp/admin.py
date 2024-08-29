from django.contrib import admin

from PracApp.models import user


class customizeAdmin(admin.ModelAdmin):
    list_display=('name','age','country',)


admin.site.register(user,customizeAdmin)


# Register your models here.
