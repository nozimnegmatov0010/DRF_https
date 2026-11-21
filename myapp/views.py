from rest_framework.viewsets import ModelViewSet
from django.core.cache import cache
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer
from rest_framework.permissions import AllowAny
from .tasks import send_welcome_email


class ProductView(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes=[AllowAny]

    def list(self, request, *args, **kwargs):
        cache_key='product_list'
        data=cache.get(cache_key)
        

        if not data :
            print('from db')
            serializer=self.get_serializer(self.get_queryset(),many=True)
            data=serializer.data
            cache.set(cache_key,data,60)
            return Response(data)
            
        print('from redis')
        return Response(data)
 
 
 
    def retrieve(self, request, *args, **kwargs):
        pk=kwargs.get('pk')
        cache_key=f'product_{pk}'
        data=cache.get(cache_key)

        if not data :
            print('from db')
            product=self.get_object()
            data = ProductSerializer(product).data
            cache.set(cache_key,data,60)
            return Response(data)
            
        print('from redis')
        return Response(data)


    def perform_create(self, serializer):
        send_welcome_email.delay('Admin')
        serializer.save()
        cache.clear()

    def perform_update(self, serializer):
        serializer.save()
        cache.clear()

    def perform_destroy(self, instance):
        instance.delete()
        cache.clear()

