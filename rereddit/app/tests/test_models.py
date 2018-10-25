from django.test import TestCase
from django.contrib.auth.models import User
from app.models import Profile, Thread


class UserTestClass(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(
            username='jacob', email='jacob@qq.com', password='top_secret')

    def test_username_label(self):
        user = User.objects.get(id=1)
        field_label = user._meta.get_field('username').verbose_name
        self.assertEquals(field_label, 'username')

    def test_email_label(self):
        user = User.objects.get(id=1)
        field_label = user._meta.get_field('email').verbose_name
        self.assertEquals(field_label, 'email address')

    def test_password_label(self):
        user = User.objects.get(id=1)
        field_label = user._meta.get_field('password').verbose_name
        self.assertEquals(field_label, 'password')


