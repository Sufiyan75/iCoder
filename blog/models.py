from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.
class Post(models.Model):
    sno = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, default="")
    content = models.TextField(default="")
    author = models.CharField(max_length=30)
    views = models.IntegerField(default=0)
    likes = models.ManyToManyField(User, related_name='post', blank=True)
    slug = models.CharField(max_length=150)
    image = models.ImageField(upload_to="blog/images", default="")
    timeStamp = models.DateTimeField(blank=True)

    def __str__(self):
        return self.title + " by " + self.author
    

class BlogComment(models.Model):
    sno = models.AutoField(primary_key=True)
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    timeStamp = models.DateTimeField(default=now)

    def __str__(self):
        return self.comment[0:20] + "... by " + self.user.username
    