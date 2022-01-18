import json

from django.http      import JsonResponse
from django.views     import View
from django.db.models import Q

from postings.models       import Posting, Comment
from users.models          import User
from utils.login_decorator import login_decorator

class PostingListView(View):
    def get(self, request):
        try:
            '''
            목적: DB에 존재하는 posting 정보를 list 형태로 주는 것이 목적
            추가 조건: 
                1. 사이즈, 주거형태, 공간, 스타일에 대해 필터(선택)이 가능해야 한다. 
                2. 페이지넨이션이 가능 해야 한다.
            '''

            '''
            1. 프론트에서 조건에 대한 정보를 받는다.
            2. 조건을 더해준다.(사이즈)
            3. DB에서 원하는 조건에 맞는 Posting 정보를 가져온다.
            4. 가져온 정보를 프론트에게 주기 알맞은 형태로 가공한다.
            5. 프론트에게 보내준다.
            '''
            
            
            #1 프론트에서 조건에 대한 정보를 받는다.
            size_id      = request.GET.get('size_id', None)
            residence_id = request.GET.get('residence_id', None)
            space_id     = request.GET.get('space_id', None)
            style_id     = request.GET.get('style_id', None)
            offset       = int(request.GET.get('offset', 0))
            limit        = int(request.GET.get('limit', 8))

            #2. 조건을 더해준다 => 조건을 만든다(Q())    
            Posting.objects.filter(size__id=size_id)
            
            q = Q()
            
            if size_id:
                q &= Q(size__id=size_id)
                
            if residence_id:
                q &= Q(residence__id = residence_id)
                
            if space_id:
                q &= Q(space__id = space_id)
                
            if style_id:
                q &= Q(style__id = style_id)
            
            
            # 3,4 원하는 조건에 맞는 데이터를 DB에서 가져온 뒤에 가공
            results = [{
                'posting_id' : posting.id,
                'content' : posting.content,
                'like_count' : posting.like_set().filter(is_like=True).count(),
                #좋아요 수, #댓글 수
                'image_url' : posting.image_set.all().first().url,
                'user_name' : posting.user.nickname,
                'user_image' : posting.uers.profile_image_url
            } for posting in Posting.objects.filter(q).distinct().order_by('-created_at')[offset:offset+limit]]
            return JsonResponse({'results' : results}, status = 200)
        
        except KeyError:
            return JsonResponse({'message' : "KEY_ERROR"}, status = 400)

    def post(self, request):
        pass

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
        
class CommentView(View):
    @login_decorator
    def post(self, request, posting_id):
        try:
            data = json.loads(request.body)
            user = request.user
            
            comment = Comment.objects.create(
                content    = data['content'],
                posting_id = posting_id,
                user_id    = user.id
            )
            
            return JsonResponse({'message' : 'created'}, status=201)        
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=401)
        
    def get(self, request, posting_id):
        offset = int(request.GET.get('offset', 0))
        limit  = int(request.GET.get('limit', 5))
        
        posting_comments = [{
            'id'         : comment.id,
            'nickname'   : comment.user.nickname,
            'user_image' : comment.user.profile_image_url,
            'content'    : comment.content
        } for comment in Comment.objects.filter(posting_id=posting_id).order_by('-created_at')[offset:offset+limit]]
        
        return JsonResponse({'result' : posting_comments}, status=200)
        
    @login_decorator
    def delete(self, request, posting_id, comment_id):
        try:
            user_id = request.user.id
            
            comment = Comment.objects.get(id=comment_id, user_id=user_id, posting_id=posting_id)
            comment.delete()
            
            return JsonResponse({'message' : 'SUCCESS_DELETE'}, status=204)
        
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=401)
        except Comment.DoesNotExist:
            return JsonResponse({'message' : 'COMMENT_DOESNOT_EXIST'}, status=404)