from rest_framework import serializers
from .models import *
from django.db.models import Avg
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password


User = get_user_model()

class SignupSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=160)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def validate(self, data):
        email = data.get('email')
        username = data.get('username')

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Пользователь с таким email уже существует.")

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("Пользователь с таким именем уже существует.")

        return data

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Пароль должен быть не менее 8 символов")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

def authenticate(email=None, password=None):
    UserModel = get_user_model()
    try:
        user = UserModel.objects.get(email=email)
        if user.check_password(password):
            return user
    except UserModel.DoesNotExist:
        return None
    return None

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if user:
                data['user'] = user
            else:
                raise serializers.ValidationError("Неверные учетные данные")
        else:
            raise serializers.ValidationError("Email и пароль обязательны")

        return data


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

class OrderSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    full_name = serializers.CharField(max_length=100)
    email = serializers.EmailField(max_length=100)
    phone_number = serializers.IntegerField()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = '__all__'


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brands
        fields = '__all__'


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Colors
        fields = '__all__'


class MemorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Memories
        fields = '__all__'


class ProductCharacteristicSerializer(serializers.Serializer):
    characteristics = serializers.ListField(child=serializers.CharField())

    def to_representation(self, instance):
        return {
            'characteristics': instance
        }

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    brand = serializers.StringRelatedField()
    model = serializers.StringRelatedField()
    colors = serializers.StringRelatedField(source='color', many=True)
    memories = serializers.StringRelatedField(source='memory', many=True)
    photos = serializers.StringRelatedField(source='photo', many=True)
    rating = serializers.SerializerMethodField()
    characteristics = serializers.SerializerMethodField()

    class Meta:
        model = Products
        fields = ['id', 'category', 'brand', 'model',
                  'description', 'name', 'price', 'in_stock',
                  'create_date', 'colors', 'memories',
                  'photos', 'characteristics', 'rating']

    def get_characteristics(self, obj):
        characteristics = obj.characteristic.all()
        serializer = ProductCharacteristicSerializer(characteristics, many=True)
        return serializer.data

    def get_rating(self, obj):
        rating = obj.reviews.aggregate(Avg('grade'))['grade__avg']
        return rating


class BasketSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)
    user_email = serializers.EmailField(source='user.email', read_only=True)
    
    class Meta:
        model = Baskets
        fields = ['email', 'user_email', 'products']

    def create(self, validated_data):
        email = validated_data.pop('email')
        user = User.objects.filter(email=email).first()
        if not user:
            raise serializers.ValidationError("Пользователь с указанным email не найден")

        basket = Baskets.objects.create(user=user)
        return basket

class ProductPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPhoto
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    name = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ['id', 'email', 'name', 'product', 'text', 'grade']

    def get_name(self, obj):
        if obj.name:
            return obj.name
        elif obj.user:
            return obj.user.username
        return None

    def create(self, validated_data):
        email = validated_data.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            validated_data['user'] = user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        email = validated_data.get('email')
        if email:
            user = User.objects.filter(email=email).first()
            if user:
                validated_data['user'] = user
        return super().update(instance, validated_data)


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'


class ProductCharacteristicSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCharacteristic
        fields = ['key', 'value']


class CarouselSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carousel
        fields = '__all__'


class ProductModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductModel
        fileds = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'full_name', 'phone_number', 'email', 'ordered_product_id']
