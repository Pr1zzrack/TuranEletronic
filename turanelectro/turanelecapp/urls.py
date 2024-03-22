from django.urls import path, include
from .views import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('login/', LoginViewSet.as_view({'post': 'login'}), name='login'),
    path('logout/', LogoutViewSet.as_view({'post': 'logout'}), name='logout'),
    path('forgot-password/', ForgotPasswordViewSet.as_view({'post': 'forgot_password'}), name='forgot_password'),
    path('signup/', SignupViewSet.as_view({'post': 'signup'}), name='signup'),
    path('categories/', CategoryViewSet.as_view({'get': 'list'}), name='categories'),
    path('brands/', BrandViewSet.as_view({'get': 'list'}), name='brands'),
    path('products/', ProductViewSet.as_view({'get': 'list'}), name='product_list'),
    path('products/<int:pk>/', ProductViewSet.as_view({'get': 'retrieve',}), name='product_detail'),
    path('basket/', BasketViewSet.as_view({'get': 'list', 'post': 'create'}), name='basket'),
    path('favorite/', FavoriteViewSet.as_view({'get': 'list', 'post': 'create'}), name='favorite'),
    path('review/', ReviewViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('recommend/', RecommendViewSet.as_view({'get': 'list'}), name='recommend'),
    path('orders/', OrderViewSet.as_view({'get': 'list', 'post': 'create'}), name='order-list-create'),
    path('model/', ProductModelViewSet.as_view({'get': 'list', 'post': 'create'}), name='model'),
]

urlpatterns += staticfiles_urlpatterns()
