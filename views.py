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
from rest_framework.views import APIView
from rest_framework import generics


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
    try:
        user_id = token_compare(request)
        if  not user_id:
            return JsonResponse({"msg":"Invalid access token."},status=status.HTTP_401_UNAUTHORIZED)
        


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
    except:
        return JsonResponse({'msg':'Something went wrong.'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

class TruckDetails(APIView):
    def get(self,request):
        try:
            truck_id = request.query_params.get('id',None)
            if truck_id:
                truck_obj = Truck.objects.get(id=truck_id)
                truck_serializer = TruckSerializer(truck_obj)
                return JsonResponse(truck_serializer.data)
            else:
                return JsonResponse({'msg':'Truck id missing.'},status=status.HTTP_400_BAD_REQUEST)
        except:
            return JsonResponse({'msg':'Something went wrong.'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self,request):

        try:
            
            data = JSONParser().parse(request)
            if 'id' in data:
                truck_obj = Truck.objects.get(id=data['id'])
                truck_serializer = TruckSerializer(truck_obj,data=data)
            else:
                truck_serializer = TruckSerializer(data=data)
            if truck_serializer.is_valid():
                truck_serializer.save()
                return JsonResponse({'msg':'Truck details updated successfully.'},status=status.HTTP_201_CREATED) 
            else:
                return JsonResponse({'msg':'Invalid truck details.'},status=status.HTTP_400_BAD_REQUEST)
        except:
            return JsonResponse({'msg':'Something went wrong.'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TruckList(APIView):
    def get(self,request):
        try:
            organisation_id = request.query_params.get('id',None)
            if organisation_id:
                trucks = Truck.objects.filter(organisation=organisation_id)
                truck_serializer = TruckListSerializer(trucks,many=True)

                return JsonResponse(truck_serializer.data,safe=False)
            else:
                return JsonResponse({'msg':'Organisation id missing.'},status=status.HTTP_400_BAD_REQUEST)
        except:
            return JsonResponse({'msg':'Something went wrong.'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class OrganisationList(APIView):
    def get(self,request):
        try:
            organisations = Organisation.objects.all()
            organisation_serializer = OrganisationSerializer(organisations,many=True)

            return JsonResponse(organisation_serializer.data,safe=False)
        except:
            return JsonResponse({'msg':'Something went wrong.'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OrganisationDetails(APIView):

    def get(self,request):
        try:
            organisation_id = request.query_params.get('id',None)
            if organisation_id:
                organisation_obj = Organisation.objects.get(id=organisation_id)
                organisation_serializer = OrganisationSerializer(organisation_obj)
                return JsonResponse(organisation_serializer.data)
            else:
                return JsonResponse({'msg':'Organisation id missing.'},status=status.HTTP_400_BAD_REQUEST)
        except:
            return JsonResponse({'msg':'Something went wrong.'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self,request):
        try:
            data = JSONParser().parse(request)
            organisation_serializer = OrganisationSerializer(data=data)
            if organisation_serializer.is_valid():
                organisation_serializer.save()
                return JsonResponse({'msg':'Organisation details updated successfully.'},status=status.HTTP_201_CREATED) 
            else:
                return JsonResponse({'msg':organisation_serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        except:
            return JsonResponse({'msg':'Something went wrong.'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class FeedBackDetail(APIView):
    def get(self,request):
        #try:
            user_id = request.query_params.get('id',None)
            if user_id:
                user_obj = FeedBack.objects.get(user_feedback=user_id)
                feedback_serializer = FeedbackSerializer(user_obj)
                return JsonResponse(feedback_serializer.data)
            else:
                return JsonResponse({'msg':'user id missing.'},status=status.HTTP_400_BAD_REQUEST)
        #except:
            #return JsonResponse({'msg':'Something went wrong.'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        #try:
            #feedback = FeedBack.objects.all()
            #feedback_serializer = FeedbackSerializer(feedback,many=True)

            #return JsonResponse(feedback_serializer.data)
        #except:
            #return JsonResponse({'msg':'Something went wrong.'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self,request):
        try: 
                
                data = JSONParser().parse(request)
                if 'id' in data:
                    feeback_obj = FeedBack.objects.get(id=data['id'])
                    user_feedback_serializer = FeedbackSerializer(feeback_obj,data=data)
                else:
                    user_feedback_serializer = FeedbackSerializer(data=data)
                if user_feedback_serializer.is_valid():
                    user_feedback_serializer.save()
                    return JsonResponse({'msg':'User feedback updated successfully.'},status=status.HTTP_201_CREATED) 
                else:
                    return JsonResponse({'msg':'feedback details are not save'},status=status.HTTP_400_BAD_REQUEST)
        except:
                return JsonResponse({'msg':'Something went wrong.'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


