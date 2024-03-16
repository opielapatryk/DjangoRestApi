from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient
from users.serializers import UserSerializer

class UserAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create(username='testuser1')
        self.user2 = User.objects.create(username='testuser2')

    def test_list_users(self):
        response = self.client.get(reverse('user-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        usernames = [user['username'] for user in response.data['results']]
        self.assertIn(self.user1.username, usernames)
        self.assertIn(self.user2.username, usernames)

    def test_retrieve_user(self):
        response = self.client.get(reverse('user-detail', kwargs={'pk': self.user1.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user1.username)

    def test_retrieve_wrong_user(self):
        response = self.client.get(reverse('user-detail', kwargs={'pk': 3}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_user(self):
        data = {'username': 'newuser'}
        response = self.client.post(reverse('user-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_update_user(self):
        data = {'username': 'updateduser'}
        response = self.client.put(reverse('user-detail', kwargs={'pk': self.user1.pk}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.get(pk=self.user1.pk).username, 'updateduser')

    def test_delete_user(self):
        response = self.client.delete(reverse('user-detail', kwargs={'pk': self.user1.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(pk=self.user1.pk).exists())

    def test_serializer(self):
        serializer_data = UserSerializer(instance=self.user1).data
        expected_data = {'id': self.user1.id, 'username': self.user1.username}
        self.assertEqual(serializer_data, expected_data)
