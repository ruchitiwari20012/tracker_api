from rest_framework import serializers
#from django.contrib.auth import User
from tracker_api.models import User
from rest_framework.validators import UniqueTogetherValidator
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['mobile_no']
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=['mobile_no']
            )
        ]
        
class UserSerializer1(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["first_name","last_name","email","role","profile_photo"]
        
        
# class UserSerializer(RetrieveAPIView):
#     pagination_class = (IsAuthenticated,)
#     serializer_class = UserSerializer

#     def get_object(self):
#         return self.request.user
  

 

