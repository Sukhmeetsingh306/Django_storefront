'''

This file is made to test the code behavior not the implementation

The every file name, class, function should start with the name test

'''

from rest_framework import status
from store.models import Product, Collection
from model_bakery import baker
import pytest


@pytest.fixture
def create_products(api_client):
    def do_store_product(product):
        return api_client.post('/store/products/', product)
    return do_store_product


@pytest.mark.django_db
class TestCreateProduct:
    def test_if_the_user_is_anonymous_returns_401(self, create_products):
        response = create_products({'title': 'a'})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_the_user_is_not_admin_returns_403(self, create_products, authenticate):
        authenticate()

        response = create_products({'title': 'a'})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_invalid_returns_400(self, create_products, authenticate):
        authenticate(is_staff=True)

        response = create_products({'title': ''})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'] is not None

    # def test_if_data_is_valid_returns_201(self, create_products, authenticate):
    #     authenticate(is_staff=True)

    #     response = create_products({'title': 'a'})

    #     assert response.status_code == status.HTTP_201_CREATED
    #     assert response.data['id'] > 0


# @pytest.mark.django_db
# class TestRetrieveProduct:
#     def test_if_collection_exists_returns_200(self, api_client):
#         product = baker.make(Product)
#         # collection = baker.make(Collection)

#         response = api_client.get(f'/store/products/{product.id}/')

#         assert response.status_code == status.HTTP_200_OK
#         assert response.data == {
#             'id': product.id,
#             'title': product.title,
#             'description': product.description,
#             'slug': product.slug,
#             'inventory': product.inventory,
#             'unit_price': product.unique_error_message,
#             'collection': product.collection,
#             'images': [],
#         }
