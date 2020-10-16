from django.test import TestCase
from .models import MyUser, UserProfile, Post, Comment, Image, Friendship, FriendRequest
import datetime
from .functions import new_comment_html
from django.urls import reverse


# Create your tests here.


class NewCommentHtmlTest(TestCase):
    def setUp(self):
        user = MyUser.objects.create(email='test@test.com', first_name='test_name', last_name='test_last_name',
                                     date_of_birth=datetime.date.today(), sex='men')
        UserProfile.objects.create(user=user)

    def test(self):
        user = MyUser.objects.get(email='test@test.com')
        profile = UserProfile.objects.get(user=user)
        request = self.client.get('app/ajax/comment').wsgi_request
        text = 'test_text'
        comment_id = 2137
        result = new_comment_html(profile, request, text, comment_id)
        self.assertEqual(-1, result.find('{{'))
        self.assertEqual(-1, result.find('}}'))
        self.assertEqual(-1, result.find('%}'))
        self.assertEqual(-1, result.find('{%'))


class EditViewTest(TestCase):
    def setUp(self):
        user = MyUser.objects.create(email='test@test.com', first_name='test_name', last_name='test_last_name',
                                     date_of_birth=datetime.date.today(), sex='men')
        profile = UserProfile.objects.create(user=user)
        post = Post.objects.create(user_profile=profile, text='Test Text')
        Comment.objects.create(author=profile, text='Test Text', post=post)

    def test(self):
        post_data = {'type': 'post', "id": '1', "new_text": 'New Test Text'}
        comment_data = {'type': 'comment', "id": '1', "new_text": 'New Test Text'}

        self.client.post(reverse('edit'), post_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.client.post(reverse('edit'), comment_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        post_text = Post.objects.get(id=1).text
        comment_text = Comment.objects.get(id=1).text

        self.assertEqual(post_text, post_data['new_text'])
        self.assertEqual(comment_text, comment_data['new_text'])


class DeleteViewTest(TestCase):
    def setUp(self):
        user = MyUser.objects.create(email='test@test.com', first_name='test_name', last_name='test_last_name',
                                     date_of_birth=datetime.date.today(), sex='men')
        profile = UserProfile.objects.create(user=user)
        post1 = Post.objects.create(user_profile=profile, text='Test Text')
        post2 = Post.objects.create(user_profile=profile, text='Test Text')
        Comment.objects.create(author=profile, text='Test Text', post=post1)
        Comment.objects.create(author=profile, text='Test Text', post=post2)
        Image.objects.create(post=post1)
        Image.objects.create(post=post2)

    def test(self):
        post_data = {'type': 'post', "id": '1'}
        comment_data = {'type': 'comment', "id": '1'}
        image_data = {'type': 'image', 'id': '1'}

        self.client.post(reverse('delete', kwargs=post_data), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertFalse(Post.objects.filter(id=1))
        self.assertFalse(Comment.objects.filter(id=1))
        self.assertFalse(Image.objects.filter(id=1))

        comment_data['id'] = 2
        image_data['id'] = 2

        self.client.post(reverse('delete', kwargs=comment_data), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.client.post(reverse('delete', kwargs=image_data), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertTrue(Post.objects.filter(id=2))
        self.assertFalse(Comment.objects.filter(id=2))
        self.assertFalse(Image.objects.filter(id=2))


class FriendShipButtonViewTest(TestCase):
    def setUp(self):
        user1 = MyUser.objects.create(email='test@test.com', first_name='test_name', last_name='test_last_name',
                                      date_of_birth=datetime.date.today(), sex='men')
        user2 = MyUser.objects.create(email='test2@test.com', first_name='test_name', last_name='test_last_name',
                                      date_of_birth=datetime.date.today(), sex='men')
        UserProfile.objects.create(user=user1)
        UserProfile.objects.create(user=user2)

    def test(self):
        profile1 = UserProfile.objects.get(user=1)
        profile2 = UserProfile.objects.get(user=2)

        data = {'auth_profile_user_id': 1, 'action': 'send friend request', 'visited_profile_user_id': 2}
        self.client.post(reverse('friendship_button'), data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertTrue(FriendRequest.objects.filter(sender=profile1, receiver=profile2))

        data = {'auth_profile_user_id': 2, 'action': 'accept friend request', 'visited_profile_user_id': 1}
        self.client.post(reverse('friendship_button'), data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertTrue(Friendship.objects.filter(from_user=profile2, to_user=profile1))

        data = {'auth_profile_user_id': 2, 'action': 'unfriend', 'visited_profile_user_id': 1}
        self.client.post(reverse('friendship_button'), data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertFalse(Friendship.objects.filter(from_user=profile2, to_user=profile1))

        data = {'auth_profile_user_id': 1, 'action': 'send friend request', 'visited_profile_user_id': 2}
        self.client.post(reverse('friendship_button'), data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        data = {'auth_profile_user_id': 1, 'action': 'cancel friend request', 'visited_profile_user_id': 2}
        self.client.post(reverse('friendship_button'), data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertFalse(FriendRequest.objects.filter(sender=profile1, receiver=profile2))


class LikeViewTest(TestCase):
    def setUp(self):
        pass
