
from django.urls import path
from .views import LoginView, UserListView, UserDetailView, UserCreateView, UserDisableView

urlpatterns = [
	path('login/', LoginView.as_view(), name='login'),
	path('usuarios/', UserListView.as_view(), name='usuarios-list'),
	path('usuarios/<int:id>/', UserDetailView.as_view(), name='usuario-detail'),
	path('usuarios/crear/', UserCreateView.as_view(), name='usuario-crear'),
	path('usuarios/<int:id>/deshabilitar/', UserDisableView.as_view(), name='usuario-deshabilitar'),
]
