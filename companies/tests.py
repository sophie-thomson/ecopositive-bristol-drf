from django.contrib.auth.models import User
from .models import Company
from rest_framework import status
from rest_framework.test import APITestCase


class CompanyListViewTests(APITestCase):
    def setUp(self):
        wonderwoman = User.objects.create_user(
            username='wonderwoman',
            password='pass'
        )
        Company.objects.create(
            owner=wonderwoman,
            name='company name',
            excerpt='wonderwomans excerpt',
            description='wonderwomans company description',
            contact_name='test',
            contact_email='test@email.com',
            role='test role',
        )

    def test_can_list_companies(self):
        self.client.login(username='wonderwoman', password='pass')
        Company.objects.get(name='company name')
        response = self.client.get('/companies/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logged_in_user_can_create_company(self):
        self.client.login(username='wonderwoman', password='pass')
        Company.objects.get(name='company name')
        response = self.client.post(
            '/companies/',
            {
                'name': 'another company name',
                'excerpt': 'company excerpt',
                'description': 'company description',
                'contact_name': 'test',
                'contact_email': 'test2@email.com',
                'role': 'test role',
            },
        )
        count = Company.objects.count()
        self.assertEqual(count, 2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_not_logged_in_cant_create_company(self):
        response = self.client.post('/companies/', {'name': 'company name'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class CompanyDetailViewTests(APITestCase):
    def setUp(self):
        wonderwoman = User.objects.create_user(
            username='wonderwoman',
            password='pass'
        )
        storm = User.objects.create_user(
            username='storm',
            password='pass'
        )
        Company.objects.create(
            owner=wonderwoman,
            name='company name',
            excerpt='wonderwomans excerpt',
            description='wonderwomans company description',
            contact_name='test',
            contact_email='test@email.com',
            role='test role',
        )
        Company.objects.create(
            owner=storm,
            name='another company name',
            excerpt='storms excerpt',
            description='storms company description',
            contact_name='test',
            contact_email='test2@email.com',
            role='test role',
        )

    def test_can_retrieve_company_using_valid_id(self):
        response = self.client.get('/companies/1/')
        self.assertEqual(response.data['name'], 'company name')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cant_retrieve_company_using_invalid_id(self):
        response = self.client.get('/companies/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_update_own_company(self):
        self.client.login(username='wonderwoman', password='pass')
        response = self.client.put(
            '/companies/1/',
            {
                'name': 'new company name',
                'excerpt': 'wonderwomans excerpt',
                'description': 'wonderwomans company description',
                'contact_name': 'test',
                'contact_email': 'test@email.com',
                'role': 'test role',
            },
        )
        company = Company.objects.filter(pk=1).first()
        self.assertEqual(company.name, 'new company name')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cant_update_another_users_company(self):
        self.client.login(username='wonderwoman', password='pass')
        response = self.client.put(
            '/companies/2/',
            {
                'name': 'new company name',
                'excerpt': 'company excerpt',
                'description': 'company description',
                'contact_name': 'test',
                'contact_email': 'test2@email.com',
                'role': 'test role',
            },
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
