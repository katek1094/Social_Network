from app.ajax_views import *


# Function
def comment_tree(post):
    tree = []
    all_comments = Comment.objects.filter(post=post)
    first_tier = all_comments.filter(reply_to=None)
    for comment in first_tier:
        replies = list(all_comments.filter(reply_to=comment))
        tree.append((comment, replies))
        # tree - lista składająca się z tuples
        # tuple[0] - first tier comment, tuple[1] - all replies to it
    if tree:
        print(tree[0][0].text)
    return tree


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
                'image_quantity': len(Image.objects.filter(post=p)),
                'comment_tree': comment_tree(p)}
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
    scrollY = request.GET.get('scrollY')
    if not scrollY:
        scrollY = 0
    auth_user_profile = UserProfile.objects.get(user=request.user)
    visited_user = MyUser.objects.get(id=id)
    visited_profile = UserProfile.objects.get(user=visited_user)
    status = auth_user_profile.friend_status_with(visited_profile)
    friendship_status_actions = {'unknown': 'send friend request', 'friend': 'unfriend', 'sended request': 'cancel friend request',
                     'received request': 'accept friend request', 'self': 'self'}
    button_action = friendship_status_actions[status]
    user_posts = visited_profile.post_set.all().order_by('-published')
    profile_posts_context = post_list_context(user_posts, auth_user_profile)

    return render(request, 'app/profile_page.html',
                  context={'visited_user': visited_profile, 'profile_posts': profile_posts_context,
                           'status': status, 'scrollY': scrollY, 'button_action': button_action})


def settings(request):

    return render(request, 'app/settings.html')


def wall(request):
    scrollY = request.GET.get('scrollY')
    if not scrollY:
        scrollY = 0
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
                  {'form': form, 'wall_posts': wall_posts, 'scrollY': scrollY})


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
    if not friend_requests:
        return redirect('welcome_page')

    return render(request, 'app/friend_requests.html', {'friend_requests': friend_requests})


def gallery(request, post_id, image_id):
    auth_user_profile = UserProfile.objects.get(user=request.user)
    post = Post.objects.get(id=post_id)
    image = Image.objects.get(id=image_id)
    images = Image.objects.filter(post=post)
    image_list = list(images.values_list('id', flat=True))
    author = post.user_profile
    current_image = image_list.index(image_id)
    like = Like.objects.filter(target_image=image_id, user_profile=auth_user_profile)
    likes = Like.objects.filter(target_image=image_id)

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
                                                'right_image': right_image, 'left_image': left_image,
                                                'like': like, 'likes': likes})
