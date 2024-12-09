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


class CommentDetailViewTests(APITestCase):
    """
    Tests that the user can view a particular comment,
    edit a comment when logged in as the comment owner,
    and is forbidden to edit a comment when not the owner.
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

        storm = User.objects.create_user(
            username='storm',
            password='pass'
        )
        Company.objects.create(
            owner=storm,
            name='another company name',
            excerpt='storms excerpt',
            description='storms company description'
        )

    def test_can_retrieve_comment_using_valid_id(self):
        wonderwoman = User.objects.get(username='wonderwoman')
        company = Company.objects.get(name='company name')

        Comment.objects.create(
            owner=wonderwoman,
            company=company,
            content='test comment'
        )
        response = self.client.get('/comments/1/')
        self.assertEqual(response.data['content'], 'test comment')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cant_retrieve_comment_using_invalid_id(self):
        response = self.client.get('/comments/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_update_own_comment(self):
        wonderwoman = User.objects.get(username='wonderwoman')
        company = Company.objects.get(name='company name')
        self.client.login(username='wonderwoman', password='pass')
        Comment.objects.create(
            owner=wonderwoman,
            company=company,
            content='test comment'
        )
        response = self.client.put(
            '/comments/1/',
            {
                'company': 1,
                'content': 'updated comment content',
            },
        )
        comment = Comment.objects.filter(pk=1).first()
        self.assertEqual(comment.content, 'updated comment content')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cant_update_another_users_comment(self):
        wonderwoman = User.objects.get(username='wonderwoman')
        company = Company.objects.get(name='company name')
        Comment.objects.create(
            owner=wonderwoman,
            company=company,
            content='wonderwomans test comment'
        )
        User.objects.get(username='storm')
        self.client.login(username='storm', password='pass')
        response = self.client.put(
            '/comments/1/',
            {
                'company': 1,
                'content': 'storms updated comment',
            },
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
