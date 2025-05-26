from rest_framework import viewsets, permissions, filters
from .models import Post, Category, Tag
from .serializers import (
    PostSerializer, PostCreateUpdateSerializer,
    CategorySerializer, TagSerializer
)
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Faqat post muallifi tahrirlashi mumkin, boshqalar faqat o‘qiy oladi.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content']

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return PostCreateUpdateSerializer
        return PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]



@api_view(['POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def add_view(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
        post.views += 1
        post.save()
        return Response({"message": "View added", "views": post.views})
    except Post.DoesNotExist:
        return Response({"error": "Post not found"}, status=404)



@api_view(['POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def add_like(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
        user = request.user
        if user in post.likes.all():
            post.likes.remove(user)
            return Response({"message": "Unliked", "likes": post.likes.count(), "is_liked": False})
        else:
            post.likes.add(user)
            return Response({"message": "Liked", "likes": post.likes.count(), "is_liked": True})
    except Post.DoesNotExist:
        return Response({"error": "Post not found"}, status=404)
