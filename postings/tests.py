import json
import jwt
from unittest.mock import patch, MagicMock

from django.test                    import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile

from postings.models import Posting, Space, Size, Residence, Style, Image, Comment, Like
from users.models    import User
from my_settings     import SECRET_KEY, ALGORITHM

class PostingViewTest(TestCase):
    def setUp(self):
        User.objects.create(
            id       = 1,
            kakao_id = 1135,
            email    = 'email@email.com',
            nickname = 'asdf',
            profile_image_url = 'asdfasdfasdf'
        )

        Space.objects.create(id=1, name='거실')
        Size.objects.create(id=1, name='10평')
        Residence.objects.create(id=1, name='아파트')
        Style.objects.create(id=1, name='심플')


    def tearDown(self):
        User.objects.all().delete()
        Posting.objects.all().delete()
        Space.objects.all().delete()
        Size.objects.all().delete()
        Residence.objects.all().delete()
        Style.objects.all().delete()
    
    
    @patch('core.storages.FileUpload')
    def test_s3_upload_image_success(self, mocked_client):
        client = Client()
        token = jwt.encode({"id" : 1}, SECRET_KEY, ALGORITHM)
        
        class MockedResponse():
            def upload(self, file):
                return 'https://wecode-barracks.s3.ap-northeast-2.amazonaws.com/033f6f97-0f08-4b6f-a3a4-296a50292f72'
        
        files = SimpleUploadedFile(
            name         = 'test.jpg',
            content      = b'file_content',
            content_type = 'image/jpg'
        )

        mocked_client.return_value = MockedResponse()
        headers = {'HTTP_Authorization': token, 'content-type' : 'multipart/form-data'}
        body = {'files'     : files,
                'space'     : 1,
                'size'      : 1,
                'residence' : 1,
                'style'     : 1,
                'title'     : 'some title for testing',
                'tags'      : ['tag1', 'tag2', 'tag3'],
                'content'   : '무야호~'
                }
        response = client.post('/postings', body, **headers)
        
        posting = Posting.objects.last()
        self.assertEqual(response.json(), {'message' : 'CREATE_SUCCESS', 'results' : {'post_id' : posting.id}})
        self.assertEqual(response.status_code, 201)

    @patch('core.storages.FileUpload')
    def test_s3_upload_image_excluded_error(self, mocked_client):
        client = Client()
        token = jwt.encode({"id" : 1}, SECRET_KEY, ALGORITHM)

        class MockedResponse():
            def upload(self, files):
                return None

        files = SimpleUploadedFile(
            name = 'test.jpg',
            content = b'file_content',
            content_type = 'image/jpg'
        )

        mocked_client.return_value = MockedResponse()
        headers = {'HTTP_Authorization': token, 'content-type' : 'multipart/form-data'}
        body = {
                'space'     : 1,
                'size'      : 1,
                'residence' : 1,
                'style'     : 1,
                'title'     : 'some title for testing',
                'tags'      : ['tag1', 'tag2', 'tag3'],
                'content'   : '무야호~'
        }
        response = client.post('/postings', body, **headers)

        self.assertEqual(response.json(), {'message' : 'IMAGE_REQUIRED'})
        self.assertEqual(response.status_code, 400)

    @patch('core.storages.FileUpload')
    def test_s3_upload_image_key_error(self, mocked_client):
        client = Client()
        token = jwt.encode({"id" : 1}, SECRET_KEY, ALGORITHM)

        class MockedResponse():
            def upload(self, files):
                return None

        files = SimpleUploadedFile(
            name         = 'test.jpg',
            content      = b'file_content',
            content_type = 'image/jpg'
            )


        mocked_client.return_value = MockedResponse()
        headers = {'HTTP_Authorization': token, 'content-type' : 'multipart/form-data'}
        body = {'files' : files}
        response = client.post('/postings', body, **headers)

        self.assertEqual(response.json(), {'message' : 'KEY_ERROR'})
        self.assertEqual(response.status_code, 400)

class PostingDetailTest(TestCase):
    def setUp(self):
        self.client = Client()
        
        User.objects.create(
            id                = 1,
            kakao_id          = 123,
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
            'like_count' : 0,
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
        self.token = jwt.encode({'id' : 1}, SECRET_KEY, ALGORITHM)
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
            image_url  = 'url1.jpg'
        )        
        
        Comment.objects.create(
            id         = 1,
            content    = 'test1',
            user_id    = 1,
            posting_id = 1
        )
        
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
        
        result = {
            'id' : 1,
            'user_id' : 1,
            'posting_id' : 1,
            'content' : 'test1'
        }
        
        response = client.post('/postings/1/comments',json.dumps(result), **header, content_type='application/json')
        self.assertEqual(response.json(), {'result' : 'created'})
        self.assertEqual(response.status_code, 201)

    def test_review_view_test_post_key_error(self):
        client  = Client()
        headers = {'HTTP_Authorization' : self.token}

        result = {
            'failure' : 111111,
            'error'   : 11111
        }
    
        response = client.post('/postings/1/comments', json.dumps(result), content_type='application/json', **headers)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {'message' : 'KEY_ERROR'})
    
    def test_comment_get_success(self):
        client = Client()
        response = client.get('/postings/1/comments')
        
        result = {
            'comments_totals' : 1,
            'comments' : [{
                'id'         : 1,
                'nickname'   : 'test1',
                'user_image' : 'test.jpg',
                'content'    : 'test1'
        }]}

        self.assertEqual(response.json(),{'result': result})
        self.assertEqual(response.status_code, 200)
        
    def test_comment_delete_success(self): 
        client = Client()
        header = {'HTTP_Authorization' : self.token}
                
        response = client.delete("/postings/1/comments/1", **header)
        
        self.assertEqual(response.status_code, 204)        
        
    def test_comment_delete_doesnotexist(self): 
        client = Client()
        header = {"HTTP_Authorization" : self.token}

        response = client.delete('/postings/1/comments/500',**header)
       
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
        
class PostingListTest(TestCase):
    def setUp(self):        
        User.objects.create(
            id                = 1,
            kakao_id          = 123,
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
        Image.objects.all().delete()
    
    def test_success_posting_list_view(self):
        client = Client()
        response = client.get('/postings')
        
        results = [{
            'posting_id'    : 1,
            'content'       : 'posting 1 desc',
            'like_count'    : 0,
            'comment_count' : 1,
            'image_url'     : 'url1',
            'user_name'     : 'kk',
            'user_image'    : 'aaa.jpg'
            }]     
        self.assertEqual(response.json(), {'results' : results})
        self.assertEqual(response.status_code, 200)