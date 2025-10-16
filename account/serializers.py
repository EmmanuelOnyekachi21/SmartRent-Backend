"""
==========================================
serializer.py
==========================================
"""
from rest_framework import serializers
from account.models import Account
from datetime import date

class AccountProfileReadSerializer(serializers.ModelSerializer):
    date_joined = serializers.DateTimeField(read_only=True)
    date_updated = serializers.DateTimeField(read_only=True)
    dob = serializers.DateField(format='%d/%m/%Y', input_formats=['%d-%m-%Y', '%d/%m/%Y'])
    class Meta:
        model = Account
        fields = [
            'id', 'full_name', 'email', 'phone_number', 'sex', 'role', 'dob',
            'age', 'address', 'profile_photo', 'date_updated', 'date_joined'
        ]

class AccountProfileWriteSerializer(serializers.ModelSerializer):
    dob = serializers.DateField(input_formats=['%d-%m-%Y', '%d/%m/%Y'])
    class Meta:
        model = Account
        fields = [
            'first_name', 'last_name', 'email', 'phone_number', 'dob',
            'sex', 'role', 'profile_photo'
        ]
    def validate_dob(self, dob):
        if (dob) > date.today():
            raise serializers.ValidationError(
                "Date of birth can't be in the future"
            )
        return dob
            

class AccountRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            'first_name', 'last_name', 'email', 'phone_number', 'dob',
            'sex', 'role'
        ]
    def validate_dob(self, dob):
        if (dob) > date.today():
            raise serializers.ValidationError(
                "Date of birth can't be in the future"
            )
        return dob