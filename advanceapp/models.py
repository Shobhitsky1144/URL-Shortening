from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class shorturl(models.Model):
    original_url=models.URLField(blank=False)
    short_query=models.CharField(blank=False,max_length=8)
    visits=models.IntegerField(default=0)
    user=models.ForeignKey(User,on_delete=models.CASCADE)

class UserDetail(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    mobile=models.CharField(max_length=10,null=True)
    image=models.ImageField(upload_to='profile_pics',null=True,default='pic.png')
