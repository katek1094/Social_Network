from app.functions import change_profile_picture
from django.core import files
from io import BytesIO
import requests
from randomuser import RandomUser
from app.models import UserProfile, Image, Friendship, Post, Like
from homepage.models import MyUser
import random, datetime
from faker import Faker


def populate_with_users(amount):
    data = RandomUser().generate_users(amount)
    index = 1
    for user in data:
        print(index)
        index += 1
        a = MyUser.objects.create_user(user.get_email(), user.get_first_name(), user.get_last_name(),
                                       user.get_dob().split("T")[0], user.get_gender(), user.get_password())
        profile = UserProfile.objects.create(user=a)
        image = Image.objects.create(profile=profile)
        url = user.get_picture()
        resp = requests.get(url)
        if resp.status_code != requests.codes.ok:
            pass
        else:
            fp = BytesIO()
            fp.write(resp.content)
            file_name = url.split("/")[-1]
            image.image.save(file_name, files.File(fp))
            change_profile_picture(image, profile)

    return 'gotowe'


def cnt():
    max_friends = 70
    min_friends = 20
    all_user_profiles = UserProfile.objects.all()
    index = 1
    end = len(all_user_profiles)
    for profile in all_user_profiles:
        print(f"{index}/{end}")
        index += 1
        if len(Friendship.objects.filter(from_user=profile)) < 18:
            new_friends = random.randrange(min_friends, max_friends, 1)
            print(new_friends)
            data = Friendship.objects.filter(from_user=profile)
            for x in range(new_friends):
                print(x, end='\r')
                new_friend = random.choice(all_user_profiles)
                check = data.filter(to_user=new_friend)
                if not check:
                    profile.add_friend(new_friend)
        else:
            print("JUZ ZROBIONE")


def clear_friendships():
    data = Friendship.objects.all()
    end = len(data)
    index = 1
    for dt in data:
        print(f"{index}/{end}")
        index += 1
        dt.delete()


def texts():
    min_amount = 2
    max_amount = 8
    profiles = UserProfile.objects.all()
    fake = Faker()
    index = 1
    for profile in profiles:
        print(f'{index}/200')
        index += 1
        if not Post.objects.filter(user_profile=profile):
            how_many = random.randrange(min_amount, max_amount, 1)
            for x in range(how_many):
                Post.objects.create(user_profile=profile, text=fake.text())
        else:
            print('done')


def fotos():
    posts = Post.objects.all().order_by("?")
    amount = len(posts)
    how_many = int(amount / 10)
    base_url = 'https://picsum.photos/width/height.jpg'
    for post in range(how_many):
        print(f'{post}/{how_many}')
        instance = posts[post]
        if not Image.objects.filter(post=instance):
            for x in range(random.randrange(1, 4, 1)):
                print('.')
                image = Image.objects.create(post=instance, published=instance.published)
                width = random.randrange(500, 900, 1)
                a = int(0.4 * width)
                height = str(random.randrange(width - a, width + a, 1))
                width = str(width)
                url = base_url.replace('width', width).replace('height', height)
                resp = requests.get(url)
                if resp.status_code != requests.codes.ok:
                    pass
                else:
                    fp = BytesIO()
                    fp.write(resp.content)
                    file_name = url.split("/")[-1]
                    image.image.save(file_name, files.File(fp))


def clear_fotos():
    images = Image.objects.filter(profile=None)
    end = len(images)
    index = 1
    for img in images:
        img.delete()
        print(f'{index}/{end}')
        index += 1




def dates():
    fake = Faker()
    posts = Post.objects.all()
    index = 1
    end = len(posts)
    for post in posts:
        print(f"{index}/{end}")
        index += 1
        x = fake.date_time_between(start_date='-10y', end_date='now')
        print(x)
        post.published = x
        print(post.published)
        print(' ')
        post.save()


def my_func(e):
    return random.randrange(1, 10000, 1)


def likes():
    profiles = UserProfile.objects.all()
    profile_how_many = len(profiles)
    profile_index = 1
    for profile in profiles:
        friends = []
        friendships = Friendship.objects.filter(from_user=profile)
        for friendship in friendships:
            friends.append(friendship.to_user)
        posts = []
        for friend in friends:
            pst = Post.objects.filter(user_profile=friend)
            for p in pst:
                posts.append(p)
        posts.sort(key=my_func)
        how_many = len(posts) * random.randrange(2, 4, 1) / 10
        index = 1
        for post in posts:
            print(f'{profile_index}/{profile_how_many} --> {index}/{how_many}')
            index += 1
            if index < how_many:
                post.like(user=profile)
        profile_index += 1


def clear_likes():
    lk = Like.objects.all()
    how_many = len(lk)
    index = 1
    for l in lk:
        print(f'{index}/{how_many}')
        index += 1
        l.delete()


def comments():
    pass
