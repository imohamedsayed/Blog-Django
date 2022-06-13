from django.db import models
from django.db.models.base import Model
from django.contrib.auth.models import User

# Create your models here.

STATUS_CAT = [
    ('1', 'active'),
    ('0', 'nonactive'),
]

class Categories(models.Model):
    cat_name = models.CharField(max_length=100,unique=True)
    cat_status = models.CharField(choices=STATUS_CAT,default=(1,'active'),max_length=10)
    cat_user = models.ForeignKey(User,on_delete=models.CASCADE)


    def __str__(self):
        return self.cat_name