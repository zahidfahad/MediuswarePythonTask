from typing import Any
from django.db.models.query import QuerySet
from product.serializers import (ProductSerializer,ProductVariantSerializer,ProductImageSerializer)
from django.views import generic
from rest_framework.views import APIView
from django.db import transaction

from product.models import (Variant,Product,ProductVariant)


class CreateProductView(generic.TemplateView):
    template_name = 'products/create.html'

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())
        return context
    
    
class CreateProductAPIView(APIView):
    product_serializer = ProductSerializer
    product_image_serializer = ProductImageSerializer
    product_variant_serializer = ProductVariantSerializer
    
    def post(self, request):
        product_serializer = self.product_serializer(data=request.data)
        product_image_serializer = self.product_image_serializer(data=request.data,many=True)
        product_variant_serializer = self.product_variant_serializer(data=request.data,many=True)
        
        product_serializer.is_valid(raise_exception=True)
        product_image_serializer.is_valid(raise_exception=True)
        product_variant_serializer.is_valid(raise_exception=True)
        
        with transaction.atomic():
            product = product_serializer.save()
            
            # for entry in product_image_serializer
            

class ProductListView(generic.ListView):
    template_name = 'products/list.html'
    model = Product
    context_object_name = 'product_list'
    paginate_by = 1
    
    def get_filter_kwargs(self):
        params = {}
        title = self.request.GET.get('title')
        variant_id = self.request.GET.get('variant')
        price__gte = self.request.GET.get('price_from')
        price__lte = self.request.GET.get('price_to')
        created_at = self.request.GET.get('date')
        if title:
            params['title'] = title
        if  variant_id:
            params['variant_id'] = variant_id
        if  price__gte:
            params['price__gte'] = price__gte
        if  price__lte:
            params['price__lte'] = price__lte
        if  created_at:
            params['created_at'] = created_at
        return params

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        variants = Variant.objects.all()
        product_variants = ProductVariant.objects.all()                
        context['variants'] = variants
        context['product_variants'] = product_variants
        return context
        
    def get_queryset(self) -> QuerySet[Any]:
        filter_kwargs = self.get_filter_kwargs()
        qs = self.model._default_manager.filter()
        return qs
    
        