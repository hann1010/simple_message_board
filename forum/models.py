from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

class Forum_post(models.Model):
    title = models.CharField(max_length=100, blank=False)
    post_type = models.CharField(max_length=100, blank=True)
    origin_post_id= models.IntegerField(default=0)
    content = RichTextField()
    date_posted = models.DateTimeField(default=timezone.now)
    date_last_save = models.DateTimeField(auto_now=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return  self.title + " / " + str(self.author)