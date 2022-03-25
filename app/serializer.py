from rest_framework import serializers
from . models import Users, Company, Attendance

class AddUserSerializer(serializers.ModelSerializer):
    key = serializers.CharField(
        write_only=True,
        required=True,
    )
    class Meta:
        model = Users
        fields = ['key', 'user_id', 'full_name']

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['key', 'bot_token', 'channel_id']

class AttendanceSerializer(serializers.ModelSerializer):
    key = serializers.CharField(
        write_only=True,
        required=True,
    )
    user_id = serializers.CharField(
        write_only=True,
        required=True,
    )

    class Meta:
        model = Attendance
        fields = ['key', 'user_id']
