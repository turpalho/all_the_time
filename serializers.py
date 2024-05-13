from django.db import transaction
from rest_framework import serializers

from project.receipt.models import Receipt, Product, Category, Store


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']
        read_only_fields = ['name', 'slug']


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ['id', 'name']
        read_only_fields = ['id']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'price', 'count', 'total_sum', 'is_weighed_out', 'created_at']


class ReceiptSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)
    # store = serializers.PrimaryKeyRelatedField(queryset=Store.objects.all())
    store = StoreSerializer()

    class Meta:
        model = Receipt
        fields = ["store", "category", "products", "total_sum", "created_at", "created_by"]
        read_only_fields = ["created_at"]

    def create(self, validated_data):
        products_data = validated_data.pop('products')

        try:
            with transaction.atomic():
                receipt = Receipt.objects.create(**validated_data)
                for product_data in products_data:
                    Product.objects.create(receipt=receipt, **product_data)
                return receipt
        except Exception as e:
            # Handle transaction error
            raise e


class ReceiptImageSerializer(serializers.Serializer):
    image = serializers.ImageField()
