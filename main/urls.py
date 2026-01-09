from django.urls import path
from main.views import (
    SendCodeAPIView, CodeVerificationAPIView, 
    ResendCodeAPIView, SignUpAPIView, LoginAPIView, PostViewSet, MediaViewSet, CommentViewSet)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='posts')
router.register(r'media', MediaViewSet, basename='media')
router.register(r'comments', CommentViewSet, basename='comments')

urlpatterns = [
    path('verify-code/', CodeVerificationAPIView.as_view()),
    path('send-code/', SendCodeAPIView.as_view()),
    path('resend-code/', ResendCodeAPIView.as_view()),
    path('sign-up/', SignUpAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
]

urlpatterns += router.urls