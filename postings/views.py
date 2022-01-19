import json

from django.http      import JsonResponse
from django.views     import View
from django.db.models import Q

from postings.models       import Posting, Comment
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