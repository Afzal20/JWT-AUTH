from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(
        write_only=True,
        min_length=8,
        required=True,
        error_messages={
            'min_length': 'Password must be at least 8 characters long.'
        }
    )
    password2 = serializers.CharField(
        write_only=True,
        min_length=8,
        required=True,
        error_messages={
            'min_length': 'Password must be at least 8 characters long.'
        }
    )

    class Meta:
        model = CustomUser
        fields = ['email', 'password1', 'password2']

    def validate(self, data):
        # Check if the passwords match
        if data['password1'] != data['password2']:
            raise serializers.ValidationError({
                'password2': 'Passwords do not match.'
            })

        # Validate the password using Django's built-in validators
        try:
            validate_password(data['password1'])
        except serializers.ValidationError as e:
            raise serializers.ValidationError({
                'password1': list(e.messages)
            })

        return data

    def create(self, validated_data):
        # Extract email and password
        email = validated_data['email']
        password = validated_data['password1']

        # Use the custom user manager to create the user
        user = CustomUser.objects.create_user(email=email, password=password)
        return user


class OTPVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    otp = serializers.CharField(
        max_length=6,
        required=True,
        error_messages={
            'required': 'OTP is required.',
            'max_length': 'OTP must be exactly 6 characters.'
        }
    )

    def validate_otp(self, otp):
        if not otp.isdigit():
            raise serializers.ValidationError('OTP must be a numeric value.')
        return otp

    def validate(self, data):
        # Ensure user with the given email exists
        email = data.get('email')
        otp = data.get('otp')

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError({'email': 'User with this email does not exist.'})

        # Validate the OTP
        if not user.validate_otp(otp):
            raise serializers.ValidationError({'otp': 'Invalid or expired OTP.'})

        return data
