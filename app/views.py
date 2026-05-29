from shlex import quote
from django.utils import timezone
import random
import requests
from rest_framework.permissions import AllowAny, AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from app.models import Contact, Property, Registration
from app.permissions import IsAdminUserCustom


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from django.contrib.auth.hashers import check_password

from app.serializers import ContactSerializer, LoginUserSerializer, PropertySerializer, RefreshTokenSerializer


# ================= REGISTER USER =================

class LoginUser(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request):

        serializer = LoginUserSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({
                "status": False,
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        mobile_number = serializer.validated_data["mobile_number"]
        password = serializer.validated_data["password"]

        try:

            # ================= ADMIN LOGIN =================
            if (
                mobile_number == "9999999999"
                and password == "admin@123"
            ):

                admin_user, created = Registration.objects.get_or_create(
                    mobile_number="9999999999",
                    defaults={
                        "name": "Admin",
                        "role": "admin",
                        "is_staff": True,
                        "is_superuser": True,
                    }
                )

                # Set password if not already set
                admin_user.set_password("admin@123")
                admin_user.save()

                refresh = RefreshToken.for_user(admin_user)

                return Response({
                    "status": True,
                    "message": "Admin Login Successful",

                    "user_id": admin_user.user_id,

                    "role": admin_user.role,

                    "access_token": str(refresh.access_token),

                    "refresh_token": str(refresh)

                }, status=status.HTTP_200_OK)

            # ================= NORMAL USER LOGIN =================
            user = Registration.objects.get(
                mobile_number=mobile_number
            )

            if check_password(password, user.password):

                refresh = RefreshToken.for_user(user)

                return Response({
                    "status": True,
                    "message": "Login Successful",

                    "user_id": user.user_id,

                    "role": user.role,

                    "access_token": str(refresh.access_token),

                    "refresh_token": str(refresh)

                }, status=status.HTTP_200_OK)

            return Response({
                "status": False,
                "message": "Invalid Password"
            }, status=status.HTTP_400_BAD_REQUEST)

        except Registration.DoesNotExist:

            return Response({
                "status": False,
                "message": "User not found"
            }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:

            return Response({
                "status": False,
                "message": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# ================= REFRESH TOKEN =================
class RefreshTokenAPI(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):

        serializer = RefreshTokenSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({
                "status": False,
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        refresh_token = serializer.validated_data["refresh_token"]

        try:
            refresh = RefreshToken(refresh_token)

            return Response({
                "status": True,
                "access_token": str(refresh.access_token)
            }, status=status.HTTP_200_OK)

        except TokenError as e:

            error_message = str(e)

            if "expired" in error_message.lower():
                return Response({
                    "status": False,
                    "message": "Refresh token expired"
                }, status=status.HTTP_401_UNAUTHORIZED)

            return Response({
                "status": False,
                "message": "Invalid refresh token"
            }, status=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            return Response({
                "status": False,
                "message": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class PropertyListCreateAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUserCustom]
    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return super().get_permissions()

    def get(self, request):
        properties = Property.objects.all().order_by("-created_at")
        serializer = PropertySerializer(properties, many=True)

        return Response({
            "status": True,
            "data": serializer.data
        })

    def post(self, request):
        serializer = PropertySerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response({
                "status": True,
                "message": "Property created successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            "status": False,
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class PropertyDetailAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUserCustom]
    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return super().get_permissions()
    def get_object(self, pk):
        try:
            return Property.objects.get(id=pk)
        except Property.DoesNotExist:
            return None

    def get(self, request, pk):
        property_obj = self.get_object(pk)

        if not property_obj:
            return Response({
                "status": False,
                "message": "Property not found"
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = PropertySerializer(property_obj)

        return Response({
            "status": True,
            "data": serializer.data
        })

    def put(self, request, pk):
        property_obj = self.get_object(pk)

        if not property_obj:
            return Response({
                "status": False,
                "message": "Property not found"
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = PropertySerializer(
            property_obj,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()

            return Response({
                "status": True,
                "message": "Property updated successfully",
                "data": serializer.data
            })

        return Response({
            "status": False,
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        property_obj = self.get_object(pk)

        if not property_obj:
            return Response({
                "status": False,
                "message": "Property not found"
            }, status=status.HTTP_404_NOT_FOUND)

        property_obj.delete()

        return Response({
            "status": True,
            "message": "Property deleted successfully"
        }, status=status.HTTP_200_OK)
    
class ContactAPIView(APIView):
    authentication_classes = [JWTAuthentication]

    def get_authenticators(self):
        if self.request.method == "POST":
            return []
        return super().get_authenticators()

    def get_permissions(self):
        if self.request.method == "POST":
            return [AllowAny()]
        return [IsAuthenticated(), IsAdminUserCustom()]
    def get(self, request):
        contacts = Contact.objects.all().order_by("-created_at")

        serializer = ContactSerializer(
            contacts,
            many=True
        )

        return Response({
            "status": True,
            "data": serializer.data
        })

    def post(self, request):
        serializer = ContactSerializer(
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()

            return Response({
                "status": True,
                "message": "Message sent successfully",
                "data": serializer.data
            })

        return Response({
            "status": False,
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)