from rest_framework import serializers
from .models import *
from user_control.models import Users


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         # fields = ('iduser', 'username', "password", "email",'phone', 'addres')
#         fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    stock_status = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = '__all__'
    
    def get_stock_status(self, obj):
        """Retorna el estado del stock"""
        if obj.stock == 0:
            return "Sin stock"
        elif obj.stock <= 5:
            return "Stock bajo"
        else:
            return "Stock disponible"
    
    def validate_stock(self, value):
        """Validar que el stock no sea negativo"""
        if value < 0:
            raise serializers.ValidationError("El stock no puede ser negativo")
        return value


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source='user.email', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ('total', 'created_at', 'updated_at')


class OrderDetailsSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='idproduct.name', read_only=True)
    product_price = serializers.DecimalField(source='idproduct.price', read_only=True, max_digits=10, decimal_places=2)
    
    class Meta:
        model = OrderDetails
        fields = '__all__'
    
    def validate(self, data):
        """Validar que hay stock suficiente"""
        product = data['idproduct']
        quantity = data['quantity']
        
        if not product.has_stock(quantity):
            raise serializers.ValidationError(f"Stock insuficiente. Disponible: {product.stock}")
        
        return data


class ShoppCartSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source='user.email', read_only=True)
    total = serializers.SerializerMethodField()
    
    class Meta:
        model = ShoppCart
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')
    
    def get_total(self, obj):
        return obj.get_total()


class ShoppCartDetailsSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='idproduct.name', read_only=True)
    product_price = serializers.DecimalField(source='idproduct.price', read_only=True, max_digits=10, decimal_places=2)
    subtotal = serializers.SerializerMethodField()
    
    class Meta:
        model = ShoppCartDetails
        fields = '__all__'
        read_only_fields = ('idshoppcart',)
    
    def get_subtotal(self, obj):
        return obj.idproduct.price * obj.quantity
    
    def validate(self, data):
        """Validar que hay stock suficiente"""
        product = data['idproduct']
        quantity = data['quantity']
        
        if not product.has_stock(quantity):
            raise serializers.ValidationError(f"Stock insuficiente. Disponible: {product.stock}")
        
        return data


class ReviewsSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    product_name = serializers.CharField(source='idproduct.name', read_only=True)
    
    class Meta:
        model = Reviews
        fields = '__all__'
        read_only_fields = ('date', 'user')


class BranchSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.username', read_only=True)
    
    class Meta:
        model = Branch
        fields = '__all__'
        read_only_fields = ('created_at',)


class StockMovementSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)
    movement_type_display = serializers.CharField(source='get_movement_type_display', read_only=True)
    
    class Meta:
        model = StockMovement
        fields = '__all__'
        read_only_fields = ('previous_stock', 'new_stock', 'created_at')


class StockUpdateSerializer(serializers.Serializer):
    """Serializer para actualizar stock de productos"""
    quantity = serializers.IntegerField()
    operation = serializers.ChoiceField(choices=[('increase', 'Aumentar'), ('decrease', 'Disminuir')])
    reason = serializers.CharField(max_length=200)
    
    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("La cantidad debe ser mayor a 0")
        return value


class CreateOrderFromCartSerializer(serializers.Serializer):
    """Serializer para crear orden desde el carrito"""
    cart_id = serializers.IntegerField()
    
    def validate_cart_id(self, value):
        try:
            cart = ShoppCart.objects.get(idshoppcart=value)
            if not cart.shoppcartdetails_set.exists():
                raise serializers.ValidationError("El carrito está vacío")
        except ShoppCart.DoesNotExist:
            raise serializers.ValidationError("Carrito no encontrado")
        return value

