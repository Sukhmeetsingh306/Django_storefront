'''
In this file we are going to test the 

Register, Sign in, Sign Out 

And the Browsing of the products
'''

from random import randint
from locust import task, between, HttpUser


class WebsiteUser(HttpUser):
    # Viewing product
    # Viewing product detail
    # Add Product to the cart

    wait_time = between(1, 5)

    @task(2)
    def view_products(self):  # view multiple products
        collection_id = randint(2, 6)
        self.client.get(
            f'/store/products/?collection_id={collection_id}',
            name='/store/products',
        )

    @task(4)
    def view_product(self):  # to view particular product
        product_id = randint(1, 1000)
        self.client.get(
            f'/store/products/{product_id}',
            name='/store/products/:id'
        )

    @task(1)
    def add_to_cart(self):  # to add product in cart
        product_id = randint(1, 10)
        self.client.post(
            f'/store/carts/{self.cart_id}/items/',
            name='/store/carts/items',
            json={
                'product_id': product_id,
                'quantity': 1,
            }
        )

    def on_start(self):
        response = self.client.post('/store/carts/')
        result = response.json()
        self.cart_id = result['id']

    @task
    def say_hello(self):
        self.client.get("/playground/hello/")
