from rest_framework import serializers
from main.models.user import User, NEW

class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        user = User.objects.filter(email=value).first()
        if user.status != NEW:
            raise serializers.ValidationError("A user with this email already VERIFIED.")
        return value

class CodeSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6, required=True)

    def validate_code(self, value):
        if not value.isdigit() or len(value) != 6:
            raise serializers.ValidationError("Code must be a 6-digit number.")
        return value