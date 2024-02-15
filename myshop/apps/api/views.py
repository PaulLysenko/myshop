from django.contrib.auth.models import User

from rest_framework import authentication
from rest_framework import exceptions
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from apps.account.models import Profile
from apps.product.models import Product
from apps.api.paginators import StandardResultsSetPagination
from apps.api.serializers import ProductSerializer, ProductFullSerializer


class CustomAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        api_token = request.META.get('HTTP_TOKEN')
        if not api_token:
            return None

        try:
            profile = Profile.objects.select_related(
                'user',
            ).get(
                api_key=api_token,
            )

        except Profile.DoesNotExist:
            raise exceptions.NotAuthenticated()

        return (profile.user, None)


class ProductsApiView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = StandardResultsSetPagination


class ProductApiView(RetrieveAPIView):
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductFullSerializer
