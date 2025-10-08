from rest_framework import serializers
from .models import (
    Product, Category, Order, OrderDetails, ShoppCart, ShoppCartDetails, Reviews,
    ServiceCategory, Service, Project, QuoteRequest, Payment, ProjectMessage
)
from user_control.models import Users

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         # fields = ('iduser', 'username', "password", "email",'phone', 'addres')
#         fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        # fields = ('idproduct', 'name', 'description', 'price', 'image', 'stock', 'url_download', 'category')
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        # fields = ('iduser', 'username', "password", "email",'phone', 'addres')
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        # fields = ('iduser', 'username', "password", "email",'phone', 'addres')
        fields = '__all__'

class OrderDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetails
        # fields = ('iduser', 'username', "password", "email",'phone', 'addres')
        fields = '__all__'



# class UserSerializer(serializers.ModelSerializer):   #! Asignado a los metodos de pago si es que es necesario
#     class Meta:
#         model = User
#         # fields = ('iduser', 'username', "password", "email",'phone', 'addres')
#         fields = '__all__'



# class PaymentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Payment
#         # fields = ('iduser', 'username', "password", "email",'phone', 'addres')
#         fields = '__all__'

class ShoppCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppCart
        # fields = ('iduser', 'username', "password", "email",'phone', 'addres')
        fields = '__all__'


class ShoppCartDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppCartDetails
        # fields = ('iduser', 'username', "password", "email",'phone', 'addres')
        fields = '__all__'


class ReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        # fields = ('iduser', 'username', "password", "email",'phone', 'addres')
        fields = '__all__'

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
    assigned_to = serializers.PrimaryKeyRelatedField(queryset=Users.objects.all(), allow_null=True, required=False)
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
                    client_obj = Users.objects.get(id=client)
                except Users.DoesNotExist:
                    raise serializers.ValidationError({'client': 'Cliente no encontrado'})
                return QuoteRequest.objects.create(client=client_obj, **validated_data)
        # por defecto, cliente autenticado
        return QuoteRequest.objects.create(client=user, **validated_data)


class ProjectMessageSerializer(serializers.ModelSerializer):
    sender = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = ProjectMessage
        fields = ['id', 'project', 'sender', 'message', 'created_at', 'is_internal']
        read_only_fields = ['id', 'created_at', 'sender']


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'project', 'amount', 'status', 'is_simulated', 'cardholder_name', 'card_last4', 'created_at']
        read_only_fields = ['id', 'status', 'is_simulated', 'created_at']