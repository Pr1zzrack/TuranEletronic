from django.contrib import admin
from .models import *


admin.site.register(Categories)
admin.site.register(Brands)
admin.site.register(Baskets)
admin.site.register(ProductModel)
admin.site.register(Review)
admin.site.register(Favorite)
admin.site.register(Carousel)


class ColorInline(admin.TabularInline):
    model = Colors
    extra = 1


class MemoryInline(admin.TabularInline):
    model = Memories
    extra = 1


class ProductPhotoInline(admin.TabularInline):
    model = ProductPhoto
    extra = 1


class ProductCharacteristicInline(admin.TabularInline):
    model = ProductCharacteristic
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'brand', 'price', 'in_stock']
    list_filter = ['category', 'brand', 'in_stock']
    search_fields = ['name', 'description', 'model']

    fieldsets = [
        ('Основная информация', {'fields': ['name', 'category', 'brand', 'model', 'description']}),
        ('ЦЕНА И НАЛИЧИЕ', {'fields': ['price', 'in_stock']}),
    ]

    add_fieldsets = [
        ('Добавление нового товара', {
            'classes': ('wide',),
            'fields': ['name', 'category', 'brand', 'model', 'description', 'price', 'in_stock'],
        }),
    ]

    inlines = [ProductPhotoInline, ProductCharacteristicInline, ColorInline, MemoryInline]


admin.site.register(Products, ProductAdmin)
