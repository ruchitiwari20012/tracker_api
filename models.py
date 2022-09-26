from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.
class User(models.Model):
    #id = models.CharField(primary_key=True, max_length=50)
    id = models.UUIDField(primary_key= True,default= uuid.uuid4,editable= False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    role = models.CharField(max_length=50)
    organisation_field = models.ForeignKey('Organisation', models.DO_NOTHING, db_column='organisation',null=True)  # Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    mobile_no = models.CharField(max_length=50)
    profile_photo = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'User'

class Organisation(models.Model):
    id = models.UUIDField(primary_key= True,default= uuid.uuid4,editable= False)
    name = models.CharField(max_length=50)
    truks = models.CharField(max_length=50)

    class Meta:
        managed = True
        db_table = 'organisation'    

class AccessToken(models.Model):
    id = models.UUIDField(primary_key= True,default= uuid.uuid4,editable= False)
    token = models.CharField(max_length=500)
    expiretime = models.CharField(max_length=50)
    isvalid = models.CharField(max_length=50)
    user = models.ForeignKey(User, models.DO_NOTHING, db_column='user')


    class Meta:
        managed = True
        db_table = 'access_token'