from django.shortcuts import render, redirect
from homepage.models import MyUser
from . models import UserProfile, Post, Image, FriendRequest, Friendship
from .forms import BestForm

from .functions import search_for_users

# Create your views here.


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
    auth_profile = UserProfile.objects.get(user=request.user)
    visited_user = MyUser.objects.get(id=id)
    visited_profile = UserProfile.objects.get(user=visited_user)
    are_friends = Friendship.objects.filter(from_user=auth_profile, to_user=visited_profile)
    if are_friends:
        status = 'friend'
    sended_request = FriendRequest.objects.filter(sender=auth_profile, receiver=visited_profile)
    if sended_request:
        status = 'sended_request'
    received_request = FriendRequest.objects.filter(sender=visited_profile, receiver=auth_profile)
    if received_request:
        status = 'received_request'
    if visited_profile == auth_profile:
        status = "auth"

    if request.method == 'POST':
        if status == "unknown":
            FriendRequest.objects.create(sender=auth_profile, receiver=visited_profile)
            status = 'sended_request'
        elif status == "sended_request":
            FriendRequest.objects.get(sender=auth_profile, receiver=visited_profile).delete()
            status = 'unknown'
        elif status == "received_request":
            FriendRequest.objects.get(sender=visited_profile, receiver=auth_profile).accept()
            status = 'friend'
        elif status == "friend":
            auth_profile.remove_friend(friend=visited_profile)
            status = 'unknown'

    user = MyUser.objects.get(id=id)
    profile_user = UserProfile.objects.get(user=user)
    user_posts = profile_user.post_set.all().order_by('-published')
    profile_posts = []
    for p in user_posts:
        published = f"{p.published.day}-{p.published.month}-{p.published.year} at {p.published.hour}:{p.published.minute}"
        data = {'post': p, 'images': Image.objects.filter(post=p), "profile": profile_user, 'published': published}
        profile_posts.append(data)

    return render(request, 'app/profile_page.html',
                  context={'profile_user': profile_user, 'profile_posts': profile_posts,
                           'status': status})


def settings(request):
    return render(request, 'app/settings.html')


def wall(request):
    profile_user = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = BestForm(request.POST, request.FILES)
        if form.is_valid():
            images = (request.FILES.getlist('image'))
            if request.FILES.getlist('image') == [] and request.POST['text'] == '':
                pass
            else:
                post = Post.objects.create(user_profile=profile_user, text=request.POST['text'])
                for image in images:
                    Image.objects.create(image=image, post=post)
                return redirect('wall')
    else:
        form = BestForm()
    all_posts = Post.objects.all()
    friends = profile_user.get_friends()
    posts = Post.objects.none()
    for friend in friends:
        posts = posts.union(all_posts.filter(user_profile=friend))
    posts = posts.union(all_posts.filter(user_profile=profile_user))
    posts = posts.order_by('-published')
    wall_posts = []
    for p in posts:
        published = f"{p.published.day}-{p.published.month}-{p.published.year} at {p.published.hour}:{p.published.minute}"
        data = {'post': p, 'images': Image.objects.filter(post=p),
                "profile": UserProfile.objects.get(user=p.user_profile), 'published': published}
        wall_posts.append(data)

    return render(request, 'app/wall.html',
                  {'form': form, 'wall_posts': wall_posts})


def search(request):
    # if request.method == 'GET'
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

