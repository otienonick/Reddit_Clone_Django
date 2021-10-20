from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.exceptions import ValidationError
from rest_framework import generics, permissions,mixins, status
from .models import Post,Vote
from .serializers import PostSerializer,VoteSerializer
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.contrib.auth.models import User
from django.db import IntegrityError
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from rest_framework.views import APIView




# Create your views here.
class Overview(APIView):
    def get(self,request):

        api_urls = {
            'postlist': '/posts',
            'single-post':'/posts/<int:pk>',
            'create-post':'/posts',
            'delete-post':'/posts/<int:pk>',
            'vote':'/posts/<int:pk>/vote',
            'signup':'/signup',
            'login':'/login',

        }

        return Response(api_urls)


@csrf_exempt
def signup(request):
    if request.method =='POST':
        try:
            data = JSONParser().parse(request)
            user =User.objects.create_user(data['username'],password = data['password'])
            user.save()
            token  = Token.objects.create(user = user)
            return JsonResponse({'token':str(token)},status = 201)
        except IntegrityError:
            return JsonResponse({'error' :'That username has already been taken,Please choose another username'})

@csrf_exempt
def login(request):
    if request.method =='POST':
        data = JSONParser().parse(request)
        user =authenticate(request, username = data['username'],password = data['password'])
        if user is None:
            return JsonResponse({'error' :'could not login.Please check username and password'})
        else:
            try:
                token = Token.objects.get(user = user)
            except:
                token  = Token.objects.create(user = user)

            return JsonResponse({'token':str(token)},status = 200)



class PostList(generics.ListCreateAPIView):
        queryset = Post.objects.all()
        serializer_class = PostSerializer
        permission_classes = [permissions.IsAuthenticatedOrReadOnly]

        def perform_create(self,serializer):
            serializer.save(poster = self.request.user)

class VoteCreate(generics.CreateAPIView,mixins.DestroyModelMixin):
        serializer_class = VoteSerializer
        permission_classes = [permissions.IsAuthenticated]

        def get_queryset(self):
            user = self.request.user
            post = Post.objects.get(pk = self.kwargs['pk'])
            return Vote.objects.filter(voter = user,post = post)

        def perform_create(self,serializer):
            if self.get_queryset().exists():
                raise ValidationError('you have already voted for this post :)')
            serializer.save(voter = self.request.user,  post = Post.objects.get(pk = self.kwargs['pk']))

        def delete(self,request,*args,**kwargs):    
            if self.get_queryset().exists():
                self.get_queryset().delete()
                return Response(status = status.HTTP_204_NO_CONTENT)
            else:
                raise ValidationError('you never voted for this post!')

class PostDelete(generics.RetrieveDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def delete(self, request, *args, **kwargs):
        post = Post.objects.filter(pk=kwargs['pk'], poster=self.request.user)
        if post.exists():
            
            return self.destroy(request, *args, **kwargs)
        else:
            raise ValidationError('This isn\'t your post to delete!')                
           

    
     




