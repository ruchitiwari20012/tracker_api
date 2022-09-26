
from os import access
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
import tracker_api
from .models import AccessToken, User
from .serializers import UserSerializer
from .serializers import UserSerializer1
from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from .models import User,AccessToken
from rest_framework.decorators import api_view
import base64
import json
import jwt
import requests
import uuid
import datetime 
#from datetime import date
# timestamp
#ts = 1667260800

# convert to datetime
#dt = datetime.fromtimestamp(ts)
#print("The date and time is:", dt)



 
# ct stores current time
# ct = datetime.datetime.now() 
# print("current time in Timestamp",ct,ct.timestamp())
# new = ct + datetime.timedelta(days=30)
# print("new time in Timestamp",new, new.timestamp())
# # ts store timestamp of current time
# ts = new.timestamp()
# print(ts)


#dt = datetime.now()
#ts = datetime.timestamp(dt)
#print("Timestamp is:", ts)
#dt = datetime(year=2022, month=2, day=17, hour=13, minute=47, second=34)

#date1 = date(2022, 11, 2)
#print("Date is :", date1)

#class UserApiView(APIView):
    # add permission to check if user is authenticated
    #permission_classes = [permissions.IsAuthenticated]

@api_view(['GET','POST'])
def user_list(request):
    if request.method=='GET':
        tracker_api=User.objects.all()

        mobile_no = request.query_params.get('mobile_no',None)
        if mobile_no is not None:
            tracker_api = tracker_api.filter(mobile_no__icontains=mobile_no)

        tracker_api_serializer = UserSerializer(tracker_api, many=True)
        return JsonResponse(tracker_api_serializer.data, safe=False)

    elif request.method =='POST':
        tracker_api_data = JSONParser().parse(request)
        tracker_serializer = UserSerializer(data=tracker_api_data)

        if tracker_serializer.is_valid():
            #tracker_serializer.save()
            user_obj = tracker_serializer.save()
            cc =  str(user_obj.id)
            #AccessToken.objects.get(user_id=User.id)
            ct = datetime.datetime.now() 
            print("current time in Timestamp",ct,ct.timestamp())
            new = ct + datetime.timedelta(days=30)
            print("new time in Timestamp",new, new.timestamp())
            # ts store timestamp of current time
            ts = new.timestamp()
            print(ts)
            #printing mobile data
            print(tracker_serializer.data)

            encoded_jwt = jwt.encode({'id':cc,"exp":ts,'type':'access'},'7f39379db36b12a2811caf4e2b19171477326955bd94c37b55757d7df6fbc5c2', algorithm='HS256')
            print(encoded_jwt)
            print(len(encoded_jwt))
            
            access_table = AccessToken(token = encoded_jwt,expiretime = ts,isvalid = True,user = user_obj)
            access_table.save()
            
              
            return JsonResponse({"access_token":encoded_jwt},status=status.HTTP_201_CREATED)
        return JsonResponse(tracker_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST'])
def user_detail_view(request):
    #try:
    print("here")
    #tracker_api = User.objects.all()
    token =request.META['HTTP_AUTHORIZATION'].replace("Bearer ","")
    print(token)
    decoded_jwt = jwt.decode(token,'7f39379db36b12a2811caf4e2b19171477326955bd94c37b55757d7df6fbc5c2', algorithms='HS256')
    #id1=decoded_jwt['id']
    #request.META['Authorization']   
    if request.method == 'GET': 
        user_obj = User.objects.get(id=decoded_jwt['id'])
        tracker_api_serializer1 = UserSerializer1(user_obj)
        return JsonResponse(tracker_api_serializer1.data,safe=False)
        
        
    elif request.method == 'POST':
        print('Hello')
        #tracker_api_data = JSONParser().parse(request)
        data = request.data
        id = User.objects.get(id=decoded_jwt['id'])
        #data['id'] = id.pk
        #tracket_api_serializer1 = UserSerializer1(data=tracker_api_data)
        tracker_api_serializer1 = UserSerializer1(id,data=data)
        if tracker_api_serializer1.is_valid():
            tracker_api_serializer1.save()
            print('in this line')
            print(tracker_api_serializer1.data)
            return JsonResponse(tracker_api_serializer1.data,status=status.HTTP_201_CREATED) 
        return JsonResponse(tracker_api_serializer1.errors, status=status.HTTP_400_BAD_REQUEST)
    
