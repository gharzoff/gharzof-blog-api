from django.urls import path
from .views import RegisterView, profile_view

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('profile/', profile_view),
]
