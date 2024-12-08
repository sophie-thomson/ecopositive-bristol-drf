from django.contrib.auth.models import User
from .models import Company
from rest_framework import status
from rest_framework.test import APITestCase


class CompanyListViewTests(APITestCase):
    def setUp(self):
        User.objects.create_user(username='wonderwoman', password='battle')

    def test_can_list_companies(self):
        wonderwoman = User.objects.get(username='wonderwoman')
        Company.objects.create(owner=wonderwoman, name='testcase company name')
        response = self.client.get('/companies/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        print(len(response.data))

    # def test_logged_in_user_can_create_company(self):
    #     self.client.login(username='wonderwoman', password='battle')
    #     response = self.client.post('/companies/', {'name': 'testcase company name'})
    #     count = Company.objects.count()
    #     self.assertEqual(count, 1)
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # def test_user_not_logged_in_cant_create_company(self):
    #     response = self.client.post('/companies/', {'name': 'testcase company name'})
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
