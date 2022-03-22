from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from django.contrib.auth.models import User
from .serializers import RegisterSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
# Create your views here.

# CreateAPIView icinde post methodu var, bu ne create ettiysek bize döndürür


class RegisterAPI(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # token key ekleme
        token = Token.objects.create(user=user)
        data = serializer.data
        data['token'] = token.key
        headers = self.get_success_headers(serializer.data)
        # token oluşturduktan sonra headers ile göndermemiz gerekiyor
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

    # def post(self, request, *args, **kwargs):
    #         serializer = RegisterSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(
    #         {"message": "user created succesfully"}
    #     )
