from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User, Characters
from .serializers import UserRegisterSerializers, CharactersSerializers


# Create your views here.
class RegisterUser(APIView):
    def post(self, request):
        serializer = UserRegisterSerializers(context={"request": request}, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class CharactersView(APIView):
    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
            char = Characters.objects.get(user=user)
            char_serializer = CharactersSerializers(char)
            return Response(char_serializer.data, status=200)
        except Exception as e:
            return Response(str(e), status=400)
    
    def post(self, request):
        request_copy = request.data.copy()
        request_copy['user'] = request.user.id

        char_serializer = CharactersSerializers(context={"request": request}, data=request_copy)
        if char_serializer.is_valid():
            char_serializer.save()
            return Response(char_serializer.data, status=201)
        return Response(char_serializer.errors, status=400)

