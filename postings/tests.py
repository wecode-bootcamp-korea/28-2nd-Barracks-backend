import json
from unittest import result
from urllib import request
import jwt

from django.test     import TestCase, Client

from postings.models import Posting, Space, Size, Residence, Style, Image, Comment, Like
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

class PostingLikeTest(TestCase):
    def setUp(self):
        self.client = Client()
        
        User.objects.create(
            kakao_id          = 1538472,
            id                = 6,
            email             = 'qwer@qwer.com',
            nickname          = '자취생',
            profile_image_url = 'abcdeg1234.jpg'
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
            id           = 5,
            title        = 'title 5 입니다',
            content      = 'posting 5 desc',
            tags         = '#집꾸미기,#자취,#원룸',
            space_id     = 1,
            size_id      = 1,
            residence_id = 1,
            style_id     = 1,
            hits         = 2,
            user_id      = 6
        )

        Image.objects.create(
            posting_id = 5,
            image_url = 'image_url'
        )
        Like.objects.create(
            user_id = 6,
            posting_id = 5,
            is_like = True
        )
        self.token = jwt.encode({'id':6}, SECRET_KEY, ALGORITHM)

    def tearDown(self):
        User.objects.all().delete()
        Space.objects.all().delete()
        Size.objects.all().delete()
        Residence.objects.all().delete()
        Style.objects.all().delete()
        Posting.objects.all().delete()
        Like.objects.all().delete()
    
    def test_posting_like_post_success(self):
        client = Client()
        
        header = {
            'HTTP_Authorization' : self.token,
        }

        body = {
            'posting_id' : 5
        }

        response = client.post('/postings/like', json.dumps(body), content_type='application/json', **header)

        result = {
            'like'       : False, 
            'user_id'    : 6,
            'posting_id' : 5
        }

        self.assertEqual(response.json(), {'result' : result})
        self.assertEqual(response.status_code, 200)

    def test_posting_like_post_key_errer(self):
        client = Client()
        
        header = {
            'HTTP_Authorization' : self.token,
        }

        body = {
            'posting_i' : 5
        }

        response = client.post('/postings/like', json.dumps(body), content_type='appliction/json', **header)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                'message' : 'KEY_ERROR'
            }
        )

    def test_posting_like_get_success(self):
        client = Client()

        header = {
            'HTTP_Authorization' : self.token,
        }

        response = client.get('/postings/like', content_type='application/json', **header)

        result= [{
            'posting_id' : 5,
            'image'      : 'image_url'
            }]

        self.assertEqual(response.json(), {'result' : result})
        self.assertEqual(response.status_code, 200)
