from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from users.models import Profile
from ckeditor.fields import RichTextField

class Chat_post(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=100, blank=True)
    origin_post_id= models.IntegerField(default=0)
    content = RichTextField(config_name='chat_config')
    date_posted = models.DateTimeField(default=timezone.now)
    date_last_save = models.DateTimeField(auto_now=timezone.now)
    author_name = models.CharField(max_length=100, blank=True)
    author_nickname = models.CharField(max_length=100, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return  self.post_type + " / " + str(self.author)
