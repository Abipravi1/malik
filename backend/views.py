from django.shortcuts import render
from .models import *
import secrets
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from datetime import datetime, timedelta, date
from django.db.models import Sum
import math


present_time = datetime.now()

'{:%H:%M:%S}'.format(present_time)
updated_time = datetime.now() + timedelta(hours=20)


@api_view(['POST'])
def loginuser(request):
    username = request.data.get('username')
    password = request.data.get('password')
    if authenticate(username=username, password=password) is not None:
        response_data = {
            'token': setAuth(username),
            'time_expire': updated_time,
            'user': username
        }
        return Response(response_data)
    else:
        return Response({"Error":"Not Logged..."}, status=status.HTTP_401_UNAUTHORIZED)


def setAuth(username):
    authKey = secrets.token_hex(20)
    value = {'username': username, 'token': authKey, 'expire': updated_time }
    expire_time = updated_time
    serializer = Tokensserializers(data=value)
    if serializer.is_valid():
        serializer.save()
    else:
        pass
    return authKey


@api_view(['POST'])
def createUser(request):
    username = request.data.get('username')
    email="admin@email.com"
    password = request.data.get('password')
    try:
        create = User.objects.create_user(username=username,
                                    email=email,
                                    password=password)
        create.save()
        return Response({"status" : "success", "data" :request.data})
    except User:
        return Response({"status":"Error", "data": User})


def check_auth(Authkey):
    present_time = datetime.now()
    '{:%H:%M:%S}'.format(present_time)
    updated_time = datetime.now()
    if Tokens.objects.filter(token=Authkey):
        Auth = Tokens.objects.get(token=Authkey)
        serializer = Tokensserializers(Auth, many=False)
        expire_time = serializer.data.get('expire')
        expire_time = expire_time.replace('Z', "")
        expire_time = datetime.strptime(expire_time, '%Y-%m-%dT%H:%M:%S.%f')
        if updated_time > expire_time:
            return False
        else:
            return True

@api_view(['GET'])
def verify_user(request, token):
    Authkey = token
    present_time = datetime.now()
    '{:%H:%M:%S}'.format(present_time)
    updated_time = datetime.now()
    if Tokens.objects.filter(token=Authkey):
        Auth = Tokens.objects.get(token=Authkey)
        serializer = Tokensserializers(Auth, many=False)
        expire_time = serializer.data.get('expire')
        expire_time = expire_time.replace('Z', "")
        expire_time = datetime.strptime(expire_time, '%Y-%m-%dT%H:%M:%S.%f')
        if updated_time > expire_time:
            return Response({"Error":'Not Logged.....'}, ststus=status.HTTP_401_UNAUTHORIZED) 
        else:
            return Response({'Error':'Not Logged.....'}, status=status.HTTP_200_OK) 
    else:
        return Response({'Error':'not Logged'}, status=status.HTTP_401_UNAUTHORIZED)
