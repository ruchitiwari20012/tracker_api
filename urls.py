from django.urls import path, include
from tracker_api import views




urlpatterns = [
    path('login/', views.login),
    path('user_detail/', views.user_detail_view),
    path('truck_details/',views.TruckDetails.as_view()),
    path('truck_list/',views.TruckList.as_view()),
    path('organisation_details/',views.OrganisationDetails.as_view()),
    path('organisation_list/',views.OrganisationList.as_view()),
    path('user_feedback/',views.FeedBackDetail.as_view())
    ]
