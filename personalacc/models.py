from django.db import models
from django.contrib.auth.models import User
from stockrouter.models import Financial
# Create your models here.
class Personal_Portfolio(models.Model):
    user=models.ForeignKey(User,to_field='username',on_delete=models.CASCADE)
    stocks=models.ManyToManyField(Financial)
