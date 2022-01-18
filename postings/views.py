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
            size_id = request.GET.get('size_id', None)
            residence_id = request.GET.get('residence_id', None)
            space_id = request.GET.get('space_id', None)
            style_id = request.GET.get('style_id', None)
            # GET이라는 요청(request)이 들어오면 get 해라 키가 'size_id'인 것을!!
            
            offset = int(request.GET.get('offset', 0))
            limit  = int(request.GET.get('limit', 8))
                
            q = Q()
            
            if size_id:
                q &= Q(size_id__name = size_id)
                
            if residence_id:
                q &= Q(residence_id__name = residence_id)
                
            if space_id:
                q &= Q(space_id__name = space_id)
                
            if style_id:
                q &= Q(style_id__name = style_id)
            
            results = [{
                'posting_id' : posting.id,
                'content' : posting.content,
                #좋아요 수, #댓글 수
                'image_url' : posting.image_set.all().first().url,
                'user_name' : #posting에 연결된 유저의 정보
                'user_image' : 
            } for posting in Posting.objects.filter(q).distinct().order_by('-created_at')[offset:offset+limit]]
            return JsonResponse({'results' : results}, status = 200)
        
        except KeyError:
            return JsonResponse({'message' : "KEY_ERROR"}, status = 400)
      


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
            data    = json.loads(request.body)
            user_id = request.user.id
            
            offset = int(request.GET.get('offset', 0))
            limit  = int(request.GET.get('limit', 5))
            
            Comment.objects.create(
                content    = data['content'],
                posting_id = posting_id,
                user_id    = user_id
            )
            
            posting_comments = [{
                'id'         : comment.id,
                'nickname'   : comment.user.nickname,
                'user_image' : comment.user.profile_image_url,
                'content'    : comment.content
            } for comment in Comment.objects.filter(posting_id=posting_id).order_by('-created_at')[offset:offset+limit]]
            
            return JsonResponse({'result' : posting_comments}, status=200)
        
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=401)
        
    def get(self, request, posting_id):
        try:
            offset = int(request.GET.get('offset', 0))
            limit  = int(request.GET.get('limit', 5))
            
            posting_comments = [{
                'id'         : comment.id,
                'nickname'   : comment.user.nickname,
                'user_image' : comment.user.profile_image_url,
                'content'    : comment.content
            } for comment in Comment.objects.filter(posting_id=posting_id).order_by('-created_at')[offset:offset+limit]]
            
            return JsonResponse({'result' : posting_comments}, status=200)
        
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=401)
        
    @login_decorator
    def delete(self, request, posting_id, comment_id):
        try:
            data       = json.loads(request.body)
            user_id    = request.user.id
            comment_id = data['comment_id']
            
            comment = Comment.objects.get(id = comment_id, user_id = user_id)
            comment.delete()
            
            return JsonResponse({'message' : 'SUCCESS_DELETE'}, status=204)
        
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=401)
        except Comment.DoesNotExist:
            return JsonResponse({'message' : 'COMMENT_DOESNOT_EXIST'}, status=404)