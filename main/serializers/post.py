from rest_framework import serializers
from main.models.post import Post, Media, Comment
from main.models.user import User
from main.serializers.user import UserSerializer

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'content']
        read_only_fields = ['id']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['user'] = UserSerializer(instance.user).data
        data['liked_users'] = UserSerializer(instance.liked_users, many=True).data
        data['viewed_users'] = UserSerializer(instance.viewed_users, many=True).data
        data['media'] = MediaSerializer(instance.media, many=True).data

        return data


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = "__all__"
        extra_kwargs = {
            'post':{'write_only':True}
        }

class CommentSerializer(serializers.Serializer):
    class Meta:
        model = Comment
        fields = "__all__"
        


class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]