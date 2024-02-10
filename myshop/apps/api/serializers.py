from rest_framework.serializers import ModelSerializer, DateTimeField
from apps.product.models import Product, Brand


class BrandSerializer(ModelSerializer):
    class Meta:
        model = Brand
        fields = [
            'name',
            'country',
        ]


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'name',
            'price',
        ]


class ProductFullSerializer(ModelSerializer):
    brand = BrandSerializer()
    created_at = DateTimeField(format='%Y:%m:%d')

    class Meta:
        model = Product
        fields = [
            'name',
            'price',
            'description',
            'brand',
            'created_at',
        ]
