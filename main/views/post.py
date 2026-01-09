from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_spectacular.utils import extend_schema
from main.models import Post, Media, Comment
from main.serializers import PostSerializer, MediaSerializer, CommentSerializer, SimpleUserSerializer
from main.permissions import IsAuthenticatedAndAuthor, IsAuthenticatedAndDone

@extend_schema(tags=["Posts"])
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().select_related("users").prefetch_related("liked_users", "viewed_users", "medias")
    serializer_class = PostSerializer
    permission_classes = [AllowAny,]
    
    def get_permissions(self):
        if self.action == "list":
            permission_classes = [AllowAny(),]
        elif self.action == "create":
            permission_classes = [IsAuthenticatedAndDone()] 
        elif self.action in ["update", "destroy", "partial_update"]:
            permission_classes = [IsAuthenticatedAndAuthor()]
        else:
            permission_classes = [AllowAny()]
        return permission_classes
      

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  
        
    @action(detail=False,permission_classes = [IsAuthenticated])
    def my_liked_posts(self, request):
        posts = self.queryset.filter(liked_users = request.user)
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)
    
    @action(detail=False, permission_classes=[IsAuthenticated])
    def my_viewed_posts(self, request):
        posts = self.queryset.filter(viewed_users = request.user)
        serializer = self.get_serializer(posts, many=True)
        
        return Response(serializer.data)
    
    @action(detail=True, permission_classes = [AllowAny])
    def users_liked_post(self, request, pk=None):
        post = self.get_object()
        serializer = SimpleUserSerializer(post.liked_users.all(), many=True)
        return Response(serializer.data)
        

    @action(detail=True, permission_classes=[AllowAny])
    def users_viewed_posts(self, request, pk=None):
        post = self.get_object()
        serializer = SimpleUserSerializer(post.viewed_users.all(),many=True)
        return Response(serializer.data)
    

@extend_schema(tags=["Media"])
class MediaViewSet(viewsets.ModelViewSet):
    queryset = Media.objects.all()
    permission_classes = [AllowAny,]
    serializer_class = MediaSerializer

    def get_permissions(self):
        if self.action == "create":
            permission_classes = [IsAuthenticatedAndDone()]
        elif self.action in ["update", "partial_update", "destroy"]:
            permission_classes = [IsAuthenticated()]
        else:
            permission_classes = [AllowAny()]
        return permission_classes
    
    def perform_create(self, serializer):
        serializer.save() 
            
            
            
@extend_schema(tags=["Comment"])
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().select_related("user", "post")
    permission_classes = [AllowAny]
    serializer_class = CommentSerializer
    
    def get_permissions(self):
        if self.action == "create":
            permission_classes = [IsAuthenticatedAndDone()]
        elif self.action in ["update","partial_update","destroy"]:
            permission_classes = [IsAuthenticated()]
        else:
            permission_classes = [AllowAny()]
        
        return permission_classes
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
    @action(detail=False, permission_classes=[IsAuthenticated])
    def my_comments_list(self, request):
        comments = self.queryset.filter(user=request.user)
        serializer = self.get_serializer(comments, many=True)
        return Response(serializer.data)
    

    @action(detail=False, permission_classes = [IsAuthenticated])
    def my_commented_posts(self, request):
        posts = Post.objects.filter(comments__user = request.user).distinct()  
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    @action(detail=True, permission_classes = [AllowAny])
    def all_comments_for_post(self, request, pk=None):
        post = Post.objects.get(pk=pk)
        comments= self.queryset.filter(post=post)
        serializer = self.get_serializer(comments, many=True)
        return Response(serializer.data)

