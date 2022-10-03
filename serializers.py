from rest_framework import serializers
from tracker_api.models import *
from rest_framework.validators import UniqueValidator

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['mobile_no']
        
class UserDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["first_name","last_name","email","role","profile_photo"]

class OrganisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = '__all__'
        read_only_fields  = ['id']
        extra_kwargs = {
                'name': {'validators': [UniqueValidator(queryset=Organisation.objects.all(),message="Organisation already exists.")]}
            }


class TruckManufacturerSerializer(serializers.ModelSerializer):

    class Meta:
        model = TruckManufacturer
        exclude = ['id']

class TruckEmissionNormsSerializer(serializers.ModelSerializer):

    class Meta:
        model = TruckEmissionNorms
        exclude = ['id']

class TruckHealthStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = TruckHealthStatus
        exclude = ['id']

class TruckCapacitySerializer(serializers.ModelSerializer):

    class Meta:
        model = TruckCapacity
        exclude = ['id']

class TruckSerializer(serializers.ModelSerializer):

    manufacturing_info = TruckManufacturerSerializer()
    emission_norms = TruckEmissionNormsSerializer()
    health_status = TruckHealthStatusSerializer()
    capacity = TruckCapacitySerializer()
    id = serializers.CharField(required=False)

    class Meta:
        model = Truck
        fields = '__all__'

    def create(self,validated_data):
        manufacturing_info = TruckManufacturer.objects.create(**validated_data.pop('manufacturing_info'))
        emission_norms = TruckEmissionNorms.objects.create(**validated_data.pop('emission_norms'))
        health_status = TruckHealthStatus.objects.create(**validated_data.pop('health_status'))
        capacity = TruckCapacity.objects.create(**validated_data.pop('capacity'))
        return Truck.objects.create(**validated_data,manufacturing_info=manufacturing_info,emission_norms=emission_norms,health_status=health_status,capacity=capacity)
    
    def update(self,instance,validated_data):
        TruckManufacturer.objects.filter(id=instance.manufacturing_info.id).update(**validated_data.pop('manufacturing_info'))
        TruckEmissionNorms.objects.filter(id=instance.emission_norms.id).update(**validated_data.pop('emission_norms'))
        TruckHealthStatus.objects.filter(id=instance.health_status.id).update(**validated_data.pop('health_status'))
        TruckCapacity.objects.filter(id=instance.capacity.id).update(**validated_data.pop('capacity'))
        Truck.objects.filter(id=instance.id).update(**validated_data)
        return instance

class TruckListSerializer(serializers.ModelSerializer):

    manufacturing_info = TruckManufacturerSerializer()
    emission_norms = TruckEmissionNormsSerializer()
    health_status = TruckHealthStatusSerializer()
    capacity = TruckCapacitySerializer()

    class Meta:
        model = Truck
        fields = '__all__'

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedBack
        fields = '__all__'
