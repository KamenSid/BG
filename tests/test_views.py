from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from BG.forms import CommentInputForm
from BG.testdb.models import Replay
from BG.members.models import Like, Guild

User = get_user_model()


class ViewsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test_user@mail.com',
            password='testpassword'
        )
        self.client.login(email='test_user@mail.com', password='testpassword')

        self.replay = Replay.objects.create(
            title='Test Replay',
            author=self.user,
            video_url='https://youtube.com/shorts/3A7tGcEAvj8?feature=share',
            description='This is a test',
            game='Rust',
        )

        self.guild = Guild.objects.create(
            name='Test Guild',
            leader=self.user,
            banner='',
        )

    def test_upload_replay_view(self):
        replay_data = {
            'title': 'Test Replay 1',
            'author': self.user,
            'video_url': 'https://youtube.com/shorts/3A7tGcEAvj8?feature=share',
            'description': 'This is a test for upload',
            'game': 'Rust',
        }
        response = self.client.post(reverse('upload-replay'), replay_data)
        self.assertEqual(response.status_code, 302)

        replay = Replay.objects.get(title='Test Replay 1')

        self.assertEqual(replay.title, 'Test Replay 1')
        self.assertEqual(replay.video_url, 'https://youtube.com/shorts/3A7tGcEAvj8?feature=share')
        self.assertEqual(replay.description, 'This is a test for upload')
        self.assertEqual(replay.game, 'Rust')

    def test_update_replay_view(self):
        # Update with new info

        updated_data = {
            'title': 'Updated Title',
            'video_url': 'https://youtube.com/shorts/4A7tGcEAvj8?feature=share',
            'description': 'Updated description',
            'game': 'Updated Game',
        }

        response = self.client.post(reverse('update-replay', kwargs={'pk': self.replay.pk}), updated_data)

        self.assertEqual(response.status_code, 302)
        self.replay.refresh_from_db()
        self.assertEqual(self.replay.title, 'Updated Title')
        self.assertEqual(self.replay.video_url, 'https://youtube.com/shorts/4A7tGcEAvj8?feature=share')
        self.assertEqual(self.replay.description, 'Updated description')
        self.assertEqual(self.replay.game, 'Updated Game')

    def test_replay_delete_view(self):
        response = self.client.post(reverse('replay-delete', args=[self.replay.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Replay.objects.filter(pk=self.replay.pk).exists())

    def test_like_replay_view(self):
        response = self.client.get(reverse('like-replay', args=[self.replay.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Like.objects.filter(user=self.user, replay=self.replay).exists())

        # Test unliking the replay
        response = self.client.get(reverse('like-replay', args=[self.replay.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Like.objects.filter(user=self.user, replay=self.replay).exists())

    def test_profile_view(self):
        response = self.client.get(reverse('profile-details', args=[self.user.pk]))
        self.assertEqual(response.status_code, 200)
        uploaded_replays = response.context['test_replays']
        new_user = response.context['appuser']
        replays_count = response.context['replays_count']
        liked_replays = response.context['liked_replays']
        owner = response.context['owner']

        self.assertEqual(new_user, self.user)
        self.assertEqual(uploaded_replays.count(), 1)
        self.assertEqual(replays_count, 1)
        self.assertEqual(liked_replays.count(), 0)
        self.assertTrue(owner)

    def test_replay_details_view(self):
        response = self.client.get(reverse('replay-details', kwargs={'pk': self.replay.pk}))
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, self.replay.title)
        self.assertIsInstance(response.context['comment_form'], CommentInputForm)

        comment_data = {'content': 'This is a test comment'}
        response = self.client.post(reverse('replay-details', kwargs={'pk': self.replay.pk}), comment_data)
        self.assertEqual(response.status_code, 302)

        self.assertTrue(self.replay.comment_set.filter(content='This is a test comment').exists())

    def test_guild_add_members_view(self):
        invited_user = User.objects.create_user(
            email='invited_user@mail.com',
            password='invitedpassword'
        )
        self.user.appuserprofile.guild = self.guild
        self.user.appuserprofile.save()
        response = self.client.post(reverse('guild-add-members'), {
            'invite_member': invited_user.appuserprofile.username
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(f"You have added {invited_user.appuserprofile.username} to {self.guild.name}",
                      response.content.decode())
        invited_user.appuserprofile.refresh_from_db()
        self.assertTrue(invited_user.appuserprofile.guild_id == self.guild.id)

        response = self.client.post(reverse('guild-add-members'), {  # Test trying to invite a member already in a guild
            'invite_member': invited_user.appuserprofile.username
        })
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('guild-add-members'), {  # Test removing a member
            'remove_member': invited_user.appuserprofile.username
        })
        invited_user.appuserprofile.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertTrue(invited_user.appuserprofile.guild is None)
