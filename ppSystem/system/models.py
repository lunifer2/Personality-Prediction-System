
from django.db import models
from django.contrib.auth.models import User
from pkg_resources import require
# Create your models here.
class UserProfile(models.Model):
    age = models.TextField(blank=False, null=False)
    phone = models.BigIntegerField(blank=False)
    gender = models.CharField(max_length=20, blank=False, null=False)
    upload_cv = models.FileField(upload_to='CV',blank=True,null=True)
    oppeness = models.PositiveSmallIntegerField(blank=False, null=False)
    conscientiousness = models.PositiveSmallIntegerField(blank=False, null=False)
    extraversion = models.PositiveSmallIntegerField(blank=False, null=False)
    agreeableness = models.PositiveSmallIntegerField(blank=False, null=False)
    neuroticism = models.PositiveSmallIntegerField(blank=False, null=False)
    user= models.ForeignKey(
        User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user_id)