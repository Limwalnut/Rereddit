from django.test import TestCase


class TestIndexView(TestCase):
    # @classmethod
    # def setUpTestData(cls):
    #     user = User.objects.create_user(
    #         username='jacob', email='jacob@qq.com', password='top_secret')

    def test_index_status_code(self):
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)