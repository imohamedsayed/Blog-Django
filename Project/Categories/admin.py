from django.contrib import admin
from . import models
# Register your models here.

class AdminCat(admin.ModelAdmin):
    list_display = ['cat_name','cat_status']
    list_editable=['cat_status']
    search_fields=['cat_name']
    list_filter = ['cat_status']



admin.site.register(models.Categories,AdminCat)



