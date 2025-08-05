from rest_framework import serializers
from .models import Users
from brand_control import models as control_model


class UserRegisterSerializer(serializers.ModelSerializer):
    """Serializer para que un usuario se registre creando su propia cuenta."""
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    roles = serializers.CharField(default='cliente')
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
        # Asegurar que el rol sea 'cliente' por defecto
        validated_data['roles'] = validated_data.get('roles', 'cliente')
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
    class Meta:
        model = Users
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone', 'address', 'roles', 'date_joined']
        read_only_fields = ['id', 'date_joined']


class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer para actualizar datos del usuario."""
    class Meta:
        model = Users
        fields = ['first_name', 'last_name', 'phone', 'address', 'email']


class BranchCreateByAdminSerializer(serializers.ModelSerializer):
    """Serializer para que un admin cree sucursales para su empresa."""

    class Meta:
        model = control_model.Branch
        fields = ['name', 'address', 'phone']

    def create(self, validated_data):
        company = self.context['request'].user
        return control_model.Branch.objects.create(company=company, **validated_data)
