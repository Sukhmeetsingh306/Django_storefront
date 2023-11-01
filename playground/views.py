'''
For the sending email 
'''

from django.core.cache import cache
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.views import APIView
# from .tasks import notify_customer
import requests


class HelloView(APIView):
    @method_decorator(cache_page(5 * 60))
    def get(self, request):
        response = requests.get('https://httpbin.org/delay/2')
        data = response.json()

        return render(request, 'hello.html', {'name': 'Sukhmeet'})

# @cache_page(5 * 20)
# def say_hello(request):
#     # notify_customer.delay('hello')
#     # key = 'httpbin_result'
#     # if cache.get(key) is None:
#     #     response = requests.get('https://httpbin.org/delay/2')
#     #     data = response.json()
#     #     cache.set(key, data)
#     response = requests.get('https://httpbin.org/delay/2')
#     data = response.json()

#     return render(request, 'hello.html', {'name': data})

    # return render(request, 'hello.html', {'name': cache.get(key)})
    # queryset = Product.objects.raw('select id, title from store_product')
    # return render(request, 'hello.html', {'name': 'Sukhmeet', 'tags': list(queryset)})
