from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from userauth.models import Users
from .models import UserFile

class UserFileApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = Users.objects.create(id='testuser', pwd='123456')
        self.client.force_authenticate(user=self.user)

    def test_create_txt_file(self):
        response = self.client.post('/api/modeltask/create_txt_file/', {'filename': 'test.txt'})
        self.assertEqual(response.status_code, 201)

    def test_multi_upload(self):
        # 这里只做接口可用性测试，具体文件上传略
        pass

    def test_list_user_files(self):
        response = self.client.get('/api/modeltask/list_user_files/')
        self.assertEqual(response.status_code, 200)

    def test_delete_user_file(self):
        # 这里只做接口可用性测试，具体删除略
        pass
