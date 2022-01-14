from .models       import User
from django.test   import TestCase,Client
from unittest.mock import patch, MagicMock

class UserTest(TestCase):
    def setUp(self):
        User.objects.create(
            kakao_id          = 1234,
            nickname          = "이아영",
            profile_image_url = "http://k.kakaocdn.net/dn/bQpvV5/btrp8qGq28a/uaHemjFTr9t58sqvn9YYAK/img_340x340.jpg",
            email             = "dkdud5135@kakao.com"
        )

    def tearDown(self):
        User.objects.all().delete()

    @patch("users.views.requests")
    def test_kakao_login_new_user_success(self, mocked_requests):
        client = Client()

        class MockedResponse:
            def json(self):
                return {
                    "id": 2074410349,
                    "properties": {
                        "nickname": "아영",
                        "profile_image": "http://k.kakaocdn.net/dn/bQpvV5/btrp8qGq28a/uaHemjFTr9t58sqvn9YYAK/img_640x640.jpg"
                    },
                    "kakao_account": {
                        "email": "dkdud2408@kakao.com"
                    }
                } 
        mocked_requests.get = MagicMock(return_value = MockedResponse())
        headers             = {"HTTP_Authorization" : "fake_access_token"}
        response            = client.get("/users/login", **headers)

        self.assertEqual(response.status_code, 200)

    @patch("users.views.requests")
    def test_kakao_login_key_error(self, mocked_requests):
        client = Client()

        class MockedResponse:
            def json(self):
                return {
                    "id": 2074410349,
                    "properties": {
                        "nickname": "아영",
                        "profile_image": "http://k.kakaocdn.net/dn/bQpvV5/btrp8qGq28a/uaHemjFTr9t58sqvn9YYAK/img_640x640.jpg"
                    },
                    "kakao_account": {
                        "email": "dkdud2408@kakao.com"
                    }
                } 
        mocked_requests.get = MagicMock(return_value = MockedResponse())
        headers             = {"HTTP_Authotion" : "fake_access_token"}
        response            = client.get("/users/login", **headers)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                'message' : 'KEY_ERROR'
            }
        )