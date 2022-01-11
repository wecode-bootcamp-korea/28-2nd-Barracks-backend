from django.db   import models

from core.models import TimeStampModel

class User(TimeStampModel):
    kakao_id          = models.IntegerField(unique=True)
    email             = models.CharField(null=True)
    nickname          = models.CharField(max_length=50)
    profile_image_url = models.URLField()

    class Meta:
        db_table = 'users'

    def __self__(self):
        return self.nickname