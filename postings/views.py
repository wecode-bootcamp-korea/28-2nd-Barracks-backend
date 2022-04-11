import json

from django.http           import JsonResponse
from django.views          import View
from django.db.models      import Q
from django.db             import transaction

from users.models          import User
from postings.models       import Posting, Image, Size, Space, Residence, Style, Comment, Like

from utils.login_decorator import login_decorator
from core.storages         import s3_client, FileUpload


class PostingListView(View):
    def get(self, request):
        try:
            size_id      = request.GET.get('size_id', None)
            residence_id = request.GET.get('residence_id', None)
            space_id     = request.GET.get('space_id', None)
            style_id     = request.GET.get('style_id', None)
            offset       = int(request.GET.get('offset', 0))
            limit        = int(request.GET.get('limit', 8))

            q = Q()
            
            if size_id:
                q &= Q(size__id = size_id)
                
            if residence_id:
                q &= Q(residence__id = residence_id)
                
            if space_id:
                q &= Q(space__id = space_id)
                
            if style_id:
                q &= Q(style__id = style_id)
            
            results = [{
                'posting_id'    : posting.id,
                'content'       : posting.content,
                'like_count'    : posting.like_set.all().filter(is_like=True).count(),
                'comment_count' : posting.comment_set.all().count(),
                'image_url'     : posting.image_set.all().first().image_url if posting.image_set.all().first() else None,
                'user_name'     : posting.user.nickname,
                'user_image'    : posting.user.profile_image_url
            } for posting in Posting.objects.filter(q).order_by('created_at')[offset:offset+limit]]
            return JsonResponse({'results' : results}, status = 200)
        
        except KeyError:
            return JsonResponse({'message' : "KEY_ERROR"}, status = 400)
    
    @login_decorator
    @transaction.atomic
    def post(self, request):
        try:
            data  = request.POST
            user  = request.user
            files = request.FILES.getlist('files')

            if not files:
                return JsonResponse({'message' : 'IMAGE_REQUIRED'}, status=400)

            posting = Posting.objects.create(
                user_id      = user.id,
                space_id     = data['space'],
                size_id      = data.get('size', None),
                residence_id = data.get('residence', None),
                style_id     = data.get('style', None),
                title        = data.get('title', None),
                tags         = data.getlist('tags', None),
                content      = data.get('content', None),
            )

            for file in files:
                image_url = FileUpload(s3_client).upload(file)
                Image.objects.create(
                    posting_id = posting.id,
                    image_url = image_url
                )
            
            return JsonResponse({'message' : 'CREATE_SUCCESS', 'results' : {"post_id" : posting.id}}, status = 201)

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
                'like_count' : posting.like_set.all().filter(is_like=True).count(),
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
            
            Comment.objects.create(
                content    = data['content'],
                posting_id = posting_id,
                user_id    = request.user.id
            )
            return JsonResponse({'result' : 'created'}, status=201)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=401)
        
    def get(self, request, posting_id):
        offset = int(request.GET.get('offset', 0))
        limit  = int(request.GET.get('limit', 5))
        posting = Posting.objects.get(id = posting_id)
        
        result = {
            'comments_totals' : posting.comment_set.all().count(),
            'comments' : [{
                'id'         : comment.id,
                'nickname'   : comment.user.nickname,
                'user_image' : comment.user.profile_image_url,
                'content'    : comment.content
            } for comment in Comment.objects.filter(posting_id=posting_id).order_by('-created_at')[offset:offset+limit]]
        }
            
        return JsonResponse({'result' : result}, status=200)
    
    @login_decorator
    def delete(self, request, posting_id, comment_id):
        try:
            user_id    = request.user.id
            
            comment = Comment.objects.get(id = comment_id, user_id = user_id, posting_id = posting_id)
            comment.delete()
            
            return JsonResponse({'message' : 'SUCCESS_DELETE'}, status=204)
        
        except Comment.DoesNotExist:
            return JsonResponse({'message' : 'COMMENT_DOESNOT_EXIST'}, status=404)

class PostingLikeView(View):
    @login_decorator
    def post(self,request):
        try:
            data = json.loads(request.body)

            posting_id = data['posting_id']
            user       = request.user

            check_like_post = Like.objects.filter(user_id = user.id, posting_id = posting_id)
            
            if check_like_post.exists():
                like         = Like.objects.get(user_id=user.id, posting_id=posting_id)
                like.is_like = not like.is_like
                like.save()
            else:
                Like.objects.create(
                    user_id    = user.id,
                    posting_id = posting_id,
                    is_like    = True,
                )

            result = {
                'like'       : like.is_like, 
                'user_id'    : user.id, 
                'posting_id' : posting_id
            }

            return JsonResponse({"result" : result}, status=200)
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

    @login_decorator
    def get(self, request):
        user     = request.user
        postings = Posting.objects.filter(like__user_id = user.id, like__is_like = True)

        result = [{
            'posting_id' : posting.id,
            'image'      : posting.image_set.first().image_url
        }for posting in postings]

        return JsonResponse({'result' : result}, status=200)
