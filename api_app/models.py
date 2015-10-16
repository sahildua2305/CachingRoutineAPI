from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class FlatchatUser(models.Model):
	user = models.OneToOneField(User)
	data = models.CharField(max_length=2048)