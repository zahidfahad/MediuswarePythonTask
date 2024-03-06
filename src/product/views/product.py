from typing import Any
from django.db.models.query import QuerySet
from product.serializers import (ProductSerializer,ProductVariantSerializer,ProductImageSerializer)
from django.views import generic
from django.db import transaction
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from product.models import (Variant,Product,ProductVariant)


class CreateProductView(generic.TemplateView):
    template_name = 'products/create.html'

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())
        return context
    
@method_decorator(csrf_exempt, name='dispatch')
class CreateProductAPIView(View):
    product_serializer = ProductSerializer
    product_image_serializer = ProductImageSerializer
    product_variant_serializer = ProductVariantSerializer
    
    def post(self, request):
        # product_info = request.POST.get('product_info')
        # media_files = request.POST.get('media_files')
        # variants = request.POST.get('variants')

        # print(product_info)
        # print(media_files)
        # print(variants)
        print(request.POST)
        return JsonResponse('ok',safe=False)
            

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
    
        