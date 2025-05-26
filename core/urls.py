from django.urls import path
from .views import RegisterView, profile_view, PasswordResetRequestView, PasswordResetConfirmView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('profile/', profile_view),
    path('reset-password/', PasswordResetRequestView.as_view()),
    path('reset-password-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view()),
]
