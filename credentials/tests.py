from django.contrib.auth.models import User
from .models import Credential
from companies.models import Company
from rest_framework import status
from rest_framework.test import APITestCase


class CredentialListViewTests(APITestCase):
    """
    Tests that the company owner can view a list of credentials,
    add a new credential when logged in as company owner, and is
    forbidden to view or create a list of credentials when not the
    company owner.
    setUp creates the test case user and company for the credential
    to be assigned to.
    """
    def setUp(self):
        wonderwoman = User.objects.create_user(
            username='wonderwoman',
            password='pass'
        )
        Company.objects.create(
            owner=wonderwoman,
            name='company name',
            excerpt='wonderwomans excerpt',
            description='wonderwomans company description'
        )
        Credential.objects.create(
            name='Fly using superpowers',
            group='Superheroes',
        )
        Credential.objects.create(
            name='100% Renewable Energy',
            group='Superheroes',
        )

    def test_can_list_all_credentials(self):
        Company.objects.get(name='company name')
        Credential.objects.get(name='Fly using superpowers')
        Credential.objects.get(name='100% Renewable Energy')

        response = self.client.get('/credentials/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_can_add_credential_as_authenticated_user(self):
        self.client.login(username='wonderwoman', password='pass')
        Company.objects.get(name='company name')
        response = self.client.post(
            '/credentials/',
            {
                'name': 'another credential',
                'group': 'Superheroes',
            }
        )
        count = Credential.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED)

    # def test_cant_create_credential_if_not_logged_in(self):
    #     Company.objects.get(name='company name')
    #     Credential.objects.get(name='Fly using superpowers')
    #     Credential.objects.get(name='100% Renewable Energy')
    #     Credential.objects.create(
    #         name='another credential',
    #         group='Superheroes',
    #     )

    #     response = self.client.get('/credentials/')
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    #     self.assertEqual(len(response.data), 3)
