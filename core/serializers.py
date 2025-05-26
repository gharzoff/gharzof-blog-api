from rest_framework import serializers
from .models import User
from django.contrib.auth.password_validation import validate_password
from blog.serializers import PostSerializer
from django.conf import settings

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    posts = PostSerializer(many=True, read_only=True)
    liked_posts = PostSerializer(many=True, read_only=True)
    profile_image = serializers.SerializerMethodField()
    posts_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'bio', 'profile_image', 'date_joined', 'posts', 'liked_posts', 'posts_count']

    def get_profile_image(self, obj):
        if obj.profile_image:
            return obj.profile_image.url
        return settings.STATIC_URL + 'img/defaultuser.png'
    
    def get_posts_count(self, obj):
        return obj.posts.count()
    
    