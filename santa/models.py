from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=100)


class Ban(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE)
    target = models.IntegerField
