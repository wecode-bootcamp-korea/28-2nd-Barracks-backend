import json

from django.http  import JsonResponse
from django.views import View

from postings.models       import Posting
from users.models          import User
from utils.login_decorator import login_decorator

import uuid
import boto3

from postings.models   import Posting, Image, Size, Space, Residence, Style
from barracks.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME

class PostingListView(View):

    s3_client = boto3.client(
        's3',
        aws_access_key_id     = AWS_ACCESS_KEY_ID,
        aws_secret_access_key = AWS_SECRET_ACCESS_KEY
    )

    @login_decorator
    def post(self, request):
        try:
            '''
            목적: DB에 posting 정보를 저장하는 것
            어떤 것을 저장?
                1. 제목, 내용, 필터, 테그, 이미지
            주의 할 점
                1. 이미지를 어디에 저장할 건지 -> s3에 저장을하고, boto3을 이용
                2. 이미지와 포스팅 간의 관계 -> 이미지 : 포스팅 = N : 1
                3. Transaction ->
            '''
            data   = request.POST
            user   = request.user
            images = request.FILES.getlist('files')

            posting = Posting.objects.create(
                user_id      = user.id,
                space_id     = data['space'],
                size_id      = data.get('size', None),
                residence_id = data.get('residence', None),
                style_id     = data.get('style', None),
                title        = data['title'],
                tags         = data.getlist('tags', None),
                content      = data.get('content', None)
            )
            
            for image in images:
                 
                key  = str(uuid.uuid4())

                self.s3_client.upload_fileobj(
                    image,
                    AWS_STORAGE_BUCKET_NAME,
                    key, 
                    ExtraArgs = {
                        "ContentType" : image.content_type
                    }
                )
                image_url = "https://wecode-barracks.s3.ap-northeast-2.amazonaws.com/"+key

                Image.objects.create(
                    posting_id = posting.id,
                    image_url  = image_url
                )
            return JsonResponse({'message':'CREATE_SUCCESS'}, status = 201)

        except Image.DoesNotExist:
            return JsonResponse({'message':'Image required'}, status=400)
 
        except Space.DoesNotExist:
            return JsonResponse({'message':'Space required'}, status=400)
 
        except Size.DoesNotExist:
            return JsonResponse({'message':'Size required'}, status=400)
 
        except Residence.DoesNotExist:
            return JsonResponse({'message':'Residence required'}, status=400)
 
        except Style.DoesNotExist:
            return JsonResponse({'message':'Style required'}, status=400)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)


class PostingDeatilView(View):
    def get(self, request, posting_id):
        try:    
            posting = Posting.objects.get(id = posting_id)
            posting.hits += 1
            posting.save()
            images = [{'image_id' : image.id, 'image_url' : image.image_url}
                      for image in posting.image_set.all()]
            user   = posting.user
        
            result = {
                'posting_id' : posting.id,
                'title'      : posting.title,
                'content'    : posting.content,
                'tags'       : posting.tags.split(','),
                'size'       : posting.size.name,
                'residence'  : posting.residence.name,
                'space'      : posting.space.name,
                'style'      : posting.style.name,
                'hits'       : posting.hits,
                'image_urls' : images,
                'user_name'  : user.nickname,
                'user_image' : user.profile_image_url
            }
        
            return JsonResponse({'result' : result}, status=200)
    
        except Posting.DoesNotExist:
            return JsonResponse({'message' : 'POSTING_DOESNOT_EXIST'}, status=404)

