from django.urls import path

from .views import ProductView

urlpatterns = [
    path(
        'product/',
        ProductView.as_view({'get': 'list', 'post': 'create'}),
        name='product-list',
    ),
    path(
        'product/<int:pk>/',
        ProductView.as_view({
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy',
        }),
        name='product-detail',
    ),
]
