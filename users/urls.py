# accounts/urls.py
from django.urls import path
from .views import LoginAPIView, UserInfoView, TokenStatusAPIView

urlpatterns = [
    path('login/', LoginAPIView.as_view()),
    path('user/', UserInfoView.as_view(), name='user-info'),
    path('check-token/', TokenStatusAPIView.as_view(), name='user-info'),
]
