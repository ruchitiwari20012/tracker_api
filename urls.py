from django.urls import path, include
from django.conf import settings
from tracker_api import views
from django.conf.urls.static import static
#from .views import (UserApiView)


urlpatterns = [
    #path('api-auth/', include('rest_framework.urls')),
    path('login_mobile/', views.user_list),
    path('user_detail/', views.user_detail_view),
    path('user_detail/:id', views.user_detail_view),


    #path('tracker_api/published', views.user_list_published),
    #path('api', UserApiView.as_view()),
    ]



