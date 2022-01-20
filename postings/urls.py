from django.urls import path

from .views import PostingDeatilView, CommentView, PostingListView, PostingLikeView

urlpatterns=[
    path('/<int:posting_id>', PostingDeatilView.as_view()),
    path('/like', PostingLikeView.as_view()),
    path('/<int:posting_id>', PostingDeatilView.as_view()),
    path('/<int:posting_id>/comments', CommentView.as_view()),
    path('/<int:posting_id>/comments/<int:comment_id>', CommentView.as_view()),
    path('', PostingListView.as_view())
]