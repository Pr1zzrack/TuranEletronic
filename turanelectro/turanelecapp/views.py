from datetime import timedelta
from rest_framework import viewsets, permissions
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, NumberFilter, ModelMultipleChoiceFilter
from django.http import QueryDict
from django.utils import timezone


from rest_framework import generics
from .serializers import OrderSerializer
import requests

class OrderCreateView(generics.CreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        send_telegram_message(instance)

class OrderListView(generics.ListAPIView):
    queryset = Contact.objects.all()
    serializer_class = OrderSerializer

def send_telegram_message(contact_instance):
    bot_token = '6766161141:AAFVJQK2pNXYuGi9yVeRAkm61FdGZsUgPzA'
    user_id = '2084770237'
    message = f"Заказ:\nИмя: {contact_instance.first_name}\nФамилия: {contact_instance.last_name}\nНомер: {contact_instance.phone_number}\nEmail: {contact_instance.email}\nID Продукта: {contact_instance.ordered_product_id}"
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {'chat_id': user_id, 'text': message}
    requests.post(url, data=payload)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategorySerializer


class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brands.objects.all()
    serializer_class = BrandSerializer


class ColorViewSet(viewsets.ModelViewSet):
    queryset = Colors.objects.all()
    serializer_class = ColorSerializer


class MemoryViewSet(viewsets.ModelViewSet):
    queryset = Memories.objects.all()
    serializer_class = MemorySerializer


class ProductFilter(FilterSet):
    min_price = NumberFilter(field_name="price", lookup_expr='gte', label='От')
    max_price = NumberFilter(field_name="price", lookup_expr='lte', label='До')
    color = ModelMultipleChoiceFilter(field_name='color__name', to_field_name='name', queryset=Colors.objects.all(),
                              label='Цвет')
    memory = ModelMultipleChoiceFilter(field_name='memory__value', to_field_name='value', queryset=Memories.objects.all(),
                               label='Память')

    class Meta:
        model = Products
        fields = ['category', 'brand', 'model',]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        brand_id = self.data.get('brand')
        if brand_id:
            self.filters['model'].queryset = ProductModel.objects.filter(id=brand_id)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ['name', 'brand__name', 'category__name']
    filterset_class = ProductFilter

    def get_queryset(self):
        queryset = super().get_queryset()

        queryset = self.filter_queryset(queryset)

        self.request.query_params._mutable = True
        self.request.query_params.pop('color', None)
        self.request.query_params.pop('memory', None)
        self.request.query_params._mutable = False

        return queryset

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        reviews = ReviewSerializer(instance.reviews.all(), many=True).data
        response_data = {
            'product': serializer.data,
            'reviews': reviews,
        }
        return Response(response_data)


class BasketViewSet(viewsets.ModelViewSet):
    queryset = Baskets.objects.all()
    serializer_class = BasketSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProductPhotoViewSet(viewsets.ModelViewSet):
    queryset = ProductPhoto.objects.all()
    serializer_class = ProductPhotoSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]


class RecommendViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Products.objects.all()
    def get_queryset(self):
        queryset = Products.objects.filter(reviews__grade__gte=2.0)
        return queryset
