from rest_framework import serializers
from .models import Booking, BookingMember, Feedback, Registration, PhoneOTP, Place, Hotel


# ---------------- REGISTER ----------------

# ---------------- LOGIN ----------------
class LoginUserSerializer(serializers.Serializer):
    mobile_number = serializers.CharField(max_length=15)
    password = serializers.CharField(write_only=True)

class RefreshTokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()
# ---------------- SEND OTP ----------------
