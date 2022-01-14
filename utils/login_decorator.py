import jwt

from django.http import JsonResponse

from ..users.models     import User
from my_settings import SECRET_KEY, ALGORITHM

def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            token        = request.headers["Authorization"] 
            user_id      = jwt.decode(token, SECRET_KEY, ALGORITHM)["id"]
            user         = User.objects.get(id=user_id)
            request.user = user 
            
            return func(self, request, *args, **kwargs)

        except jwt.InvalidTokenError:
            return JsonResponse({"message": "INVALID_TOKEN"}, status = 400)

        except jwt.DecodeError: 
            return JsonResponse({"error_code" : "DECODE_ERROR"}, status = 401)

        except User.DoesNotExist:
            return JsonResponse({"error_code" : "UNKNOWN_USER"}, status = 401)
        
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
    return wrapper
