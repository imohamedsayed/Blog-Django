from datetime import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

STATUS_MEG = [
    ('1', 'active'),
    ('0', 'nonactive'),
]


# Create your models here.
class Customer(models.Model):
    user_first = models.CharField(max_length=100)
    user_last = models.CharField(max_length=100)
    user_img = models.ImageField(upload_to='photo/',default='photo/265261750_2137137816444812_3009440320167266103_n.jpg')
    user_email = models.EmailField()
    user_pass = models.CharField(max_length=50)
    user_date_on = models.DateField(default=timezone.now)

    def __str__(self):
        return self.user_first


class message(models.Model):
    meg_details = models.TextField()
    meg_status = models.CharField(choices=STATUS_MEG,default=('0', 'nonactive'),max_length=10)
    meg_date = models.DateField(default=timezone.now)
    cust_id = models.ForeignKey(Customer,on_delete=models.CASCADE)

    def __str__(self):
        return self.meg_details


class reply(models.Model):
    re_details = models.TextField()
    meg_id = models.ForeignKey(message,on_delete=models.CASCADE)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    re_date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.re_details

