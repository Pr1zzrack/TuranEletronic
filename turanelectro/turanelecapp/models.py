from django.db import models
from django.contrib.auth.models import User


class Contact(models.Model):
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    ordered_product_id = models.IntegerField()

    def __str__(self):
        return f"{self.full_name}"


class Categories(models.Model):
    name = models.CharField(max_length=64, verbose_name='Категория')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Brands(models.Model):
    name = models.CharField(max_length=16, verbose_name='Бренд')
    brand_logo = models.ImageField(upload_to='brands_logo/', verbose_name='логотип бренда')
    image = models.ImageField(upload_to='image/', verbose_name='фото')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'


class ProductModel(models.Model):
    name = models.CharField(max_length=32, verbose_name='Модель')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Модель'
        verbose_name_plural = 'Модели'


class Products(models.Model):
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, verbose_name='Категория')
    brand = models.ForeignKey(Brands, on_delete=models.CASCADE, verbose_name='Бренд')
    name = models.CharField(max_length=128, verbose_name='Название продукта')
    description = models.TextField(verbose_name='Описание')
    model = models.ForeignKey(ProductModel, on_delete=models.CASCADE, verbose_name='Модель')
    price = models.PositiveSmallIntegerField(default=0, verbose_name='Цена')
    in_stock = models.BooleanField(default=False, verbose_name='В наличии')
    create_date = models.DateField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['name']

    def __str__(self):
        return self.name


class ProductCharacteristic(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, verbose_name='Товар', related_name='characteristic')
    key = models.CharField(max_length=64, verbose_name='Характеристика')
    value = models.CharField(max_length=255, verbose_name='Значение')

    def __str__(self):
        return f'{self.key}: {self.value}'

    class Meta:
        verbose_name = 'Характеристика'
        verbose_name_plural = 'Характеристики'


class Baskets(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    products = models.ManyToManyField(Products, verbose_name='Продукты в корзине')

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзина'


class ProductPhoto(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, verbose_name='Товар', related_name='photo')
    image = models.ImageField(upload_to='product_photo/', verbose_name='Фото')

    class Meta:
        verbose_name = 'Фотография товара'
        verbose_name_plural = 'Фотографии товара'

    def __str__(self):
        return f'{self.image}'


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    email = models.EmailField(verbose_name='Email')
    product = models.ForeignKey(Products, on_delete=models.CASCADE, verbose_name='Товар', related_name='reviews')
    text = models.TextField(verbose_name='Текст отзыва')
    grade = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)], verbose_name='Оценка')
    name = models.CharField(max_length=255, verbose_name='Имя', blank=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['user']

    def __str__(self):
        return f'Отзыв - {self.name}'

    def save(self, *args, **kwargs):
        if not self.name:
            user = User.objects.filter(email=self.email).first()
            if user:
                self.name = user.username
        super().save(*args, **kwargs)


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    products = models.ManyToManyField(Products, verbose_name='Продукты в избранном')

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'


class Carousel(models.Model):
    text = models.CharField(max_length=128, verbose_name='Текст')
    image = models.ImageField(upload_to='carousel_photo/', verbose_name='Изображение')

    class Meta:
        verbose_name = 'Карусель'
        verbose_name_plural = 'Карусели'


class Colors(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, verbose_name='Товар', related_name='color')
    name = models.CharField(max_length=32, verbose_name='Цвет')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Цвет'
        verbose_name_plural = 'Цвета'


class Memories(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, verbose_name='Товар', related_name='memory')
    value = models.PositiveSmallIntegerField(default=0, null=True, blank=True, verbose_name='Объем')

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = 'Объем'
        verbose_name_plural = 'Объем'
