'''
This file is made to test the code behavior not the implementation

The every file name, class, function should start with the name test
'''

from rest_framework import status
from rest_framework.test import APIClient
import pytest


@pytest.mark.django_db
class TestCreateCollection:
    def test_if_the_user_is_anonymous_returns_401(self):
        client = APIClient()
        response = client.post('/store/collections/', {'title': 'a'})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
