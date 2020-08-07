from django.contrib import admin
from .models import UserProfile, Post, Image, Friendship, FriendRequest, Like, PreGalleryUrl

# Register your models here.


class FriendshipInLine(admin.StackedInline):
    model = Friendship
    fk_name = "from_user"


class UserProfileAdmin(admin.ModelAdmin):
    inlines = [FriendshipInLine]


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Post)
admin.site.register(Image)
admin.site.register(FriendRequest)
admin.site.register(Friendship)
admin.site.register(Like)
admin.site.register(PreGalleryUrl)