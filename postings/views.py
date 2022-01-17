import json

from django.http      import JsonResponse
from django.views     import View
from django.db.models import Q

from postings.models       import Posting, Comment, Like
from users.models          import User
from utils.login_decorator import login_decorator

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
                'tags'       : posting.tags.split(',') if posting.tags else None,
                'size'       : posting.size.name if posting.size else None,
                'residence'  : posting.residence.name if posting.residence else None,
                'space'      : posting.space.name,
                'style'      : posting.style.name if posting.style else None,
                'hits'       : posting.hits,
                'like_count' : posting.like_set.all().filter(is_like=True).count(),
                'image_urls' : images,
                'user_name'  : user.nickname,
                'user_image' : user.profile_image_url,
            }
            return JsonResponse({'result' : result}, status=200)
        
        except Posting.DoesNotExist:
            return JsonResponse({'message' : 'POSTING_DOESNOT_EXIST'}, status=404)

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