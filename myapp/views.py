from django.shortcuts import render
from myapp.models import Pilot,Airport
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.csrf import csrf_exempt
import requests
import json
import io
from rest_framework.parsers import JSONParser
from .serializer import AirportSerializer
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
#user = CustomUser.objects.create_user(email='user@example.com', password='mypassword')
from django.core import serializers
from django.http import JsonResponse

def airport_details(request,user_id):
    token = request.META.get('HTTP_AUTHORIZATION')

    if not token:
        return JsonResponse({'error': 'Authorization header missing'}, status=401)

    # Perform your token validation logic here
    # For example, you can decode and verify a JWT token

    if not valid_token:
        return JsonResponse({'error': 'Invalid token'}, status=401)

    detail=Airport.objects.filter(user_id=user_id)
    serialized_queryset = serializers.serialize('json', detail)
    response_data = {'data': serialized_queryset}
    return JsonResponse(response_data,safe=False)  


@csrf_exempt
def airport_create(request):
    if request.method=="POST":
        token = request.META.get('HTTP_AUTHORIZATION')

        if not token:
            return JsonResponse({'error': 'Authorization header missing'}, status=401)
    
        # Perform your token validation logic here
        # For example, you can decode and verify a JWT token
    
        if not valid_token:
            return JsonResponse({'error': 'Invalid token'}, status=401)
        json_data=request.body
        stream=io.BytesIO(json_data)
        data=JSONParser().parse(stream)
        serialise_data=AirportSerializer(data=data)
        if serialise_data.is_valid():
            serialise_data.save()
            res={"msg":'data added succesfully'}
            response=JSONRenderer().render(res)
            return HttpResponse(response,content_type="application/json")
        response=JSONRenderer().render(serialise_data.errors)
        return HttpResponse(response,content_type="application/json")


class RegisterView(APIView):
    def post(self, request):
        name = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        if Pilot.objects.filter(name=name).exists():
            return Response({'error': 'Username is already taken'})
        elif Pilot.objects.filter(email=email).exists():
            return Response({'error': 'Email is already registered'})
        else:
            user = Pilot.objects.create_user(
                name=name,
                email=email,
                password=password
            )
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })

class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = Pilot.objects.filter(email=email).first()

        if user is None:
            return Response({'error': 'Invalid credentials'})
        elif not user.check_password(password):
            return Response({'error': 'Invalid credentials'})
        else:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
