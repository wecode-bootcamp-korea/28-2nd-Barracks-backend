from django.db                       import models
from django.db.models.fields         import BooleanField
from django.db.models.fields.related import ForeignKey

from core.models                     import TimeStampModel

class Posting(TimeStampModel):
    user      = ForeignKey('users.User', on_delete=models.CASCADE)
    name      = models.CharField(max_name=50)
    tags      = models.CharField(max_length=200)
    content   = models.TextField(max_length=1500)
    hits      = models.IntegerField(default=0)
    size      = models.ForeignKey('.Size', on_delete=models.SET_NULL, null=True)
    residence = models.ForeignKey('.Residence', on_delete=models.SET_NULL, null=True)
    space     = models.ForeignKey('.Space', on_delete=models.CASCADE)
    style     = models.ForeignKey('.Style', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'postings'

    def __str__(self):
        return self.name

class Like(models.Model):
    user    = ForeignKey('users.User', on_delete=models.CASCADE)
    posting = ForeignKey('.Posting', on_delete=models.CASCADE)
    is_like = BooleanField(null=False)

    class Meta:
        db_table = 'likes'

class Comment(TimeStampModel):
    user    = ForeignKey('users.User', on_delete=models.CASCADE)
    posting = ForeignKey('.Posting', on_delete=models.CASCADE)
    content = models.CharField(max_length=350)

    class Meta:
        db_table = 'comments'

class Image(models.Model):
    posting   = ForeignKey('.Posting', on_delete=models.CASCADE)
    image_url = models.URLField()

    class Meta:
        db_table = 'images'

class Size(models.Model):
    name = models.CharField(max_length=50)

class Residence(models.Model):
    name = models.CharField(max_length=50)

class Space(models.Model):
    name = models.CharField(max_length=50)

class Style(models.Model):
    name = models.CharField(max_length=50)