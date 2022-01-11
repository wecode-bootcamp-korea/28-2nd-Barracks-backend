from django.urls import path

from .views import PostingView, PostingDeatilView, CommentView

app_name = "postings"

urlpatterns=[
    path('', PostingView.as_view()),
    path('/<int:posting_id>', PostingDeatilView.as_view()),
    path('/<int:posting_id>/comments', CommentView.as_view()),
    path('/<int:posting_id>/comments/<int:comment_id>', CommentView.as_view())
]
