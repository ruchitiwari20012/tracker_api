from cgi import MiniFieldStorage
from unittest.util import _MAX_LENGTH
from django.db import models
import uuid

# Create your models here.
class User(models.Model):
    id = models.UUIDField(primary_key= True,default= uuid.uuid4,editable= False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    role = models.CharField(max_length=50)
    organisation = models.ForeignKey('Organisation', models.DO_NOTHING, db_column='organisation',null=True) 
    mobile_no = models.CharField(max_length=50)
    profile_photo = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'User'

class Organisation(models.Model):
    id = models.UUIDField(primary_key= True,default= uuid.uuid4,editable= False)
    name = models.CharField(max_length=50)

    class Meta:
        managed = True
        db_table = 'organisation'    

class AccessToken(models.Model):
    id = models.UUIDField(primary_key= True,default= uuid.uuid4,editable= False)
    token = models.CharField(max_length=500)
    expire_time = models.CharField(max_length=50)
    is_valid = models.CharField(max_length=50)
    user = models.ForeignKey(User, models.DO_NOTHING, db_column='user')


    class Meta:
        managed = True
        db_table = 'access_token'

class TruckManufacturer(models.Model):
    id = models.UUIDField(primary_key= True,default= uuid.uuid4,editable= False)
    name = models.CharField(max_length=50)
    manufactured_date = models.DateField(blank=True, null=True)
    truck_number = models.CharField(max_length=50)
    model_number = models.CharField(max_length=50)
    vehicle_class = models.CharField(max_length=50)
    vehicle_type = models.CharField(max_length=50)
    alerts = models.CharField(max_length=50)

    class Meta:
        managed = True
        db_table = 'truck_manufacturer'

class TruckEmissionNorms(models.Model):
    id = models.UUIDField(primary_key= True,default= uuid.uuid4,editable= False)
    co = models.CharField(max_length=50)
    co_corrected = models.CharField(max_length=50)
    hc = models.CharField(max_length=50)
    co2 = models.CharField(max_length=50)
    o2 = models.CharField(max_length=50)
    rpm = models.CharField(max_length=50)
    oil_temperature = models.CharField(max_length=50)

    class Meta:
        managed = True
        db_table = 'truck_emission_norms'

class TruckHealthStatus(models.Model):
    id = models.UUIDField(primary_key= True,default= uuid.uuid4,editable= False)
    status = models.CharField(max_length=50)
    last_service = models.CharField(max_length=50)
    service_station = models.CharField(max_length=50)
    service_contact = models.CharField(max_length=50)

    class Meta:
        managed = True
        db_table = 'truck_health_status'

class TruckCapacity(models.Model):
    id = models.UUIDField(primary_key= True,default= uuid.uuid4,editable= False)
    unladen_weight = models.CharField(max_length=50)
    horse_power = models.CharField(max_length=50)
    wheel_base = models.CharField(max_length=50)
    cylinders = models.CharField(max_length=50)
    fuel = models.CharField(max_length=50)
    mileage = models.CharField(max_length=50)
    size = models.CharField(max_length=50)

    class Meta:
        managed = True
        db_table = 'truck_capacity'
    

class Truck(models.Model):
    id = models.UUIDField(primary_key= True,default= uuid.uuid4,editable= False)
    registration_number = models.CharField(max_length=50)
    vin = models.CharField(max_length=50)
    manufacturing_info = models.ForeignKey(TruckManufacturer, models.CASCADE, db_column='manufacturing_info',null=True)
    emission_norms = models.ForeignKey(TruckEmissionNorms, models.CASCADE, db_column='emission_norms',null=True)
    health_status = models.ForeignKey(TruckHealthStatus, models.CASCADE, db_column='health_status',null=True)
    capacity = models.ForeignKey(TruckCapacity, models.CASCADE, db_column='capacity',null=True)
    rc_status = models.CharField(max_length=50)
    insurance_end_date = models.DateField(blank=True, null=True)
    organisation = models.ForeignKey(Organisation, models.DO_NOTHING, db_column='organisation',null=True) 

    class Meta:
        managed = True
        db_table = 'truck'

class FeedBack(models.Model):
    
    feedback = models.CharField(max_length = 500)
    user_feedback = models.ForeignKey(User, models.DO_NOTHING,db_column='user')

    class Meta:
        managed = True
        db_table = 'FeedBack'
