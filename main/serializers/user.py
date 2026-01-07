from rest_framework import serializers
from main.models.user import User, NEW, DONE
from main.utils import is_email, is_phone



class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, value):

        user = User.objects.filter(email=value).first()
        if user != None and user.status != NEW :
            raise serializers.ValidationError("A user with this email already VERIFIED.")
        return value

class CodeSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6, required=True)

    def validate_code(self, value):
        if not value.isdigit() or len(value) != 6:
            raise serializers.ValidationError("Code must be a 6-digit number.")
        return value
    
class UserInfoSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length = 150)
    last_name = serializers.CharField(max_length = 150, required = False, allow_blank = True)
    username = serializers.CharField(max_length = 150, required = True)
    phone = serializers.CharField(max_length = 13, min_length = 13)
    password1 = serializers.CharField(min_length = 8, max_length = 16)
    password2 = serializers.CharField(min_length = 8, max_length = 16)

    def validate_username(self, value:str):
        user = User.objects.filter(username=value)
        if user is not None:
            raise serializers.ValidationError('Username already taken.')

    def validate_phone(self, value:str):
        if not value.startswith('+'):
            raise serializers.ValidationError('Phone number must start with +')
        
        user = User.objects.filter(phone=value)
        if user is not None:
            raise serializers.ValidationError('Phone number already used.')

        return value

    
class LoginSerializer(serializers.Serializer):
    user_input = serializers.CharField(max_length = 200, required=True)
    password = serializers.CharField(max_length = 16, required = True)

    def validate(self, validated_data):
        user_input = validated_data.get('user_input')
        if is_email(user_input):
            user = User.objects.filter(email=user_input).filter(status=DONE).first()
            if user is not None:
                validated_data['username'] = user.username
            else:
                raise serializers.ValidationError('User not found.')
        elif is_phone(user_input):
            user = User.objects.filter(phone=user_input).filter(status=DONE).first()
            if user is not None:
                validated_data['username'] = user.username
            else:
                raise serializers.ValidationError('User not found.')
        else:
            validated_data['username'] = user_input
        
        return validated_data

