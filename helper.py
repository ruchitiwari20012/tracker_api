from lib2to3.pgen2 import token
from .serializers import *
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from .models import *
from rest_framework.decorators import api_view
import json
import jwt


from rest_framework import status

SECRET_KEY_JWT = '7f39379db36b12a2811caf4e2b19171477326955bd94c37b55757d7df6fbc5c2'


def token_compare(request):
    try:
        token =request.META['HTTP_AUTHORIZATION'].replace("Bearer ","")
        
        if  AccessToken.objects.filter(token = token).exists():
            token_obj = AccessToken.objects.get(token=token)
            access_token = jwt.decode(token,SECRET_KEY_JWT, algorithms='HS256')
            id=access_token['id']
            user_id  = str(token_obj.user.id)
            if id == user_id:
                return user_id
            else:
                return False
        else:
            return False
    except:
        return False
        
