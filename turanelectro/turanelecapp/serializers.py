from rest_framework import serializers
from .models import *
from django.db.models import Avg


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


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    brand = serializers.StringRelatedField()
    model = serializers.StringRelatedField()
    colors = serializers.StringRelatedField(source='color', many=True)
    memories = serializers.StringRelatedField(source='memory', many=True)
    photos = serializers.StringRelatedField(source='photo', many=True)
    characteristics = serializers.StringRelatedField(source='characteristic', many=True)

    rating = serializers.SerializerMethodField()

    class Meta:
        model = Products
        fields = ['id', 'category', 'brand', 'model',
                  'description', 'name', 'price', 'in_stock',
                  'create_date', 'colors', 'memories',
                  'photos', 'characteristics', 'rating']

    def get_rating(self, obj):
        rating = obj.reviews.aggregate(Avg('grade'))['grade__avg']
        return rating


class BasketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Baskets
        fields = '__all__'


class ProductPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPhoto
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Review
        fields = '__all__'


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

