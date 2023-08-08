from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from BG.testdb.models import Replay
from BG.members.models import Like

User = get_user_model()


class ViewsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test_user@mail.com',
            password='testpassword'
        )
        self.client.login(email='testuser', password='testpassword')

    def test_update_replay_view(self):
        replay = Replay.objects.create(
            title='Test Replay',
            author=self.user,
            video_url='www.example.com',
            description='This is a test',
            game='Rust'
        )
        # Update with new info

        updated_data = {
            'title': 'Updated Title',
            'video_url': 'www.updated.com',
            'description': 'Updated description',
            'game': 'Updated Game',
        }

        response = self.client.post(reverse('update-replay', args=[replay.pk]), **updated_data)

        self.assertEqual(response.status_code, 302)
        replay.refresh_from_db()
        self.assertEqual(replay.title, 'Updated Title')

    def test_like_replay_view(self):
        replay = Replay.objects.create(
            title='Test Replay',
            author=self.user,
            video_url='www.example.com',
            description='This is a test',
            game='Rust'
        )
        response = self.client.post(reverse('like-replay', args=[replay.pk]))  # Like the replay
        self.assertEqual(response.status_code, 302)
        self.assertEqual(replay.like_set.count(), 1)
        response = self.client.post(reverse('like-replay', args=[replay.pk]))  # Unlike the replay
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Like.objects.count(), 0)

    # TODO
    # def test_profile_view(self):

    # def test_upload_replay_view(self):

    # def test_replay_delete_view(self):

    # def test_replay_details_view(self):

    # def test_update_profile_view(self):
