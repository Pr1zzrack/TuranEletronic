from django.urls import path, include
from .views import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('accounts/', include('allauth.urls'), name='accounts'),
    path('categories/', CategoryViewSet.as_view({'get': 'list'}), name='categories'),
    path('brands/', BrandViewSet.as_view({'get': 'list'}), name='brands'),
    path('products/', ProductViewSet.as_view({'get': 'list'}), name='product_list'),
    path('products/<int:pk>/', ProductViewSet.as_view({'get': 'retrieve',}), name='product_detail'),
    path('basket/', BasketViewSet.as_view({'get': 'list', 'post': 'create'}), name='basket'),
    path('favorite/', FavoriteViewSet.as_view({'get': 'list', 'post': 'create'}), name='favorite'),
    path('review/', ReviewViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('recommend/', RecommendViewSet.as_view({'get': 'list'}), name='recommend'),
]

urlpatterns += staticfiles_urlpatterns()