from typing import Any
from django.contrib import admin
from django.db.models.aggregates import Count
from django.db.models.query import QuerySet
from django.utils.html import format_html, urlencode
from django.urls import reverse
from . import models

# Register your models here.


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']
    search_fields = ['title']

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        url = (
            reverse('admin:store_product_changelist')  # app_model_page
            + '?'
            + urlencode(
                {
                    'collection__id': str(collection.id)
                }
            )
        )
        return format_html('<a href="{}">{} Products</a>', url,  collection.products_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count=Count('products')
        )


class InventoryFilter(admin.SimpleListFilter):  # for filtering the data
    title = 'Inventory'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [
            ('10', 'Low'),
            ('20', 'Medium'),
            ('30', 'High')
        ]

    def queryset(self, request, queryset: QuerySet[Any]):
        if self.value() == '10':
            return queryset.filter(inventory__lte=10)
        elif self.value() == '20':
            return queryset.filter(inventory__lte=20)
        elif self.value() == '30':
            return queryset.filter(inventory__lte=30)


class ProductImageInline(admin.TabularInline):
    model = models.ProductImage
    readonly_fields = ['thumbnail']

    def thumbnail(self, instance):
        if instance.image.name != '':
            thumbnail_image = format_html(
                f'<img src = "{instance.image.url}"  class = "thumbnail" />')
            return thumbnail_image
        else:
            return ''


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    actions = ['clear_inventory']
    autocomplete_fields = ['collection']
    inlines = [ProductImageInline]
    list_display = ['title', 'unit_price',
                    'inventory_status', 'collection_title']
    list_editable = ['unit_price']
    list_filter = ['collection', 'last_update', InventoryFilter]
    ordering = ['title']
    list_per_page = 10
    list_select_related = ['collection']
    prepopulated_fields = {
        'slug': ['title']  # we can add here as many fields as we want
    }
    search_fields = ['title']

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        elif 10 < product.inventory < 20:
            return 'Medium'
        else:
            return 'High'

    def collection_title(self, product):
        return product.collection.title

# this function that we had made will not delete the product it will clear its inventory only
    @admin.action(description='Clear Inventory')
    def clear_inventory(self, request, queryset):
        update_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f'{update_count} Products are successfully updated'
        )

    class Media:
        css = {
            'all': ['store/styles.css']
        }


@admin.register(models.Customer)
class CustomerAmin(admin.ModelAdmin):
    autocomplete_fields = ['user']
    list_display = ['first_name', 'last_name', 'membership', 'order_count']
    list_editable = ['membership']
    list_per_page = 10
    list_select_related = ['user']
    ordering = ['user__first_name', 'user__last_name']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']

    @admin.display(ordering='order_count')
    def order_count(self, customer):
        url = (
            reverse('admin:store_order_changelist')  # app_model_page
            + '?'
            + urlencode(
                {
                    'customer__id': str(customer.id)
                }
            )
        )
        return format_html('<a href="{}">{}</a>', url, customer.id)


# we can also use the stack inline at the place of tabular
class OrderItemInline(admin.StackedInline):
    autocomplete_fields = ['product']
    min_num = 1
    max_num = 10
    model = models.OrderItem
    extra = 0


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ['customer']
    inlines = [OrderItemInline]
    list_display = ['id', 'placed_at', 'customer']
