'''
For the sending email 
'''

from django.shortcuts import render
from .tasks import notify_customer


def say_hello(request):
    notify_customer.delay('hello')

    return render(request, 'hello.html', {'name': 'Sukhmeet'})
    # queryset = Product.objects.raw('select id, title from store_product')
    # return render(request, 'hello.html', {'name': 'Sukhmeet', 'tags': list(queryset)})
