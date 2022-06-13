from django.contrib import admin
from . import models
# Register your models here.

class AdminPost(admin.ModelAdmin):
    list_display=['post_title','user_id','post_status','cat_id','post_view']
    list_editable =['post_status','user_id','cat_id','post_view']
    search_fields= ['post_title']
    list_filter = ['cat_id','user_id']



class AdminComment(admin.ModelAdmin):
    list_display=['com_details','com_status','cust_id','post_id']
    list_editable =['com_status']
    search_fields= ['com_details']
    list_filter = ['cust_id','post_id']



admin.site.register(models.post,AdminPost)
admin.site.register(models.comment,AdminComment)
