from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid


# Tags
class Tag(models.Model):
    name = models.CharField(max_length=20)


# files
class File(models.Model):
    name = models.CharField(
        max_length=150,
        null=True,
        blank=True
    )
    filePath = models.CharField(max_length=4096)


# User Profile
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20, blank=True)
    last_name = models.CharField(max_length=20, blank=True)
    username = models.CharField(max_length=20, blank=True)
    #avatar = models.OneToOneField(File, null=True, blank=True, on_delete=models.SET_NULL)
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


class Thread(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)

    def __str__(self):
        return self.title

    def snippet(self):
        return self.text[:50] + '...'


# Thread Files
class ThreadFile(models.Model):
    threadId = models.ForeignKey(Thread, on_delete=models.CASCADE)
    fileId = models.ForeignKey(File, on_delete=models.CASCADE)


# Thread Tags
class ThreadTag(models.Model):
    threadId = models.ForeignKey(Thread, on_delete=models.CASCADE)
    tagId = models.ForeignKey(Tag, on_delete=models.CASCADE)


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    threadID = models.ForeignKey(Thread, on_delete=models.CASCADE)
    comment_time = models.DateTimeField(
            default=timezone.now)
    parentCommentID = models.OneToOneField('self', null=True, blank=True, on_delete=models.SET_NULL)
    text = models.TextField()


# Comment Files
class CommentFile(models.Model):
    commentId = models.ForeignKey(Comment, on_delete=models.CASCADE)
    fileId = models.ForeignKey(File, on_delete=models.CASCADE)


# Comment Tags
class CommentTag(models.Model):
    commentId = models.ForeignKey(Comment, on_delete=models.CASCADE)
    tagId = models.ForeignKey(Tag, on_delete=models.CASCADE)