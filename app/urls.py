from django.urls import path

from .views import LoginUser, RefreshTokenAPI
urlpatterns = [
   
    path('login/', LoginUser.as_view()),
    path('refresh-token/', RefreshTokenAPI.as_view()),
    

]