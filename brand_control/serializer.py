from rest_framework import serializers
from .models import (
    ServiceCategory, Service, Project, QuoteRequest, Payment, ProjectMessage
)
from django.contrib.auth import get_user_model

User = get_user_model()


class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = ['id', 'name', 'description']


class ServiceSerializer(serializers.ModelSerializer):
    category = ServiceCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=ServiceCategory.objects.all(), source='category', write_only=True)

    class Meta:
        model = Service
        fields = ['id', 'name', 'description', 'service_type', 'base_price', 'features', 'delivery_time', 'category', 'category_id']


class ProjectSerializer(serializers.ModelSerializer):
    client = serializers.PrimaryKeyRelatedField(read_only=True)
    assigned_to = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), allow_null=True, required=False)
    service = serializers.PrimaryKeyRelatedField(queryset=Service.objects.all())

    class Meta:
        model = Project
        fields = ['id', 'title', 'brief', 'status', 'priority', 'start_date', 'delivery_date', 'total_price', 'paid_amount', 'client', 'assigned_to', 'service', 'created_at', 'updated_at']
        read_only_fields = ['paid_amount', 'created_at', 'updated_at']


class QuoteRequestSerializer(serializers.ModelSerializer):
    client = serializers.PrimaryKeyRelatedField(read_only=True)
    service = serializers.PrimaryKeyRelatedField(queryset=Service.objects.all())

    class Meta:
        model = QuoteRequest
        fields = ['id', 'client', 'service', 'title', 'description', 'budget', 'status', 'created_at', 'updated_at', 'approved_by', 'approved_at', 'rejected_reason', 'linked_project']
        read_only_fields = ['status', 'created_at', 'updated_at', 'approved_by', 'approved_at', 'rejected_reason', 'linked_project']

    def create(self, validated_data):
        request = self.context['request']
        user = request.user
        if hasattr(user, 'is_admin') and (user.is_admin() if callable(user.is_admin) else user.is_admin):
            # admin puede crear en nombre de un cliente si se pasó 'client'
            client = request.data.get('client')
            if client:
                try:
                    client_obj = User.objects.get(id=client)
                except User.DoesNotExist:
                    raise serializers.ValidationError({'client': 'Cliente no encontrado'})
                return QuoteRequest.objects.create(client=client_obj, **validated_data)
        # por defecto, cliente autenticado
        return QuoteRequest.objects.create(client=user, **validated_data)


class ProjectMessageSerializer(serializers.ModelSerializer):
    sender = serializers.PrimaryKeyRelatedField(read_only=True)
    attachment_url = serializers.SerializerMethodField()
    attachment_name = serializers.CharField(read_only=True)
    has_attachment = serializers.ReadOnlyField()
    attachment_type = serializers.ReadOnlyField()

    class Meta:
        model = ProjectMessage
        fields = ['id', 'project', 'sender', 'message', 'attachment', 'attachment_url', 'attachment_name', 'has_attachment', 'attachment_type', 'created_at', 'is_internal']
        read_only_fields = ['id', 'created_at', 'sender', 'attachment_name']

    def get_attachment_url(self, obj):
        if obj.attachment:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.attachment.url)
            return obj.attachment.url
        return None

    def create(self, validated_data):
        # Guardar el nombre original del archivo
        if 'attachment' in validated_data and validated_data['attachment']:
            validated_data['attachment_name'] = validated_data['attachment'].name
        return super().create(validated_data)


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'project', 'amount', 'status', 'is_simulated', 'cardholder_name', 'card_last4', 'created_at']
        read_only_fields = ['id', 'status', 'is_simulated', 'created_at']