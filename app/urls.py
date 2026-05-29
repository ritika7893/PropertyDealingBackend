from django.urls import path

from .views import ContactAPIView, LoginUser, PropertyDetailAPIView, PropertyListCreateAPIView, RefreshTokenAPI
urlpatterns = [
   
    path('login/', LoginUser.as_view()),
    path('refresh-token/', RefreshTokenAPI.as_view()),
    path("properties/",PropertyListCreateAPIView.as_view(),name="property-list-create"),

    path("properties/<int:pk>/",PropertyDetailAPIView.as_view(),name="property-detail"),
    path("contact/",ContactAPIView.as_view(),name="contact"),
    

]