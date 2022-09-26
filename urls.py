from django.urls import path, include
from tracker_api import views




urlpatterns = [
    path('login/', views.login),
    path('user_detail/', views.user_detail_view),
    #path('token/', views.token_compare)
    ]


