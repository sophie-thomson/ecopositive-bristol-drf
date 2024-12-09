from django.contrib.auth.models import User
from .models import Comment, Company
from rest_framework import status
from rest_framework.test import APITestCase


class CommentListViewTests(APITestCase):
    """
    Tests that the user can view a list of comments,
    create a comment when logged in, and is forbidden to
    create a comment when not logged in.
    setUp creates the test case user and company for the comment
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

    def test_can_list_all_comments(self):
        wonderwoman = User.objects.get(username='wonderwoman')
        company = Company.objects.get(name='company name')

        Comment.objects.create(
            owner=wonderwoman,
            company=company,
            content='test comment'
        )
        Comment.objects.create(
            owner=wonderwoman,
            company=company,
            content='another test comment'
        )
        response = self.client.get('/comments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_logged_in_user_can_create_comment(self):
        self.client.login(username='wonderwoman', password='pass')
        Company.objects.get(name='company name')
        response = self.client.post(
            '/comments/',
            {
                'company': 1,
                'content': 'test comment content',
            },
        )
        count = Comment.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_not_logged_in_cant_create_comment(self):
        Company.objects.get(name='company name')
        response = self.client.post(
            '/comments/',
            {
                'company': 1,
                'content': 'test comment content',
            }
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
