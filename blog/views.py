from django.shortcuts import render
from .serializers import BlogPostSerializer
from .models import BlogPost
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, RetrieveAPIView

# Create your views here.
class BlogPostCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = BlogPostSerializer
    queryset = BlogPost.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class BlogListView(ListAPIView):
    serializer_class = BlogPostSerializer
    queryset = BlogPost.objects.all()


class BlogPostUpdateView(UpdateAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = BlogPostSerializer
    queryset = BlogPost.objects.all()


class BlogPostDetailView(RetrieveAPIView):
    serializer_class = BlogPostSerializer
    queryset = BlogPost.objects.all()