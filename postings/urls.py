from django.urls import path

from .views import PostingDeatilView, PostingLikeView

urlpatterns=[
    path('/<int:posting_id>', PostingDeatilView.as_view()),
    path('/like', PostingLikeView.as_view())
]