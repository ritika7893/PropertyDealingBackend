from django.urls import path

from .views import ContactAPIView, LoginUser, PropertyBulkCreateAPIView, PropertyDetailAPIView, PropertyListCreateAPIView, RefreshTokenAPI, TestimonialDetailAPIView, TestimonialListCreateAPIView
urlpatterns = [
   
    path('login/', LoginUser.as_view()),
    path('refresh-token/', RefreshTokenAPI.as_view()),
    path("properties/",PropertyListCreateAPIView.as_view(),name="property-list-create"),

    path("properties/<int:pk>/",PropertyDetailAPIView.as_view(),name="property-detail"),
    path("contact/",ContactAPIView.as_view(),name="contact"),
    path("properties/bulk-create/",PropertyBulkCreateAPIView.as_view(),name="property-bulk-create"),
    path('testimonials/', TestimonialListCreateAPIView.as_view(), name='testimonial-list-create'),
    path('testimonials/<int:pk>/', TestimonialDetailAPIView.as_view(), name='testimonial-detail'),
]