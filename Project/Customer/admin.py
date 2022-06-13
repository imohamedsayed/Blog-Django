from django.contrib import admin
from . import models

# Register your models here.

 
class CustomerAdmin(admin.ModelAdmin):
     list_display= ['user_first','user_email','user_pass']
     list_editable =['user_email','user_pass']
     search_fields = ['user_first']
     
class ReplyAdmin(admin.ModelAdmin):
     list_display= ['re_details','user_id']
     search_fields = ['re_details']
     list_filter = ['user_id']
     

     
admin.site.register(models.Customer,CustomerAdmin)
admin.site.register(models.reply,ReplyAdmin)