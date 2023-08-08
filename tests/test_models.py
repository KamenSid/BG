from django.contrib.auth import get_user_model
from django.test import TestCase

from BG.testdb.models import Replay

User = get_user_model()


def get_first_user():
    return User.objects.first()


class ModelsTestCase(TestCase):
    def setUp(self):
        User.objects.create(email="test_user@mail.com",
                            password="testpass"
                            )
        Replay.objects.create(title="Test Model",
                              author=get_first_user(),
                              video_url='www.someurl.com',
                              description='This is a test',
                              game='Rust'
                              )

    def test_replay_creation(self):
        replay = Replay.objects.get(title="Test Model")

        self.assertEqual(replay.title, "Test Model")
        self.assertEqual(replay.author, get_first_user())
        self.assertEqual(replay.video_url, 'www.someurl.com')
        self.assertEqual(replay.description, 'This is a test')
        self.assertEqual(replay.game, 'Rust')

    def test_profile_creation(self):
        user = get_first_user()
        profile = user.appuserprofile
        profile.steam_id = "00000"

        self.assertEqual(profile.username, 'test_user')
        self.assertEqual(profile.app_user, user)
        self.assertEqual(profile.steam_id, '00000')

    def test_profile_deleted_after_user_deletion(self):
        user = get_first_user()
        user.delete()

        with self.assertRaises(User.appuserprofile.RelatedObjectDoesNotExist):
            profile = user.appuserprofile

