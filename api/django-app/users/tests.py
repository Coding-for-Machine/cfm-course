from django.test import TestCase
from .models import MyUser, Profile

class UserModelTest(TestCase):

    def test_create_user(self):
        user = MyUser.objects.create_user(username="testuser", password="password123", telegram_id=123456)
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.telegram_id, 123456)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        superuser = MyUser.objects.create_superuser(username="admin", password="adminpass")
        self.assertEqual(superuser.username, "admin")
        self.assertTrue(superuser.is_active)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

    def test_profile_created_with_user(self):
        user = MyUser.objects.create_user(username="profileuser", password="password123")
        profile = Profile.objects.get(user=user)
        self.assertIsNotNone(profile)
        self.assertEqual(profile.user.username, "profileuser")
        self.assertEqual(profile.age, 12)  # default age

    def test_profile_avatar_url(self):
        user = MyUser.objects.create_user(username="avataruser", password="password123")
        profile = user.profile
        self.assertIn("/static/images/user.png", profile.avatar_url)
