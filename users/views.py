import requests

import jwt
from datetime import datetime, timedelta

from django.http  import JsonResponse
from django.views import View

from .models     import User
from my_settings import SECRET_KEY, ALGORITHM

class KakaoLoginView(View):
    def get(self, request):
        try:
            kakao_token = request.headers["Authorization"]
            header      = {'Authorization': f'Bearer {kakao_token}'}
            user_info   = requests.get('https://kapi.kakao.com/v2/user/me', headers=header, timeout = 5).json()

            if user_info.get('code') == -401:
                return JsonResponse({'messages' : 'INVALID_TOKEN'}, status=401)

            kakao_id      = user_info['id']
            nickname      = user_info["properties"]['nickname']
            profile_image = user_info["properties"]['profile_image']
            email         = user_info["kakao_account"]['email']
            
            user, is_create = User.objects.get_or_create(
                kakao_id    = kakao_id,
                defaults    = {
                    "nickname"          : nickname,
                    "profile_image_url" : profile_image,
                    "email"             : email
                }
            )

            payload = {
                "id"  : user.id,
                "exp" : datetime.now() + timedelta(days=3),
                "iat" : datetime.now()
            }

            user_information = {
                "nickname"      : user.nickname,
                "profile_image" : user.profile_image_url,
                "email"         : user.email
            }
            access_token = jwt.encode(payload, SECRET_KEY, ALGORITHM)

            return JsonResponse({'token' : access_token, "user_information" : user_information}, status=200)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)