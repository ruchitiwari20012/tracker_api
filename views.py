
from urllib import request
from .serializers import *
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from .models import *
from rest_framework.decorators import api_view
import json
import jwt
from datetime import datetime,timedelta
from rest_framework import status
from .helpers import *

# calling functions




SECRET_KEY_JWT = '7f39379db36b12a2811caf4e2b19171477326955bd94c37b55757d7df6fbc5c2'

@api_view(['GET','POST'])
def login(request):
    try:
        if request.method=='GET':
            mobile_no = request.query_params.get('mobile_no',None)
            if mobile_no is not None:
                user_obj = User.objects.get(mobile_no=mobile_no)
                user_serializer = UserSerializer(user_obj)
                return JsonResponse(user_serializer.data)
            else:
                return JsonResponse({'msg':'Mobile number missing.'},status=status.HTTP_400_BAD_REQUEST)

        

        elif request.method =='POST':
            user_data = JSONParser().parse(request)
            print("you will get the detail of user_data",user_data)
            user_serializer = UserSerializer(data=user_data)
            
            if user_serializer.is_valid():
                mobile_no= user_data['mobile_no']
                if User.objects.filter(mobile_no = mobile_no).exists():
                    user_obj = User.objects.get(mobile_no=mobile_no)
                    user_id = str(user_obj.id)
                    user_access = AccessToken.objects.get(user = user_id)
                    user_access.delete()
                else:
                    user_obj = user_serializer.save()
                    user_id =  str(user_obj.id)
                    

                expire_time = (datetime.now()+timedelta(days=30)).timestamp()
                access_token = jwt.encode({'id':user_id,"exp":expire_time,'type':'access'},SECRET_KEY_JWT, algorithm='HS256')
                access_token_obj = AccessToken(token = access_token,expire_time = expire_time,is_valid = True,user = user_obj)
                access_token_obj.save()
                return JsonResponse({"access_token":access_token},status=status.HTTP_200_OK)
    except:
        return JsonResponse({'msg':'Something went wrong.'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET','POST'])
def user_detail_view(request):
    #try:
        #token =request.META['HTTP_AUTHORIZATION'].replace("Bearer ","")
        user_id = token_compare(request)
        if  not user_id:
            return JsonResponse({"msg":"Invalid access token."},status=status.HTTP_401_UNAUTHORIZED)
        

        #access_token = jwt.decode(token,SECRET_KEY_JWT, algorithms='HS256')

        if request.method == 'GET': 
            user_obj = User.objects.get(id=user_id)
            user_details_serializer = UserDetailsSerializer(user_obj)
            return JsonResponse(user_details_serializer.data,safe=False)
            
            
        elif request.method == 'POST':
            data = request.data
            id = User.objects.get(id=user_id)
            user_details_serializer = UserDetailsSerializer(id,data=data)
            if user_details_serializer.is_valid():
                user_details_serializer.save()
                return JsonResponse({'msg':'User details updated successfully.'},status=status.HTTP_201_CREATED) 
    #except:
        #return JsonResponse({'msg':'Something went wrong.'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
