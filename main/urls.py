from django.urls import path
from main.views import SendCodeAPIView, CodeVerificationAPIView, ResendCodeAPIView

urlpatterns = [
    path('verify-code/', CodeVerificationAPIView.as_view()),
    path('send-code/', SendCodeAPIView.as_view()),
    path('resend-code/', ResendCodeAPIView.as_view()),

]