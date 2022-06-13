from datetime import datetime
from django.db import models
from django.db.models.base import Model
from Categories import models as modelsCat
from django.contrib.auth.models import User
from Customer.models import Customer
from django.utils import timezone


STATUS_POST = [
    ('1', 'active'),
    ('0', 'nonactive'),
]


def image_upload(instance,filename):
    imagename , extsion = filename.split(".")
    return "postImage/%s.%s"%(instance.post_title,extsion)


# Create your models here
class post(models.Model):
    post_title = models.CharField(max_length=100,unique=True)
    post_details = models.TextField()
    post_status = models.CharField(choices=STATUS_POST,default=(1,'active'),max_length=10)
    post_view = models.IntegerField(default=0)
    post_photo = models.ImageField(upload_to=image_upload)
    cat_id = models.ForeignKey(modelsCat.Categories,on_delete=models.CASCADE)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    post_date = models.DateField(default=timezone.now)


    def __str__(self):
        return self.post_title

class comment(models.Model):
    com_details = models.CharField(max_length=150)
    com_date = models.DateField(default=timezone.now)
    com_status = models.CharField(choices=STATUS_POST,default=(0,'nonactive'),max_length=10)
    cust_id = models.ForeignKey(Customer,on_delete=models.CASCADE)
    post_id = models.ForeignKey(post,on_delete=models.CASCADE)

    def __str__(self):
        return self.com_details


