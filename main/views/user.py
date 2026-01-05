from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from main.utils import send_code
from main.serializers import EmailSerializer, CodeSerializer
from main.models.user import User, UserConfirmation, VERIFIED

class SendCodeAPIView(APIView):
    serializer_class = EmailSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        user = User.objects.create(email=email)
        code = user.create_code()

        send_code(email, code)

        data = {
            'status': 'Success',
            'message': 'Confirmation code sent to email.',
            'token': user.token()
        }

        return Response(data, status=200)

class CodeVerificationAPIView(APIView):
    serializer_class = CodeSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        code = serializer.validated_data.get('code')


        confirmation = user.confirmations.order_by('-created_at').first()

        if confirmation.code != code or confirmation.is_expired():
            return Response({'status': 'Error', 'message': 'Invalid or expired code.'}, status=400)

        user.status = VERIFIED
        user.save()

        data = {
            'status': 'Success',
            'message': 'Email verified successfully.',
            'token': user.token()
        }

        return Response(data, status=200)
    

class ResendCodeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        if self.resend_code(user):
            data = {
                'status': 'Success',
                'message': 'New confirmation code sent to email.'
            }
        else:
            data = {
                'status': 'Error',
                'message': 'You have unexpired code!'
            }

        return Response(data, status=200)

    def resend_code(self, user):
        confirmation = user.confirmations.order_by('-created_at').first()
        if confirmation.is_expired():
            code = user.create_code()
            send_code(user.email, code)

            return True