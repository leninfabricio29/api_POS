
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import CustomUser
from .serializers import UserDetailSerializer, UserCreateSerializer

from .serializers import CustomTokenObtainPairSerializer

class LoginView(TokenObtainPairView):
	"""Endpoint para login con JWT y datos de usuario"""
	serializer_class = CustomTokenObtainPairSerializer

class UserListView(generics.ListAPIView):
	queryset = CustomUser.objects.all()
	serializer_class = UserDetailSerializer
	permission_classes = [permissions.IsAuthenticated]

class UserDetailView(generics.RetrieveAPIView):
	queryset = CustomUser.objects.all()
	serializer_class = UserDetailSerializer
	permission_classes = [permissions.IsAuthenticated]
	lookup_field = 'id'

class UserCreateView(generics.CreateAPIView):
	queryset = CustomUser.objects.all()
	serializer_class = UserCreateSerializer
	permission_classes = [permissions.IsAuthenticated]

class UserDisableView(APIView):
	permission_classes = [permissions.IsAuthenticated]

	def post(self, request, id):
		try:
			user = CustomUser.objects.get(id=id)
			user.is_active = False
			user.save()
			return Response({'detail': 'Empleado deshabilitado'}, status=status.HTTP_200_OK)
		except CustomUser.DoesNotExist:
			return Response({'detail': 'No existe el usuario'}, status=status.HTTP_404_NOT_FOUND)
