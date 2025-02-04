from django.http import JsonResponse
from django.views.generic import TemplateView, ListView
from django.shortcuts import redirect, get_object_or_404

from modules.product.models import Category, Product
from .models import Channel
from ..product.choices import ProductStatus


class HomeView(TemplateView):
    template_name = "channel/list.html"

    def dispatch(self, request, *args, **kwargs):
        channels = Channel.objects.filter(active=True)
        if channels.count() == 1:
            return redirect('channel:detail', pk=channels.first().id)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['channels'] = Channel.objects.filter(active=True)
        return context


class ChannelDetailView(ListView):
    template_name = "channel/view.html"
    context_object_name = 'products'

    def get_queryset(self):
        self.channel = get_object_or_404(Channel, pk=self.kwargs.get('pk'))
        category_id = self.request.GET.get('category', None)

        if category_id:
            self.category = get_object_or_404(Category, pk=category_id, channels__channel=self.channel)
        else:
            self.category = Category.objects.filter(channels__channel=self.channel).first()

        if not self.category:
            return Product.objects.none()

        return Product.objects.filter(
            category=self.category,
            status=ProductStatus.online
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['channel'] = self.channel
        context['categories'] = Category.objects.filter(channels__channel=self.channel).prefetch_related('info')
        context['selected_category'] = self.category

        return context


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product_data = {
        'name': product.name,
        'description': product.description,
        'variants': list(product.variants.values('id', 'price', 'code')),
        'currency': product.category.channels.first().channel.currency,
        'images': [media.image.url for media in product.media.all()],
        'ingredients': [
            {
                'name': additive.additive.name,
                'price': str(additive.additive.price),
                'image': additive.additive.image.url,
            }
            for additive in product.additives.select_related('additive').all()
        ],
    }
    return JsonResponse(product_data)
