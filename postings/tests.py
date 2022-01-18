import json, jwt

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

class CommentTest(TestCase):
    def setUp(self):
        User.objects.create(
            id                = 1,
            kakao_id          = 11,
            email             = 'test1@test1.com',
            nickname          = 'test1',
            profile_image_url = 'test.jpg'
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
        
        Image.objects.create(
            id         = 1,
            posting_id = 1,
            image_url  = 'url1'
        )        
        
        Comment.objects.create(
            id         = 1,
            content    = 'test1 for comment',
            user_id    = 1,
            posting_id = 1
        )
        
        self.token = jwt.encode({'user' : 1}, SECRET_KEY, ALGORITHM)
    
    def tearDown(self):
        User.objects.all().delete()
        Space.objects.all().delete()
        Style.objects.all().delete()
        Residence.objects.all().delete()
        Size.objects.all().delete()
        Posting.objects.all().delete()
        Image.objects.all().delete()
        Comment.objects.all().delete()
        
    def test_comment_post_success(self):
        client = Client()
        header = {'HTTP_Authorization' : self.token}
        
        comment = {
            'posting_id' : 1,
            'user_id' : 1,
            'content' : 'test1 for comment',
        }
        
        posting_comments = [{
            'id' : 1,
            'nickname' : 'test1',
            'user_image' : 'test.jpg',
            'content' : 'test1 for comment'
        }]
        
        response = client.post('/postings/comments/1', json.dump(comment), **header, content_type='application/json')
        self.assertEqual(response.json(), {'message' : posting_comments})
        self.assertEqual(response.status_code, 200)

    def test_comment_post_key_error(self):
        client = Client()
        header = {'HTTP_Authorization' : self.token}
        
        comment = {}
        
        response = client.post('/postings/comments/1', json.dump(comment), **header, content_type='application/json')
        self.assertEqual(response.json(), {'message' : 'KEY_ERROR'})
        self.assertEqual(response.status_code, 401)
        
    def test_comment_get_success(self):
        client = Client()
        response = client.get('/postings/comments/1')
        
        posting_comments = [
            {
                'id' : 1,
                'nickname' : 'test1',
                'user_image' : 'test.jpg',
                'content' : 'fest1 for comment'
            }
        ]
        
        self.assertEqual(response.json(), {'result' : posting_comments})
        self.assertEqual(response.status_code, 200)
        
    def test_comment_delete_success(self):
        client = Client()
        