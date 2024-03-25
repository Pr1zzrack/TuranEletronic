from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, NumberFilter, ModelMultipleChoiceFilter
import requests
from django.contrib.auth import logout
from rest_framework.decorators import action
from rest_framework import status
from rest_framework import permissions
from rest_framework import viewsets
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated

User = get_user_model()

class LoginViewSet(viewsets.ViewSet):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data.get('user')
            if user:
                return Response({"message": "Вход выполнен успешно", "email": user.email}, status=status.HTTP_200_OK)
        return Response({"error": "Неверные учетные данные"}, status=status.HTTP_400_BAD_REQUEST)

class SignupViewSet(viewsets.ViewSet):
    serializer_class = SignupSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['post'])
    def signup(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "Регистрация прошла успешно", "email": user.email}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Неверные данные", "fields": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class LogoutViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['post'])
    def logout(self, request):
        logout(request)
        return Response({"message": "Вы успешно вышли из системы"}, status=status.HTTP_200_OK)

class ForgotPasswordViewSet(viewsets.ViewSet):
    serializer_class = ForgotPasswordSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['post'])
    def forgot_password(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            return Response({"message": "Ссылка для восстановления пароля отправлена на ваш email"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Неверные данные", "fields": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        send_telegram_message(instance, chat_id='-1002030525141')

def send_telegram_message(contact_instance, chat_id):
    bot_token = '6766161141:AAFVJQK2pNXYuGi9yVeRAkm61FdGZsUgPzA'
    message = f"Заказ:\nФамилия Имя: {contact_instance.full_name}\nНомер: {contact_instance.phone_number}\nEmail: {contact_instance.email}\nID Продукта: {contact_instance.ordered_product_id}"
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {'chat_id': chat_id, 'text': message}
    requests.post(url, data=payload)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategorySerializer

class CarouselViewSet(viewsets.ModelViewSet):
    queryset = Carousel.objects.all()
    serializer_class = CarouselSerializer

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
        return queryset

    @action(detail=True, methods=['get'])
    def characteristics(self, request, pk=None):
        product = self.get_object()
        characteristics = product.productcharacteristic_set.all()
        serializer = ProductCharacteristicSerializer(characteristics, many=True)
        return Response(serializer.data)

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
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class ProductPhotoViewSet(viewsets.ModelViewSet):
    queryset = ProductPhoto.objects.all()
    serializer_class = ProductPhotoSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        email = serializer.validated_data.get('email')
        user = User.objects.filter(email=email).first()
        serializer.save(user=user)

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
