from django.urls import path

from apps.user import api_endpoints

app_name = 'user'

urlpatterns = [
    path('login/', api_endpoints.LoginView.as_view()),
    path('register/', api_endpoints.SendOTPView.as_view(), name='register'),
    path('register/complete/', api_endpoints.CompleteRegisterView.as_view(), name='complete_register'),
    path('refresh/', api_endpoints.RefreshView.as_view(), name='refresh'),
]