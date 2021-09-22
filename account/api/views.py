from rest_framework.decorators import api_view

from account.models import User

from rest_framework import generics, status
from rest_framework.views import APIView

from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializer import SignUpSerializer, LoginSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model, login, logout


@api_view(('POST',))
def logout_api_view(request):
    try:
        refresh_token = request.data['refresh']
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response("successful logout", status=status.HTTP_200_OK)
    except:
        refresh_token == request.data['access']
        return Response({"msg : invalid token"}, status=status.HTTP_400_BAD_REQUEST)


class SignUpApiView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_class = [AllowAny]


class LoginApiView(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = LoginSerializer
    permission_class = [AllowAny]

    def get_object(self):
        obj = User.objects.filter(email=self.request.data['email']).first()
        return obj

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            user = self.get_object()
            serializer = self.get_serializer(data=user, partial=True)
            if serializer.is_valid():
                return Response(status=status.HTTP_200_OK, data='login successful')

            return Response(status=status.HTTP_403_FORBIDDEN, data='login unsuccessful')


class ChangePasswordUpdate(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = LoginSerializer
    permission_class = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        self.user = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            if not self.user.check_password(serializer.data.get('OldPassword')):
                return Response({'old_password': ['Wrong password']}, status.HTTP_400_BAD_REQUEST)
            self.user.set_password(serializer.data.get('NewPassword'))
            return Response(status=status.HTTP_200_OK, data='password updated!!')
        return Response(status.HTTP_400_BAD_REQUEST, serializer.errors, )
