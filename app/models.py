from django.db import models
from homepage.models import MyUser


def profile_image_directory_path(instance, filename):
    return f"images/{instance.user.id}/profile_image/{filename}"


class UserProfile(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, primary_key=True)
    profile_picture = models.ImageField(upload_to=profile_image_directory_path, default="default_profile_pic.jpg")
    city = models.CharField(max_length=40, blank=True)
    country = models.CharField(max_length=30, blank=True)
    nickname = models.CharField(max_length=24, blank=True)
    friends = models.ManyToManyField('self', through='Friendship', symmetrical=False, related_name='related_to+')

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    def add_friend(self, friend, symm=True):
        if friend != self:
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

    def friend_status_with(self, user_profile):
        status = 'unknown'
        if Friendship.objects.filter(from_user=self, to_user=user_profile):
            status = 'friend'
        if FriendRequest.objects.filter(sender=self, receiver=user_profile):
            status = 'sended request'
        if FriendRequest.objects.filter(sender=user_profile, receiver=self):
            status = 'received request'
        if user_profile == self:
            status = "self"

        return status


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
        return f'{self.published.day}-{self.published.month}-{self.published.year}  ' \
               f'{self.published.hour}:{self.published.minute} by {self.user_profile}'

    def like(self, user):
        if len(self.image_set.all()) == 1:
            Like.objects.create(target_image=self.image_set.all()[0], user_profile=user, target_post=self)
        else:
            Like.objects.create(target_post=self, user_profile=user)

    def unlike(self, user):
        if len(self.image_set.all()) == 1:
            Like.objects.get(target_image=self.image_set.all()[0], user_profile=user, target_post=self).delete()
        else:
            Like.objects.get(target_post=self, user_profile=user).delete()

    @property
    def likes(self):
        return len(Like.objects.filter(target_post=self))


def image_directory_path(instance, filename):
    if instance.post:
        return f"images/{instance.post.user_profile.user.id}/{filename}"
    else:
        return f"images/{instance.profile.user.id}/profile_images/{filename}"


class Image(models.Model):
    image = models.ImageField(upload_to=image_directory_path)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True)
    published = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.id}'

    def like(self, user):
        if self.profile:
            Like.objects.create(target_image=self, user_profile=user)
        elif len(self.post.image_set.all()) == 1:
            Like.objects.create(target_image=self, user_profile=user, target_post=self.post)
        else:
            Like.objects.create(target_image=self, user_profile=user)

    def unlike(self, user):
        if self.profile:
            Like.objects.get(target_image=self, user_profile=user).delete()
        elif len(self.post.image_set.all()) == 1:
            Like.objects.get(target_image=self, user_profile=user, target_post=self.post).delete()
        else:
            Like.objects.get(target_image=self, user_profile=user).delete()

    @property
    def likes(self):
        return len(Like.objects.filter(target_image=self))


class Comment(models.Model):
    published = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True)
    image = models.ForeignKey(Image, on_delete=models.CASCADE, blank=True, null=True)
    text = models.TextField()
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.published.day}-{self.published.month}-{self.published.day}  ' \
               f'{self.published.hour}:{self.published.minute} by {self.author}'


class Like(models.Model):
    published = models.DateTimeField(auto_now_add=True)
    target_image = models.ForeignKey(Image, on_delete=models.CASCADE, blank=True, null=True)
    target_post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True)
    target_comment = models.ForeignKey(Comment, on_delete=models.CASCADE, blank=True, null=True)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    @property
    def target(self):
        if self.target_image is not None:
            return self.target_image
        if self.target_comment is not None:
            return self.target_comment
        if self.target_post is not None:
            return self.target_post

    def __str__(self):
        return f'{self.user_profile} ---> {self.target}'


class PreGalleryUrl(models.Model):
    url = models.URLField()
    scrollY = models.IntegerField(default=0)
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, primary_key=True)
