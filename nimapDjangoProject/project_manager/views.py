from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from .serializers import ClientSerializer, ProjectSerializer, UserSerializer
from django.contrib.auth.models import User
from .models import Project, Client
from rest_framework import generics
from .models import Project
from .serializers import ProjectSerializer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status


class UserCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class ClientListCreateView(generics.ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class ClientDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class ProjectCreateView(generics.CreateAPIView):
    serializer_class = ProjectSerializer

    def create(self, request, *args, **kwargs):
        # Extracting user IDs from the request data
        user_ids = request.data.get('users', [])
        client_id = request.data.get('client', None)

        # Validate client existence
        if not Client.objects.filter(id=client_id).exists():
            return Response({'error': f'Client with ID {client_id} does not exist.'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Validate each user ID
        for user_id in user_ids:
            if not User.objects.filter(id=user_id).exists():
                return Response({'error': f'User with ID {user_id} does not exist.'},
                                status=status.HTTP_400_BAD_REQUEST)

        # Proceed with creating the project if all validations pass
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # If validation fails, return the errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class UserProjectsView(generics.ListAPIView):
    serializer_class = ProjectSerializer


    def get_queryset(self):
        user = self.request.user
        return Project.objects.filter(users=user)




class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
