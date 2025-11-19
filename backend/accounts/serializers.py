from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        # 👇 Solo pedimos email (login principal) + username opcional
        fields = ['id', 'email', 'username', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data.get('username', ''),  # username opcional
            password=validated_data['password']
        )
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        # Buscar usuario por email
        try:
            user = User.objects.get(email=email)
            # Validar la contraseña directamente
            if not user.check_password(password):
                raise serializers.ValidationError("Credenciales inválidas.")
            if not user.is_active:
                raise serializers.ValidationError("Cuenta desactivada.")
            # Retornar el usuario en el diccionario de datos
            data['user'] = user
            return data
        except User.DoesNotExist:
            raise serializers.ValidationError("Credenciales inválidas.")
