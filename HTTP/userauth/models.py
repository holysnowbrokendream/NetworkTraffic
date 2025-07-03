from django.db import models

# Create your models here.

class Users(models.Model):
    id = models.CharField(primary_key=True, max_length=64)
    pwd = models.CharField(max_length=128)

    class Meta:
        db_table = 'users'
