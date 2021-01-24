from app.ajax_views import *


# Functions

# import time
# start = time.time()
# end = time.time()
# print(end - start)

def post_list_context(posts, auth_user_profile):
    posts = posts[:30]
    posts_with_context = []
    for p in posts:
        published = f"{p.published.day}-{p.published.month}-{p.published.year} at " \
                    f"{p.published.hour}:{p.published.minute}"
        profile = UserProfile.objects.get(user=p.user_profile)
        data = {'post': p,
                'images': Image.objects.filter(post=p),
                "profile": profile,
                'published': published,
                'like': Like.objects.filter(target_post=p, user_profile=auth_user_profile),
                'likes': p.likes,
                'comments': Comment.objects.filter(post=p)}
        posts_with_context.append(data)
    return posts_with_context


# Views


def welcome_page(request):
    if request.user.is_authenticated:
        # profile_user = UserProfile.objects.get(user=request.user)
        # return render(request, 'app/wall.html', context={"profile_user": profile_user})
        return redirect("wall")
    else:
        return redirect('login')


def profile_page(request, id):
    scroll_y = request.GET.get('scrollY')
    if not scroll_y:
        scroll_y = 0
    auth_user_profile = UserProfile.objects.get(user=request.user)
    visited_user = MyUser.objects.get(id=id)
    visited_profile = UserProfile.objects.get(user=visited_user)
    status = auth_user_profile.friend_status_with(visited_profile)
    friendship_status_actions = {'unknown': 'send friend request', 'friend': 'unfriend',
                                 'sended request': 'cancel friend request',
                                 'received request': 'accept friend request', 'self': 'self'}
    button_action = friendship_status_actions[status]
    user_posts = visited_profile.post_set.all().order_by('-published')
    profile_posts_context = post_list_context(user_posts, auth_user_profile)
    profile_image_id = Image.objects.filter(profile=visited_profile).order_by('-published')
    if profile_image_id:
        profile_image_id = profile_image_id[0].id

    return render(request, 'app/profile_page.html',
                  context={'visited_user': visited_profile, 'profile_posts': profile_posts_context,
                           'status': status, 'scrollY': scroll_y, 'button_action': button_action,
                           'profile_image_id': profile_image_id})


def settings(request):
    auth_user_profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = NewProfilePictureUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = request.FILES.get('image')
            if not image:
                pass
            else:
                new_profile_pic = Image.objects.create(profile=auth_user_profile, image=image)
                change_profile_picture(new_profile_pic, auth_user_profile)

                return redirect('settings')
    else:
        form = NewProfilePictureUploadForm()

    return render(request, 'app/settings.html', {'form': form})


def wall(request):
    scroll_y = request.GET.get('scrollY')
    if not scroll_y:
        scroll_y = 0
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
            pass
            #  TODO: do not reload page if form is not valid, display some info about it
    else:
        form = BestForm()

    all_posts = Post.objects.all()
    friends = auth_user_profile.get_friends().iterator()

    posts = []
    for friend in friends:
        query = all_posts.filter(user_profile=friend)
        for p in query:
            posts.append(p)
    my_posts = (all_posts.filter(user_profile=auth_user_profile))
    for p in my_posts:
        posts.append(p)
    posts.sort(key=lambda x: x.published, reverse=True)
    wall_posts = post_list_context(posts, auth_user_profile)

    return render(request, 'app/wall.html',
                  {'form': form, 'wall_posts': wall_posts, 'scrollY': scroll_y})


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
    friend_requests_objects = FriendRequest.objects.filter(receiver=auth_user_profile)
    if not friend_requests_objects:
        return redirect('welcome_page')

    return render(request, 'app/friend_requests.html', {'friend_requests': friend_requests_objects})


def gallery(request, image_id):
    # gallery types: post, profile photos
    image = Image.objects.get(id=image_id)
    if image.post:
        post_id = Post.objects.get(image=image_id).id
        post = Post.objects.get(id=post_id)
        images = Image.objects.filter(post=post)
        author = post.user_profile
    elif image.profile:
        author = image.profile
        images = Image.objects.filter(profile=author)
    else:
        author = None
        images = None
        print('ERROR IN A GALLERY VIEW, SOMETHING WRONG WITH IMAGE INSTANCE ATTRIBUTES')

    auth_user_profile = UserProfile.objects.get(user=request.user)
    image_list = list(images.values_list('id', flat=True))
    current_image = image_list.index(image_id)
    is_liked = Like.objects.filter(target_image=image_id, user_profile=auth_user_profile)
    likes = len(Like.objects.filter(target_image=image_id))
    comments = Comment.objects.filter(image=image)

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

    return render(request, 'app/gallery.html', {'author': author, 'image': image,
                                                'right_image': right_image, 'left_image': left_image,
                                                'like': is_liked, 'likes': likes, 'comments': comments})
