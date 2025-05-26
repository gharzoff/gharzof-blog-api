from rest_framework import serializers
from .models import Post, Category, Tag
from core.models import User
from django.conf import settings

class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class PostSerializer(serializers.ModelSerializer):
    author = UserShortSerializer(read_only=True)
    likes = UserShortSerializer(many=True, read_only=True)
    total_likes = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    category = CategorySerializer()
    tags = TagSerializer(many=True)
    is_owner = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    reading_time = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'slug',
            'content',
            'image',
            'views',
            'total_likes',
            'author',
            'likes',
            'is_liked',
            'is_owner',
            'reading_time',
            'category',
            'tags',
            'created_at',
            'updated_at'
        ]

    def get_total_likes(self, obj):
        return obj.likes.count()
    
    def get_is_owner(self, obj):
        request = self.context.get('request')
        return request.user == obj.author
    
    def get_reading_time(self, obj):
        words = len(obj.content.split())
        minutes = max(1, words // 200)
        return f"{minutes} min read"

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(id=request.user.id).exists()
        return False
    
    def get_image(self, obj):
        if obj.image:
            return obj.image.url
        return settings.STATIC_URL + 'img/defaultpost.png'


class PostCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'title', 'content', 'image', 'category', 'tags'
        ]
