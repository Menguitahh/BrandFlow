from rest_framework import serializers
from .models import Users
from brand_control import models as control_model
from brand_control import serializer as control_serializer


class UserRegisterSerializer(serializers.ModelSerializer):
    """Serializer para que un usuario se registre creando su propia compañía."""
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    company = control_serializer.CategorySerializer(required=True)
    role = serializers.HiddenField(default='admin')

    class Meta:
        model = Users
        fields = ['username', 'email', 'password', 'password2', 'name', 'role', 'company']
        extra_kwargs = {'email': {'required': True}}

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Las contraseñas no coinciden."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        company_data = validated_data.pop('company')
        new_company = control_model.Company.objects.create(**company_data)
        validated_data['role'] = 'admin'
        return Users.objects.create_user(company=new_company, **validated_data)


class UserCreateByAdminSerializer(serializers.ModelSerializer):
    """Serializer para que un admin cree usuarios dentro de su empresa."""
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = Users
        fields = ['username', 'email', 'password', 'password2', 'name', 'role', 'branch']
        extra_kwargs = {'email': {'required': True}}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and hasattr(request.user, 'company'):
            self.fields['branch'].queryset = control_model.Branch.objects.filter(company=request.user.company)

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Las contraseñas no coinciden."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        company = self.context['request'].user.company
        return Users.objects.create_user(company=company, **validated_data)


class BranchCreateByAdminSerializer(serializers.ModelSerializer):
    """Serializer para que un admin cree sucursales para su empresa."""

    class Meta:
        model = control_model.Branch
        fields = ['name', 'address', 'phone']

    def create(self, validated_data):
        company = self.context['request'].users.company
        return control_model.Branch.objects.create(company=company, **validated_data)
