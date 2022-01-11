from django.urls import path, include

urlpatterns = [
    path('users', include('users.urls')),
<<<<<<< HEAD
<<<<<<< HEAD
    path('postings', include('postings.urls'))
]
=======
    path('/postings', include('postings.urls'))
]
>>>>>>> 14f7127 (User 앱 merge에 따른 리베이스 완료 및 Posting 앱 작업 지속)
=======
    path('postings', include('postings.urls'))
]
>>>>>>> a255457 (포스팅 기능 구현 완료)
