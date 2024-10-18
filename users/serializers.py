from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'  

        extra_kwargs = {
            'password': {'write_only': True}
        }

    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        isinstance = self.Meta.model(**validated_data)

        if password:
            isinstance.set_password(password)
        isinstance.save()
        return isinstance
    
class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'name', 'email'] 