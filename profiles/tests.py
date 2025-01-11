from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase


class ProfileDetailViewTests(APITestCase):
    """
    Tests that the user can view their own profile,
    edit their profile as the profile owner,
    and is forbidden to edit the profile when not the owner.
    setUp creates the test case users.
    """
    def setUp(self):
        User.objects.create_user(
            username='wonderwoman',
            password='pass',
        )

        User.objects.create_user(
            username='storm',
            password='pass',
        )

    def test_can_retrieve_profile_using_valid_id(self):
        response = self.client.get('/profiles/1/')
        self.assertEqual(response.data['owner'], 'wonderwoman')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cant_retrieve_profile_using_invalid_id(self):
        response = self.client.get('/profiles/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_update_own_profile(self):
        self.client.login(username='wonderwoman', password='pass')
        response = self.client.get('/profiles/1/')
        self.assertEqual(response.data['first_name'], '')
        response = self.client.put(
            '/profiles/1/',
            {
                'first_name': 'jane',
            })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'jane')

    def test_user_cant_update_another_users_profile(self):
        self.client.login(username='storm', password='pass')
        response = self.client.get('/profiles/1/')
        self.assertEqual(response.data['first_name'], '')
        response = self.client.put(
            '/profiles/1/',
            {
                'first_name': 'wendy',
            })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
