from rest_framework.views import APIView
from .serializers import SerializerNote, SignUpSerializer
from rest_framework import viewsets , status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Notes
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist 

# Create your views here.
class NotesViewSet(viewsets.ModelViewSet):
    queryset = Notes.objects.all()
    serializer_class = SerializerNote
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated] 
    search_fields = ['title', 'tag']
    
    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }  

    def get_queryset(self): 
        queryset = Notes.objects.all().filter(user=self.request.user).order_by('-id')
        return queryset
    
    
class SignUpApi(APIView):
    def get(self, request):
        return Response({
                    'status': 403,
                    'msg': 'SignUp Api For Post Request'
                }, status=status.HTTP_403_FORBIDDEN)


    def post(self, request):
        try:
            if 'username' in request.data:
                user = User.objects.get(username=request.data['username'])
                return Response({
                            'status': 226,
                            'msg': 'Username Is Already Exist, Please Login'
                        }, status=status.HTTP_226_IM_USED)
            else:
                return Response({
                            'status': 403,
                            'msg': 'first_name, last_name, email, username, password is required'
                        }, status=status.HTTP_403_FORBIDDEN)
        except User.DoesNotExist:
            serializer = SignUpSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                if 'username' and 'password' in request.data:
                    username = request.data['username']
                    password = request.data['password']
                    user = authenticate(username=username, password=password)
                    if user is not None:
                        access = AccessToken.for_user(user)
                        token = {
                            'status': 202,
                            'token': str(access)
                        }
                        return Response(token, status=status.HTTP_202_ACCEPTED)
                return Response({
                            'status': 200,
                            'msg': 'SignUp Successfull, Please Login'
                        }, status=status.HTTP_200_OK)
            return Response({
                        'status': 400,
                        'msg': serializer.errors
                    }, status=status.HTTP_400_BAD_REQUEST)


class SignInApi(APIView):
    def get(self, request):
        return Response({
                    'status': 403,
                    'msg': 'SignIn Api For Post Request'
                }, status=status.HTTP_403_FORBIDDEN)


    def post(self, request):
        if 'username' and 'password' in request.data:
            username = request.data['username']
            password = request.data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                refresh = RefreshToken.for_user(user)
                token = {
                    'status': 202,
                    'token': str(refresh.access_token)
                }
                return Response(token, status=status.HTTP_202_ACCEPTED)
            return Response({
                        'status': 404,
                        'msg': 'Invalid Username & Password Please Try Again'
                    }, status=status.HTTP_404_NOT_FOUND)
        return Response({
                    'status': 403,
                    'msg': 'Username & Password is required'
                }, status=status.HTTP_403_FORBIDDEN)