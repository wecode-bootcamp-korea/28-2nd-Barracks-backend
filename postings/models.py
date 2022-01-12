from django.db   import models
from core.models import TimeStampModel

class Posting(TimeStampModel):
    user      = models.ForeignKey('users.User', on_delete=models.CASCADE)
    title     = models.CharField(max_length=100, null=True)
    tags      = models.CharField(max_length=300, null=True)
    content   = models.TextField(max_length=1500, null=True)
    hits      = models.IntegerField(default=0)
    size      = models.ForeignKey('postings.Size', on_delete=models.SET_NULL, null=True)
    residence = models.ForeignKey('postings.Residence', on_delete=models.SET_NULL, null=True)
    space     = models.ForeignKey('postings.Space', on_delete=models.CASCADE)
    style     = models.ForeignKey('postings.Style', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'postings'

    def __str__(self):
        return self.title

class Like(models.Model):
    user    = models.ForeignKey('users.User', on_delete=models.CASCADE)
    posting = models.ForeignKey('postings.Posting', on_delete=models.CASCADE)
    is_like = models.BooleanField(null=False)

    class Meta:
        db_table = 'likes'

class Comment(TimeStampModel):
    user    = models.ForeignKey('users.User', on_delete=models.CASCADE)
    posting = models.ForeignKey('postings.Posting', on_delete=models.CASCADE)
    content = models.CharField(max_length=350)

    class Meta:
        db_table = 'comments'

class Image(models.Model):
    posting   = models.ForeignKey('postings.Posting', on_delete=models.CASCADE)
    image_url = models.URLField(max_length=2000)

    class Meta:
        db_table = 'images'

class Size(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'sizes'

class Residence(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'residences'

class Space(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'spaces'

class Style(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'styles'