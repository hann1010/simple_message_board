from mimetypes import init
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=40, blank=True)
    club = models.CharField(max_length=200, blank=True)
    call = models.CharField(max_length=200, blank=True)
    qth = models.CharField(max_length=200, blank=True)
    address = models.CharField(max_length=200, blank=True)
    email_public = models.EmailField(max_length=200, blank=True)
    town = models.CharField(max_length=200, blank=True)
    country = models.CharField(max_length=200, blank=True)
    initial_chat = models.CharField(max_length=200, default='<p></p>')
    beep_sound = models.BooleanField(default=False)
    user_level= models.PositiveIntegerField(default=10)
    list_rows= models.PositiveIntegerField(default=10)
    items_in_page= models.PositiveIntegerField(default=10)
    messages_in_chat_page= models.PositiveIntegerField(default=10)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return  str(self.user) + " / " + self.nickname +" / " \
        + self.address + " / " + self.town + " / " \
        + str(self.user_level)

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()