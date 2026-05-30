from rest_framework import serializers
from .models import  Contact, Property, Registration, Testimonial


# ---------------- REGISTER ----------------

# ---------------- LOGIN ----------------
class LoginUserSerializer(serializers.Serializer):
    mobile_number = serializers.CharField(max_length=15)
    password = serializers.CharField(write_only=True)

class RefreshTokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()
# ---------------- SEND OTP ----------------
class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = "__all__"

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = "__all__"
        read_only_fields = ["id", "created_at"]

class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = '__all__'