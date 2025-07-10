from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import UserProfile


class UserSerializer(serializers.ModelSerializer):
    """用户序列化器"""
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')
        read_only_fields = ('id',)


class UserProfileSerializer(serializers.ModelSerializer):
    """用户信息序列化器"""
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = '__all__'


class LoginSerializer(serializers.Serializer):
    """登录序列化器"""
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError('用户名或密码错误')
            if not user.is_active:
                raise serializers.ValidationError('用户账户已被禁用')
        else:
            raise serializers.ValidationError('必须提供用户名和密码')

        attrs['user'] = user
        return attrs


class RegisterSerializer(serializers.ModelSerializer):
    """注册序列化器"""
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password_confirm', 'first_name', 'last_name')

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError('两次输入的密码不一致')
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        # 创建用户信息
        UserProfile.objects.create(user=user)
        return user 