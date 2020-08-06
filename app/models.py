from django.db import models
from homepage.models import MyUser


def user_directory_path(instance, filename):
    return f"users/{instance.user.id}/profile_images/{filename}"


class UserProfile(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, primary_key=True)
    profile_picture = models.ImageField(upload_to=user_directory_path, default="default_profile_pic.jpg")
    city = models.CharField(max_length=40, blank=True)
    country = models.CharField(max_length=30, blank=True)
    nickname = models.CharField(max_length=24, blank=True)
    friends = models.ManyToManyField('self', through='Friendship', symmetrical=False, related_name='related_to+')

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    def add_friend(self, friend, symm=True):
        friendship = Friendship.objects.get_or_create(from_user=self, to_user=friend)
        if symm:
            friend.add_friend(self, False)
        return friendship

    def remove_friend(self, friend, symm=True):
        Friendship.objects.filter(from_user=self, to_user=friend).delete()
        if symm:
            friend.remove_friend(self, False)

    def get_friends(self):
        return self.friends.filter(to_user__from_user=self)


# https://charlesleifer.com/blog/self-referencing-many-many-through/
class Friendship(models.Model):
    from_user = models.ForeignKey(UserProfile, related_name='from_user', on_delete=models.CASCADE)
    to_user = models.ForeignKey(UserProfile, related_name='to_user', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.from_user} - {self.to_user}"


class FriendRequest(models.Model):
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='friendrequest_sender')
    receiver = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='friendrequest_receiver')

    def accept(self):
        new_friendship = self.sender.add_friend(friend=self.receiver)
        self.delete()
        return new_friendship

    def __str__(self):
        return f'{self.sender} -----> {self.receiver}'


class Post(models.Model):
    published = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.published.day}-{self.published.month}-{self.published.day}  ' \
               f'{self.published.hour}:{self.published.minute} by {self.user_profile}'

    def comments_tree(self):
        comments = self.postcomment_set.all()


def image_directory_path(instance, filename):
    return f"images/{instance.post.user_profile.user.id}/{filename}"


class Image(models.Model):
    image = models.ImageField(upload_to=image_directory_path, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.id}'


class PostComment(models.Model):
    published = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    reply_to = models.ManyToManyField('self', related_name='reply', blank=True)
    text = models.TextField()
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.published.day}-{self.published.month}-{self.published.day}  ' \
               f'{self.published.hour}:{self.published.minute} by {self.user_profile}'