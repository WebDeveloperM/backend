from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny

from django.utils.timezone import now
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CustomToken


class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user:
            # Foydalanuvchi uchun tokenni olish yoki yaratish
            token, created = CustomToken.objects.get_or_create(user=user)

            # Token muddati tugagan bo‘lsa, uni yangilaymiz
            if not created and token.is_expired():
                token.delete()  # Eski tokenni o‘chiramiz
                token = CustomToken.objects.create(user=user)  # Yangi token yaratamiz

            return Response({
                'token': token.key,
                'expires_at': token.expires_at,
                "firstname": user.first_name,
                "lastname": user.last_name,
            }, status=status.HTTP_200_OK)

        return Response({'error': 'Неправильный логин или пароль'}, status=status.HTTP_401_UNAUTHORIZED)


class UserInfoView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request, *args, **kwargs):
        user = request.user
        return Response({
            "id": user.id,
            "username": user.username,
            "firstname": user.firstname,
            "lastname": user.lastname,
        }, status=status.HTTP_200_OK)


class TokenStatusAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request, *args, **kwargs):
        # Tokenni olish
        token = kwargs.get('token')

        try:
            token = CustomToken.objects.get(key=token)
        except CustomToken.DoesNotExist:
            return Response({'error': 'Token not found'}, status=404)

        # Tokenning amal qilish muddatini tekshirish
        if token.expires_at and now() > token.expires_at:
            return Response({'is_expired': True, 'message': 'Token has expired'}, status=200)

        # Token hali amal qiladi
        return Response({'is_expired': False, 'message': 'Token is still valid'}, status=200)
