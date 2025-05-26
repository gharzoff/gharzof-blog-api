from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import PostViewSet, CategoryViewSet, TagViewSet, add_like, add_view

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='posts')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'tags', TagViewSet, basename='tags')

urlpatterns = [
    path('', include(router.urls)),
    path('posts/<int:post_id>/view/', add_view, name='add_view'),
    path('posts/<int:post_id>/like/', add_like, name='add_like'),]
