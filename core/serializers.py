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
    posts_count = serializers.SerializerMethodField()

    profile_image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'bio', 'profile_image', 'date_joined', 'posts', 'liked_posts', 'posts_count']

    def get_posts_count(self, obj):
        return obj.posts.count()

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        if instance.profile_image:
            rep['profile_image'] = instance.profile_image.url
        else:
            rep['profile_image'] = settings.STATIC_URL + 'img/defaultuser.png'
        return rep

    
    