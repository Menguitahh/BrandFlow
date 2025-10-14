from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Users
from brand_control import models as control_model


class UserRegisterSerializer(serializers.ModelSerializer):
    """Serializer para que un usuario se registre creando su propia cuenta."""
    username = serializers.CharField()
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    roles = serializers.CharField(default='cliente', write_only=True, required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    phone = serializers.CharField(required=False)
    address = serializers.CharField(required=False)

    class Meta:
        model = Users
        fields = ['username', 'email', 'password', 'password2', 'first_name', 'last_name', 'phone', 'address', 'roles']
        extra_kwargs = {'email': {'required': True}}

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Las contraseñas no coinciden."})

        username = attrs.get('username')
        email = attrs.get('email')
        
        # Mensajes más claros para duplicados
        if username and Users.objects.filter(username=username).exists():
            raise serializers.ValidationError({"username": "Ya existe un usuario con ese nombre. Elige otro."})
        if email and Users.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": "Ya existe un usuario registrado con ese email."})
        
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        # Forzar siempre cliente y ignorar roles entrante
        validated_data['roles'] = 'cliente'
        return Users.objects.create_user(**validated_data)


class UserCreateByAdminSerializer(serializers.ModelSerializer):
    """Serializer para que un admin cree usuarios dentro de su empresa."""
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    phone = serializers.CharField(required=False)
    address = serializers.CharField(required=False)

    class Meta:
        model = Users
        fields = ['username', 'email', 'password', 'password2', 'first_name', 'last_name', 'phone', 'address', 'roles']
        extra_kwargs = {'email': {'required': True}}

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Las contraseñas no coinciden."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        # Asignar la empresa del admin que crea el usuario
        validated_data['company'] = self.context['request'].user
        return Users.objects.create_user(**validated_data)


class UserDetailSerializer(serializers.ModelSerializer):
    """Serializer para mostrar detalles del usuario."""
    role = serializers.CharField(source='roles', read_only=True)
    is_admin = serializers.ReadOnlyField()
    class Meta:
        model = Users
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone', 'address', 'roles', 'role', 'is_admin', 'date_joined']
        read_only_fields = ['id', 'date_joined']


class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer para actualizar datos del usuario."""
    class Meta:
        model = Users
        fields = ['first_name', 'last_name', 'phone', 'address', 'email']


# BranchCreateByAdminSerializer eliminado - modelo Branch no existe
