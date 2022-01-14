from django.urls import path

from .views import KakaoLoginView

urlpatterns = [
    path('/login', KakaoLoginView.as_view())
]