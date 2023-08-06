from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from BG.testdb.models import Replay

User = get_user_model()


class ReplayViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='testuser@mail.com', password='testpassword')
        self.replay = Replay.objects.create(title='Test Replay', game='Test Game', description='Test Description',
                                            author=self.user)

    def test_replay_detail_view(self):
        self.assertEqual(self.replay.title, 'Test Replay')
        self.assertEqual(self.replay.game, 'Test Game')
        self.assertEqual(self.replay.description, 'Test Description')
        self.assertEqual(self.replay.author, self.user)
