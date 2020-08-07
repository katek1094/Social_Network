from django.shortcuts import render, redirect
from django.http import JsonResponse
from homepage.models import MyUser
from . models import UserProfile, Post, Image, FriendRequest, Friendship, Like, PreGalleryUrl
from .forms import BestForm

from .functions import search_for_users

# Create your views here.


def post_list_context(posts, auth_user_profile):
    posts_with_context = []
    for p in posts:
        published = f"{p.published.day}-{p.published.month}-{p.published.year} at {p.published.hour}:{p.published.minute}"
        profile = UserProfile.objects.get(user=p.user_profile)
        data = {'post': p,
                'images': Image.objects.filter(post=p),
                "profile": profile,
                'published': published,
                'like': Like.objects.filter(target_post=p, user_profile=auth_user_profile),
                'likes': p.likes,
                'image_quantity': len(Image.objects.filter(post=p))}
        posts_with_context.append(data)
    return posts_with_context


def welcome_page(request):
    if request.user.is_authenticated:
        # profile_user = UserProfile.objects.get(user=request.user)
        # return render(request, 'app/wall.html', context={"profile_user": profile_user})
        return redirect("wall")
    else:
        return redirect('login')


def profile_page(request, id):
    # statuses: "friend, sended_request, received_request, unknown, auth
    status = "unknown"
    auth_user_profile = UserProfile.objects.get(user=request.user)
    visited_user = MyUser.objects.get(id=id)
    visited_profile = UserProfile.objects.get(user=visited_user)
    are_friends = Friendship.objects.filter(from_user=auth_user_profile, to_user=visited_profile)
    if are_friends:
        status = 'friend'
    sended_request = FriendRequest.objects.filter(sender=auth_user_profile, receiver=visited_profile)
    if sended_request:
        status = 'sended_request'
    received_request = FriendRequest.objects.filter(sender=visited_profile, receiver=auth_user_profile)
    if received_request:
        status = 'received_request'
    if visited_profile == auth_user_profile:
        status = "auth"

    if request.method == 'POST':
        if status == "unknown":
            FriendRequest.objects.create(sender=auth_user_profile, receiver=visited_profile)
            status = 'sended_request'
        elif status == "sended_request":
            FriendRequest.objects.get(sender=auth_user_profile, receiver=visited_profile).delete()
            status = 'unknown'
        elif status == "received_request":
            FriendRequest.objects.get(sender=visited_profile, receiver=auth_user_profile).accept()
            status = 'friend'
        elif status == "friend":
            auth_user_profile.remove_friend(friend=visited_profile)
            status = 'unknown'

    user = MyUser.objects.get(id=id)
    profile_user = UserProfile.objects.get(user=user)
    user_posts = profile_user.post_set.all().order_by('-published')
    profile_posts = post_list_context(user_posts, auth_user_profile)

    return render(request, 'app/profile_page.html',
                  context={'profile_user': profile_user, 'profile_posts': profile_posts,
                           'status': status})


def settings(request):

    return render(request, 'app/settings.html')


def wall(request):
    auth_user_profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = BestForm(request.POST, request.FILES)
        if form.is_valid():
            images = (request.FILES.getlist('image'))
            if request.FILES.getlist('image') == [] and request.POST['text'] == '':
                pass
            else:
                post = Post.objects.create(user_profile=auth_user_profile, text=request.POST['text'])
                for image in images:
                    Image.objects.create(image=image, post=post)
                return redirect('wall')
    else:
        form = BestForm()

    all_posts = Post.objects.all()
    friends = auth_user_profile.get_friends()
    posts = Post.objects.none()
    for friend in friends:
        posts = posts.union(all_posts.filter(user_profile=friend))
    posts = posts.union(all_posts.filter(user_profile=auth_user_profile))
    posts = posts.order_by('-published')
    wall_posts = post_list_context(posts, auth_user_profile)

    return render(request, 'app/wall.html',
                  {'form': form, 'wall_posts': wall_posts})


def search(request):
    phrase = request.GET['search']
    users = []
    profiles = UserProfile.objects.all()
    for profile in profiles:
        users.append({"id": profile.user.id,
                      "first_name": profile.user.first_name,
                      "last_name": profile.user.last_name})
    results_ids = search_for_users(users, phrase)
    results_profiles = []
    for r in results_ids:
        user = MyUser.objects.get(id=r)
        results_profiles.append(UserProfile.objects.get(user=user))

    return render(request, 'app/search.html',
                  {"results_profiles": results_profiles, "phrase": phrase})


def friend_requests(request):
    auth_user_profile = UserProfile.objects.get(user=request.user)
    if request.method == "POST":
        sender = request.POST['sender']
        fr = FriendRequest.objects.get(receiver=auth_user_profile, sender=sender)
        fr.accept()

    auth_user_profile = UserProfile.objects.get(user=request.user)
    friend_requests = FriendRequest.objects.filter(receiver=auth_user_profile)

    return render(request, 'app/friend_requests.html', {'friend_requests': friend_requests})


def like(request):
    post_id = request.POST['post_id']
    post = Post.objects.get(id=post_id)
    auth_user_profile = UserProfile.objects.get(user=request.user)
    action = request.POST['action']
    if action == 'like':
        post.like(auth_user_profile)
    if action == 'unlike':
        post.unlike(auth_user_profile)

    return JsonResponse({'success': True})


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
        auth_user_id = request.GET['auth_user_id']
        auth_user_profile = UserProfile.objects.get(user=auth_user_id)
        model_instance = PreGalleryUrl.objects.get(user_profile=auth_user_profile)
        exit_url = model_instance.url
        model_instance.delete()

        return JsonResponse({'success': True, 'url': exit_url, 'scrollY': model_instance.scrollY})


def gallery(request, post_id, image_id):
    post = Post.objects.get(id=post_id)
    image = Image.objects.get(id=image_id)
    images = Image.objects.filter(post=post)
    image_list = list(images.values_list('id', flat=True))
    author = post.user_profile
    current_image = image_list.index(image_id)

    if current_image != 0:
        left_image_id = image_list[current_image - 1]
        left_image = images.get(id=left_image_id)
    else:
        left_image = None
    if current_image != len(image_list) - 1:
        right_image_id = image_list[current_image + 1]
        right_image = images.get(id=right_image_id)
    else:
        right_image = None

    return render(request, 'app/gallery.html', {'post': post, 'author': author, 'image': image,
                                                'right_image': right_image, 'left_image': left_image})
