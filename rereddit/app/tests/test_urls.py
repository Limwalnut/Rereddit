from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.urls import reverse
from app.views import index, signup_view, login_view, logout_view, thread_list, thread_detail, thread_create, profile_view
from app import urls
from app import views


class HomePageTest(TestCase):
    def test_root_url_resolves_to_index_view(self):
        found = resolve('/')
        self.assertEqual(found.func, index)

    # def test_view_uses_correct_template(self):
    #     response = self.client.get(reverse('home'))
    #     self.assertEquals(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'index.html')


class SignUpTest(TestCase):
    def test_signup_url_resolves_to_signup_view(self):
        found = resolve('/signup/')
        self.assertEqual(found.func, signup_view)


class LoginTest(TestCase):
    def test_login_url_resolves_to_login_view(self):
        found = resolve('/login/')
        self.assertEqual(found.func, login_view)


class ThreadListTest(TestCase):
    def test_threads_url_resolves_to_threads_view(self):
        found = resolve('/threads/')
        self.assertEqual(found.func, thread_list)


class ThreadDetailTest(TestCase):
    def test_thread_detail_url_resolves_to_thread_detail_view(self):
        found = resolve('/thread/1/')
        self.assertEqual(found.func, thread_detail)


class ThreadCreateTest(TestCase):
    def test_thread_create_url_resolves_to_thread_create_view(self):
        found = resolve('/thread/create/')
        self.assertEqual(found.func, thread_create)


class ProfileTest(TestCase):
    def test_profile_url_resolves_to_profile_view(self):
        found = resolve('/profile/1/')
        self.assertEqual(found.func, profile_view)

        # url = reverse('profile', args=[1])
        # self.assertEqual(url, '/profile/1988/')
