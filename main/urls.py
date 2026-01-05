from django.urls import path
from main.views import SendCodeAPIView, CodeVerificationAPIView, ResendCodeAPIView, SignUpAPIView

urlpatterns = [
    path('verify-code/', CodeVerificationAPIView.as_view()),
    path('send-code/', SendCodeAPIView.as_view()),
    path('resend-code/', ResendCodeAPIView.as_view()),
    path('sign-up/', SignUpAPIView.as_view()),

]