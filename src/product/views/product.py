from typing import Any
from django.shortcuts import render
from django.db.models.query import QuerySet
from product.serializers import (ProductSerializer,ProductVariantSerializer,ProductImageSerializer)
from django.views import generic
from django.db import transaction
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse,QueryDict
import json

from product.models import (Variant,Product,ProductVariant,ProductVariantPrice)



@method_decorator(csrf_exempt, name='dispatch')
class CreateProductView(View):
    template_name = 'products/create.html'
    product_serializer = ProductSerializer
    product_variant_serializer = ProductVariantSerializer

    def get_context_data(self):
        context = {}
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())
        return context
    
    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            query_dict = QueryDict('', mutable=True)
            query_dict.update(data)


            product_info = query_dict.get('product_info')
            product_variants = query_dict.get('variants')
            product_variant_prices = query_dict.get('product_variant_prices')

            print(product_info)
            print(product_variants)
            print(product_variant_prices)
            
            with transaction.atomic():
                product = Product.objects.create(title=product_info['title'],sku=product_info['sku'],description=product_info['description'])
                ProductVariant.objects.bulk_create([ProductVariant(
                    variant_title=(',').join(tag for tag in i['tags']),
                    variant_id=i['option'],
                    product=product
                ) for i in product_variants])


                for price in product_variant_prices:
                    pass
                
                # ProductVariantPrice.objects.bulk_create([ProductVariantPrice(
                        
                #     ) for i in product_variant_prices])

            # Your further processing logic here

            return JsonResponse({"product_id": 'prod'}, safe=False)

        except json.JSONDecodeError as e:
            # Handle JSON decoding error
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
    
class UploadImages(View):
    product_image_serializer = ProductImageSerializer
    def post(self, request, *args, **kwargs):
        print(request.FILES)
        print(request.POST)
        # for file in 
        return JsonResponse("ok",safe=False)

            

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
    
        