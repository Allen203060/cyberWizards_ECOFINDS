from rest_framework import serializers
from .models import User, Product, Category, CartItem, Order

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model, used for registration.
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the Category model.
    """
    class Meta:
        model = Category
        fields = ('id', 'name', 'slug')

class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for the Product model. Includes read-only fields for related models.
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    category_name = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = Product
        fields = ('id', 'owner', 'category', 'category_name', 'title', 'description', 'price', 'image_placeholder', 'is_sold', 'created_at')

class CartItemSerializer(serializers.ModelSerializer):
    """
    Serializer for Cart items.
    """
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product', write_only=True
    )

    class Meta:
        model = CartItem
        fields = ('id', 'product', 'product_id', 'quantity')

class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for past Orders.
    """
    products = ProductSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = ('id', 'user', 'products', 'total_price', 'ordered_at')