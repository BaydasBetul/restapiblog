from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from .models import Blog, Comment, Like, BlogView
from .pagination import CursorPagi, Pagination
from .permissions import IsOwnerOrReadOnly
from .serializers import BlogViewSerializer, CommentSerializer, BlogSerializer, LikeSerializer
# Create your views here.


class BlogList(generics.ListCreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    pagination_class = Pagination
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response({
            'status': status.HTTP_200_OK,
            'message': 'Blog created!'
        })


class BlogDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    lookup_field = 'id'
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly,)

    def put(self, request, *args, **kwargs):
        self.update(request, *args, **kwargs)
        return Response({
            'status': status.HTTP_200_OK,
            'message': 'Blog updated!'
        })

    def delete(self, request, *args, **kwargs):
        self.destroy(request, *args, **kwargs)
        content = {'message': 'Blog deleted!'}
        return Response(content, status=status.HTTP_200_OK)


class CommentList(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        post_id = self.kwargs['id']
        return Comment.objects.filter(post=post_id)

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response({
            'status': status.HTTP_200_OK,
            'message': 'Comment added successfully!'
        })


class LikeList(generics.ListCreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        post_id = self.kwargs['id']
        return Like.objects.filter(post=post_id)


class BlogViewList(generics.ListCreateAPIView):
    queryset = BlogView.objects.all()
    serializer_class = BlogViewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        post_id = self.kwargs['id']
        return BlogView.objects.filter(post=post_id)
