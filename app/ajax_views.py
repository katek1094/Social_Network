from django.shortcuts import render, redirect
from django.http import JsonResponse
from homepage.models import MyUser
from . models import UserProfile, Post, Image, FriendRequest, Friendship, Like, PreGalleryUrl, Comment
from .forms import BestForm, NewProfilePictureUploadForm
from .functions import search_for_users, change_profile_picture, new_comment_html
from urllib import parse
import re


def pre_gallery_url(request):
    if request.method == "POST":
        auth_user_id = request.POST['auth_user_id']
        auth_user_profile = UserProfile.objects.get(user=auth_user_id)
        previous_url = request.POST['previous_url']
        scrollY = request.POST['scrollY']
        old_instance = PreGalleryUrl.objects.filter(user_profile=auth_user_profile)
        if old_instance:
            old_instance.delete()
        PreGalleryUrl.objects.create(user_profile=auth_user_profile, url=previous_url, scrollY=scrollY)

        return JsonResponse({'success': True})

    if request.method == 'GET':
        auth_user_id = request.GET.get('auth_user_id')
        auth_user_profile = UserProfile.objects.get(user=auth_user_id)
        model_instance = PreGalleryUrl.objects.get(user_profile=auth_user_profile)
        exit_url = model_instance.url
        index = exit_url.find('?scrollY')
        if index:
            exit_url = exit_url[:index]
        scrollY = model_instance.scrollY
        model_instance.delete()
        context = {'scrollY': scrollY}
        final = exit_url + '?' + parse.urlencode(context)

        return JsonResponse({'success': True, 'url': final})


def comment(request):
    auth_user_profile = UserProfile.objects.get(user=request.user)
    target_type = request.POST['type']
    target_id = request.POST['id']
    text = request.POST.get('text')
    final_new_comment_html = new_comment_html(auth_user_profile, request, text, target_id)
    if text != '':
        if target_type == 'post':
            post = Post.objects.get(id=target_id)
            Comment.objects.create(post=post, text=text, author=auth_user_profile)
            return JsonResponse({'success': True, 'new_comment_html': final_new_comment_html})
        elif target_type == 'image':
            image = Image.objects.get(id=target_id)
            Comment.objects.create(image=image, text=text, author=auth_user_profile)
            return JsonResponse({'success': True, 'new_comment_html': final_new_comment_html})


def like(request):
    target_type = request.POST['target_type']
    target_id = request.POST['target_id']
    target_models = {'post': Post, 'image': Image, 'comment': Comment}
    model = target_models[target_type]
    target = model.objects.get(id=target_id)
    auth_user_profile = UserProfile.objects.get(user=request.user)
    action = request.POST['action']
    if action == 'like':
        target.like(auth_user_profile)
    if action == 'unlike':
        target.unlike(auth_user_profile)

    return JsonResponse({'success': True})


def friendship_button(request):
    auth_profile_user_id = request.POST.get('auth_profile_user_id')
    action = request.POST.get('action')
    visited_profile_user_id = request.POST.get('visited_profile_user_id')
    auth_profile = UserProfile.objects.get(user=auth_profile_user_id)
    visited_profile = UserProfile.objects.get(user=visited_profile_user_id)
    if action == 'send friend request':
        FriendRequest.objects.create(sender=auth_profile, receiver=visited_profile)
    if action == 'unfriend':
        auth_profile.remove_friend(friend=visited_profile)
    if action == 'cancel friend request':
        FriendRequest.objects.get(sender=auth_profile, receiver=visited_profile).delete()
    if action == 'accept friend request':
        FriendRequest.objects.get(sender=visited_profile, receiver=auth_profile).accept()
    status = auth_profile.friend_status_with(visited_profile)
    friendship_status_actions = {'unknown': 'send friend request', 'friend': 'unfriend',
                                 'sended request': 'cancel friend request',
                                 'received request': 'accept friend request', 'self': 'self'}

    return JsonResponse({'success': True, 'new_action': friendship_status_actions[status]})


def delete(request, type, id):
    target_models = {'post': Post, 'image': Image, 'comment': Comment}
    model = target_models[type]
    target = model.objects.get(id=id)
    target.delete()

    return JsonResponse({'success': True})
