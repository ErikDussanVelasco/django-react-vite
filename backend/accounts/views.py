from django.contrib.auth import get_user_model, authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.views import View
from django.utils.decorators import method_decorator
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from .serializers import RegisterSerializer, LoginSerializer

# ✅ Obtiene el modelo de usuario configurado en AUTH_USER_MODEL
User = get_user_model()


# ==================== VISTAS BASADAS EN TEMPLATES ====================

class RegisterTemplateView(View):
    """Vista de registro con template HTML"""
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('inventario_dashboard')
        return render(request, 'accounts/register.html')
    
    def post(self, request):
        email = request.POST.get('email', '').strip().lower()
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        password_confirm = request.POST.get('password_confirm', '').strip()
        
        # Validaciones
        if not email or not username or not password:
            messages.error(request, 'Por favor completa todos los campos')
            return render(request, 'accounts/register.html')
        
        if password != password_confirm:
            messages.error(request, 'Las contraseñas no coinciden')
            return render(request, 'accounts/register.html', {
                'email': email,
                'username': username
            })
        
        if len(password) < 6:
            messages.error(request, 'La contraseña debe tener al menos 6 caracteres')
            return render(request, 'accounts/register.html', {
                'email': email,
                'username': username
            })
        
        # Verificar si el usuario ya existe
        if User.objects.filter(email__iexact=email).exists():
            messages.error(request, 'El correo ya está registrado')
            return render(request, 'accounts/register.html', {
                'username': username
            })
        
        if User.objects.filter(username__iexact=username).exists():
            messages.error(request, 'El usuario ya está registrado')
            return render(request, 'accounts/register.html', {
                'email': email
            })
        
        # Crear usuario
        try:
            user = User.objects.create_user(
                email=email,
                username=username,
                password=password
            )
            # NO autologueamos, dejamos que el usuario haga login manualmente
            messages.success(request, f'¡Cuenta creada exitosamente! Por favor inicia sesión con tus credenciales.')
            return redirect('login')
        except Exception as e:
            messages.error(request, f'Error al registrar: {str(e)}')
            return render(request, 'accounts/register.html', {
                'email': email,
                'username': username
            })


class LoginTemplateView(View):
    """Vista de login con template HTML"""
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('inventario_dashboard')
        return render(request, 'accounts/login.html')
    
    def post(self, request):
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '').strip()
        
        if not email or not password:
            messages.error(request, 'Por favor completa todos los campos')
            return render(request, 'accounts/login.html')
        
        # Autenticar usando el backend personalizado
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'¡Bienvenido de vuelta {user.username}!')
            return redirect('inventario_dashboard')
        else:
            messages.error(request, 'Correo o contraseña incorrectos')
            return render(request, 'accounts/login.html', {
                'email': email
            })


class LogoutTemplateView(View):
    """Vista de logout"""
    def get(self, request):
        logout(request)
        messages.success(request, 'Sesión cerrada correctamente')
        return redirect('login')


class HomeTemplateView(View):
    """Vista Home - solo para usuarios autenticados"""
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        return render(request, 'inventario/dashboard.html', {
            'user': request.user
        })


# ==================== VISTAS API (REST) ====================

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get('user')
        
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email
                },
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            })
        else:
            return Response({"error": "Usuario no encontrado"}, status=status.HTTP_400_BAD_REQUEST)


class UserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email
        })

