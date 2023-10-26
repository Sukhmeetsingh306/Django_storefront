# from django.forms import DecimalField
from django.shortcuts import render
# from django.db.models import Q, F
# from django.db.models.aggregates import Count, Max, Min, Avg, Sum
#
# Create your views here.


def say_hello(request):
    # query_set = Product.objects.filter(
    #     Q(inventory__lt=10) | Q(unit_price__lt=20))

    # query_set = Product.objects.filter(
    # id__in=OrderItem.objects.values('product_id').distinct()).order_by('title')

    #    product = Product.objects.order_by('title')

    # query_set = Product.objects.prefetch_related(
    #     'promotions').select_related('collection').all()

    # query_set = Order.objects.select_related(
    #     'customer').prefetch_related('orderitem_set__product').order_by('-placed_at')[:5]

    # result = Product.objects.aaggregate(
    #     count=Count('id'), min_price=Min('unit_price'))

    # discounted_price = ExpressionWrapper(
    #     F('unit_price') * 0.8, output_field=DecimalField(max_digits=6,  min_value=2))
    # queryset = Product.objects.annotate(discounted_price=discounted_price)

    # queryset = TaggedItem.objects.get_tags_for(Product, 1)

    queryset = Product.objects.raw('select id, title from store_product')

    return render(request, 'hello.html', {'name': 'Sukhmeet', 'tags': list(queryset)})
