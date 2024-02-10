from rest_framework.generics import ListAPIView, RetrieveAPIView

from apps.product.models import Product
from apps.api.paginators import StandardResultsSetPagination
from apps.api.serializers import ProductSerializer, ProductFullSerializer


class ProductsApiView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = StandardResultsSetPagination


class ProductApiView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductFullSerializer
