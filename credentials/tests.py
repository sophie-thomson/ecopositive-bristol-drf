from django.contrib.auth.models import User
from .models import Credential
from rest_framework import status
from rest_framework.test import APITestCase


class CredentialListViewTests(APITestCase):
    """
    Tests that the company owner can view a list of credentials,
    add a new credential when logged in as company owner, and is
    forbidden to view or create a list of credentials when not the
    company owner.
    setUp creates the test case user and credentials to list.
    """
    def setUp(self):
        wonderwoman = User.objects.create_user(
            username='wonderwoman',
            password='pass'
        )
        Credential.objects.create(
            owner=wonderwoman,
            name='Fly using superpowers',
            group='Eco-Conscious Approach',
        )
        Credential.objects.create(
            owner=wonderwoman,
            name='100% Renewable Energy',
            group='Eco-Conscious Approach',
        )

    def test_can_list_all_credentials(self):
        Credential.objects.get(name='Fly using superpowers')
        Credential.objects.get(name='100% Renewable Energy')

        response = self.client.get('/credentials/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_logged_in_user_can_create_credential(self):
        self.client.login(username='wonderwoman', password='pass')
        response = self.client.post(
            '/credentials/',
            {
                'name': 'another credential',
                'group': 'Eco-Conscious Approach',
            }
        )
        count = Credential.objects.count()
        self.assertEqual(count, 3)
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED)

    def test_cant_create_credential_if_not_logged_in(self):
        response = self.client.post(
            '/credentials/',
            {
                'name': 'another credential',
                'group': 'Eco-Conscious Approach',
            }
        )
        self.assertEqual(
            response.status_code, status.HTTP_403_FORBIDDEN)


class CredentialDetailViewTests(APITestCase):
    """
    Tests that a particular credential can be retrieved, that the
    credential owner can edit and delete the credential, and that
    it is forbidden for a non-owner to edit or delete the credential.
    setUp creates the test case users and credentials to be retrieved.
    """
    def setUp(self):
        wonderwoman = User.objects.create_user(
            username='wonderwoman',
            password='pass'
        )
        storm = User.objects.create_user(
            username='storm',
            password='pass'
        )
        Credential.objects.create(
            owner=wonderwoman,
            name='Fly using superpowers',
            group='Eco-Conscious Approach',
        )
        Credential.objects.create(
            owner=storm,
            name='Uses wind energy',
            group='Eco-Conscious Approach',
        )

    def test_can_retrieve_credential_using_valid_id(self):
        response = self.client.get('/credentials/1/')
        self.assertEqual(response.data['name'], 'Fly using superpowers')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cant_retrieve_credential_using_invalid_id(self):
        response = self.client.get('/credentials/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_owner_can_update_own_credential(self):
        self.client.login(username='wonderwoman', password='pass')
        response = self.client.put(
            '/credentials/1/',
            {
                'name': 'Fly in a plane',
                'group': 'Eco-Conscious Approach',
            }
        )
        credential = Credential.objects.filter(pk=1).first()
        self.assertEqual(credential.name, 'Fly in a plane')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cant_update_credential_logged_in_but_not_owner(self):
        self.client.login(username='storm', password='pass')
        response = self.client.put(
            '/credentials/1/',
            {
                'name': 'Fly in a plane',
                'group': 'Eco-Conscious Approach',
            }
        )
        self.assertEqual(
            response.status_code, status.HTTP_403_FORBIDDEN)
