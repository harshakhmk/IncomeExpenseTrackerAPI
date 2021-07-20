from django.shortcuts import render, reverse
from rest_framework.response import Response
from .models import User, Alerts
from rest_framework import permissions
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from utils.permission import *

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status, generics, views
from .serializers import (
    ResetPasswordSerializer,
    RegisterUserSerializer,
    EmailVerificationSerializer,
    LoginSerializer,
    AlertSerializer,
)
from django.contrib.sites.shortcuts import get_current_site
from utils.email import Util
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Create your views here.
class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterUserSerializer
    queryset = User.objects.all()

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        # now user is created
        user_data = serializer.data
        user = User.objects.get(email=user_data.get("email"))
        token = RefreshToken.for_user(user).access_token
        current_domain = get_current_site(request).domain
        relative_url = reverse("verify-email")
        absolute_url = (
            "http://" + current_domain + relative_url + "?token=" + str(token)
        )
        message_body = (
            f"Hi {user.username}, please verify your email address from below link\n"
            + absolute_url
        )
        email_data = {
            "body": message_body,
            "subject": "Verify your email",
            "to_email": user.email,
        }
        Util.send_email(email_data)
        return Response(user_data, status=status.HTTP_201_CREATED)


class VerifyUserEmail(views.APIView):
    serializer_class = EmailVerificationSerializer
    token_param = openapi.Parameter(
        "token",
        in_=openapi.IN_QUERY,
        description="Enter token to verify your account",
        type=openapi.TYPE_STRING,
    )

    @swagger_auto_schema(manual_parameters=[token_param])
    def get(self, request):
        token = request.GET.get("token")
        try:
            data = jwt.decode(token, settings.SECRET_KEY)
            user = User.objects.filter(id=data["user_id"])
            if user.is_verified:
                return Response(
                    {"message": "Already verified"}, status=status.HTTP_200_OK
                )

            user.is_verified = True
            user.save()
            return Response(
                {"message": "Successfully verified"}, status=status.HTTP_200_OK
            )
        except jwt.ExpiredSignatureError as e:
            return Response(
                {"message": "Activation link Expired"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except jwt.Exceptions.DecodeError as de:
            return Response(
                {"message": "Invalid Token"}, status=status.HTTP_400_BAD_REQUEST
            )


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        # data = request.data
        # user_data = serializer.data
        # user = User.objects.get(email=user_data.get("email"))
        # user_alerts, created = Alerts.objects.get_or_create(user=user)
        print(serializer.__dir__())
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status.HTTP_200_OK)


class ResetPasswordView(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer

    def post(self, request):
        data = {"request": request, "data": request.data}
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)


class PasswordTokenCheckAPI(generics.GenericAPIView):
    def get(self, request):
        pass


class NotificationAlertsView(generics.GenericAPIView):
    serializer_class = AlertSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner)

    def get(self, request):
        user = request.user
        user_alerts = Alerts.objects.filter(user=user)
        serializer = self.serializer_class(user_alerts)
        return Response(serializer.data, status.HTTP_200_OK)

    def put(self, request):
        instance = Alerts.objects.filter(user=request.user).first()
        serializer = self.serializer_class(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_200_OK)
