from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
from PIL import Image


# Tags
class Tag(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

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
    GENDER_CHOICES = (('Male', 'Male'), ('Female', 'Female'), ('Unisex', 'Unisex/Parody'))
    gender = models.CharField(max_length=20, choices = GENDER_CHOICES, null = True)
    # gender = models.CharField(max_length = 20, null = True)
    phone = models.IntegerField(default=0)
    birthday = models.DateField( blank=True, null = True)
    image = models.ImageField(upload_to='media/profile_image', blank=True, default = 'media/profile_image/779d213e8b3d36e45f97e23a9eafb478.png')


    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

class FollowTag(models.Model):
    tag = models.ManyToManyField(Tag, related_name = 'tag_set', null=True)
    current_user = models.ForeignKey(User, related_name = 'owner', null = True,on_delete=models.CASCADE)

    @classmethod
    def subscribe_tag(cls, current_user, new_tag):
        following_tag, created = cls.objects.get_or_create(
            current_user = current_user
        )
        following_tag.tag.add(new_tag)

    @classmethod
    def unsubscribe_tag(cls, current_user, new_tag):
        following_tag, created = cls.objects.get_or_create(
            current_user = current_user
        )
        following_tag.tag.remove(new_tag)

class Friends(models.Model):
    friend = models.ManyToManyField(User, related_name="friend_set")
    current_user = models.ForeignKey(User, related_name='friend_owner', null=True, on_delete=models.CASCADE)

    @classmethod
    def subscribe_friend(cls, current_user, new_friend):
        following_friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        following_friend.friend.add(new_friend)

    @classmethod
    def unsubscribe_friend(cls, current_user, new_friend):
        following_friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        following_friend.friend.remove(new_friend)

class Thread(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    tags = models.ManyToManyField(Tag)

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
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    threadID = models.ForeignKey(Thread, on_delete=models.CASCADE)
    comment_time = models.DateTimeField(
            default=timezone.now)
    parentCommentID = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    text = models.TextField()
    tags = models.ManyToManyField(Tag)


# Comment Tags
class CommentTag(models.Model):
    commentId = models.ForeignKey(Comment, on_delete=models.CASCADE)
    tagId = models.ForeignKey(Tag, on_delete=models.CASCADE)