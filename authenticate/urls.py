from django.urls import reverse, path, include
from .views import RegisterView, VerifyUserEmail, LoginAPIView, NotificationAlertsView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("verify-email/", VerifyUserEmail.as_view(), name="verify-email"),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path(
        "notification-alerts/",
        NotificationAlertsView.as_view(),
        name="notification-alerts",
    ),
]
