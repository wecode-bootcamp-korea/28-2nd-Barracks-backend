<<<<<<< HEAD
import json

from django.test     import TestCase, Client
from postings.models import Posting, Space, Size, Residence, Style, Image, Comment
from users.models    import User
from my_settings     import SECRET_KEY, ALGORITHM

class PostingDetailTest(TestCase):
    def setUp(self):
        self.client = Client()
        
        User.objects.create(
            kakao_id          = 123,
            id                = 1,
            email             = 'abc@ab.com',
            nickname          = 'kk',
            profile_image_url = 'aaa.jpg'
        )
         
        Space.objects.create(
            id   = 1,
            name = 'A'
        )
        
        Size.objects.create(
            id   = 1,
            name = '10평'
        )
        
        Residence.objects.create(
            id   = 1,
            name = '아파트'
        )
        
        Style.objects.create(
            id   = 1,
            name = '빈티지'
        )
        
        Posting.objects.create(
            id           = 1,
            title        = 'title 1 입니다',
            content      = 'posting 1 desc',
            tags         = '#갬성,#인테리어',
            space_id     = 1,
            size_id      = 1,
            residence_id = 1,
            style_id     = 1,
            hits         = 0,
            user_id      = 1
        )
        
        Comment.objects.create(
            content    = 'comment content 1',
            posting_id = 1,
            user_id    = 1
        )
        
        Image.objects.create(
            id         = 1,
            posting_id = 1,
            image_url  = 'url1'
        )
        
    def tearDown(self):
        User.objects.all().delete()
        Space.objects.all().delete()
        Style.objects.all().delete()
        Residence.objects.all().delete()
        Size.objects.all().delete()
        Posting.objects.all().delete()
        Comment.objects.all().delete()
        Image.objects.all().delete()
        
    def test_posting_detail_view_get_success(self):
        client   = Client()
        response = client.get('/postings/1')
        
        result = {
            'posting_id' : 1,
            'title'      : 'title 1 입니다',
            'content'    : 'posting 1 desc',
            'tags'       : ['#갬성','#인테리어'],
            'size'       : '10평',
            'residence'  : '아파트',
            'space'      : 'A',
            'style'      : '빈티지',
            'hits'       : 1,
            'image_urls' : [{'image_id': 1, 'image_url': 'url1'}],
            'user_name'  : 'kk',
            'user_image' : 'aaa.jpg'
        }
        
        self.assertEqual(response.json(),{'result' : result}) 
        self.assertEqual(response.status_code, 200)
        
    def test_posting_detail_view_get_doesnotexist(self):
        client   = Client()
        response = client.get('/postings/5')
        self.assertEqual(response.json(),
            {
                'message' : 'POSTING_DOESNOT_EXIST'
            }
        )
        self.assertEqual(response.status_code, 404)
=======
from django.test import TestCase
from users.models import User
from postings.models import Posting, Image, Size, Space, Residence, Style
import unittest

# Create your tests here.

class PostingViewTest(unittest.TestCase):
    def setUp(self):
        User.objects.create(
            id = 1,
            kakao_id          = show3045,
            email             = joshua.jung0129@gmail.com,
            nickname          = daydream03,
            profile_image_url = asdf@asdf.com
        )
    def test_post_success(self):


    def test_post_key_error(self)
>>>>>>> a255457 (포스팅 기능 구현 완료)
